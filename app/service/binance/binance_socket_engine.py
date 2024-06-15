"""Binance socket engine module"""

# Built-In
import asyncio
import logging
from datetime import datetime

# Third-Party
from binance import BinanceSocketManager
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import async_session, settings
from app.data_access import clear_cache, get_setting_query

# App
from app.models import MdLogs, Setting
from app.schemas import AppStatusEnum, OrderRequest, SettingStatusEnum, SocketTypeEnum
from app.service.binance import (  # type: ignore
    binance_client,
    build_stream_name,
    get_pairs_availables,
    set_klines,
    update_klines,
)
from app.service.order_management_service import OrderManagementService
from app.service.setting_service import SettingsService
from app.service.strategy_service import StrategyServices

logger = logging.getLogger("WebSocketClient")


# pylint: disable=too-many-locals, too-many-branches, too-many-statements
async def init_binance_websocket_engine(
    cache_clear: bool | None = False,
    db_session: AsyncSession | None = None,
) -> None:
    """
    Initialize binance websocket

    multiplex_listener. I.e: {
        'stream': 'adausdt@kline_1m',
        'data': {
            'e': 'kline',
            'E': 1670257782485,
            's': 'ADAUSDT',
            'k': {
                't': 1670257740000,
                'T': 1670257799999,
                's': 'ADAUSDT',
                'i': '1m',
                'f': 418874080,
                'L': 418874096,
                'o': '0.32040000',
                'c': '0.32030000',
                'h': '0.32040000',
                'l': '0.32030000',
                'v': '6994.90000000',
                'n': 17,
                'x': False,
                'q': '2241.10655000',
                'V': '2508.80000000',
                'Q': '803.81952000',
                'B': '0'
            }
        }
    }
    """

    await asyncio.sleep(5)

    market_data_start = False
    while market_data_start is False:
        market_data_status = (
            await binance_client().get_system_status()  # type: ignore
        )  # {'status': 0, 'msg': 'normal'}  # type: ignore
        setting_status = await SettingsService().get_setting_status()
        if (
            settings.APP_STATUS != AppStatusEnum.RUNNING
            or setting_status["status"] != SettingStatusEnum.FULL
            or market_data_status["status"] != 0
        ):
            await asyncio.sleep(30)
            continue
        market_data_start = True

    if cache_clear:
        clear_cache(db_redis=settings.DB_REDIS_KLINES)

    if not db_session:
        async with async_session.begin() as db_session:  # type: ignore
            pass

    setting_db: Setting = await get_setting_query(db_session=db_session)

    pairs_availables: dict = await get_pairs_availables(
        currency_base=setting_db.currency_base, trading_type=setting_db.trading_type  # type: ignore
    )
    pair_list = [pair for pair in pairs_availables]  # pylint: disable=unnecessary-comprehension
    kline_stream: list = build_stream_name(
        pair_list=pair_list,
        socket_name=settings.BINANCE_SOCKET_NAME[0],
        interval_list=settings.BINANCE_SOCKET_INTERVAL,
    )

    multiplex_socket = BinanceSocketManager(client=binance_client(), user_timeout=60).multiplex_socket(  # type: ignore
        streams=kline_stream
    )

    if cache_clear:
        for interval in settings.BINANCE_SOCKET_INTERVAL:
            await set_klines(
                pair_list=pair_list,
                interval=interval,
                limit=settings.BINANCE_CACHE_LIMIT,
            )
    try:
        logger.info("Attempting to connect to Binance Websocket")
        async with multiplex_socket as multiplex_listener:
            while True:
                if not (ml_resp := await multiplex_listener.recv()):
                    continue
                if ml_resp.get("e") == "error":  # {'e': 'error', 'm': 'Queue overflow. Message not filled'}
                    await binance_client().close_connection()  # type: ignore
                    await init_binance_websocket_engine(db_session=db_session, cache_clear=False)
                if not (ml_data := ml_resp.get("data")):
                    continue
                if "k" in ml_data:
                    event_type, event_time, symbol, tick = ml_data.values()
                    update_klines(pair=symbol, tick=tick)

                    update_detail_account = False
                    if setting_db.is_real_time:  # real time
                        for pair in setting_db.pairs:
                            signal = await StrategyServices.strategy_temp(pair=pair, setting_db=setting_db)
                            if signal and setting_db.bot_status:
                                await OrderManagementService(db_session=db_session).create_order(
                                    order=OrderRequest(
                                        pair=pair,
                                        trading_type=setting_db.trading_type,  # type: ignore
                                        side=signal,
                                        ord_type=setting_db.order_type,  # type: ignore
                                        orig_qty=setting_db.amount_per_order,  # type: ignore
                                    ),
                                )
                                update_detail_account = True
                    elif not setting_db.is_real_time and tick["x"]:  # only kline is finished
                        for pair in setting_db.pairs:
                            signal = await StrategyServices.strategy_temp(pair=pair, setting_db=setting_db)
                            if signal and setting_db.bot_status:
                                await OrderManagementService(db_session=db_session).create_order(
                                    order=OrderRequest()  # type: ignore
                                )
                            update_detail_account = True

                    if update_detail_account:
                        # update detail account
                        update_detail_account = False

                    if tick["x"]:
                        log = MdLogs(
                            eventType=event_type,
                            eventTime=event_time,
                            intervalKline=(tick["i"] if event_type == SocketTypeEnum.KLINE else None),
                            createdAt=datetime.utcnow(),
                            symbol=symbol,
                            tick=tick,
                        )
                        log.save()

    except Exception as exc:
        await binance_client().close_connection()  # type: ignore
        logger.error("Unexpected error has occurred:")
        logger.exception(exc)
        raise
    finally:
        await db_session.close()
