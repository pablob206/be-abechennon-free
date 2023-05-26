"""Binance socket engine module"""
# Built-In
from datetime import datetime
import asyncio

# Third-Party
from binance import BinanceSocketManager  # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession

# App
from app.models import MdLogs, SocketTypeEnum, Settings, AppStatusEnum
from app.config import settings
from app.service.binance.binance_service import (
    build_stream_name,
    get_pairs_availables,
    set_klines,
    update_klines_cache,
    binance_client,
)
from app.data_access import clear_cache, get_settings_query


async def init_binance_websocket_engine(db_session: AsyncSession | None = None) -> None:
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

    if settings.APP_STATUS != AppStatusEnum.RUNNING:
        return

    clear_cache()

    await asyncio.sleep(2)
    settings_db: Settings = await get_settings_query(db_session=db_session)

    pairs_availables: dict = await get_pairs_availables(
        currency_base=settings_db.currency_base, trading_type=settings_db.trading_type
    )
    pair_list = [  # pylint: disable=unnecessary-comprehension
        pair for pair in pairs_availables
    ]
    kline_stream: list = build_stream_name(
        pair_list=pair_list,
        socket_name=settings.BINANCE_SOCKET_NAME[0],
        interval_list=settings.BINANCE_SOCKET_INTERVAL,
    )

    multiplex_socket = BinanceSocketManager(
        client=binance_client(), user_timeout=60
    ).multiplex_socket(streams=kline_stream)

    for interval in settings.BINANCE_SOCKET_INTERVAL:
        asyncio.ensure_future(
            set_klines(
                pair_list=pair_list,
                interval=interval,
                limit=settings.BINANCE_CACHE_LIMIT,
            )
        )

    try:
        async with multiplex_socket as multiplex_listener:
            while True:
                if not (ml_resp := await multiplex_listener.recv()):
                    continue
                ml_data = ml_resp["data"]
                if "k" in ml_data:
                    event_type, event_time, symbol, tick = ml_data.values()
                    await update_klines_cache(pair=symbol, tick=tick)
                    if tick["x"]:
                        log = MdLogs(
                            eventType=event_type,
                            eventTime=event_time,
                            intervalKline=(
                                tick["i"]
                                if event_type == SocketTypeEnum.KLINE
                                else None
                            ),
                            datetimeAt=datetime.utcnow(),
                            symbol=symbol,
                            tick=tick,
                        )
                        log.save()

    except Exception:
        await binance_client().close_connection()
        raise
