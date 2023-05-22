"""Binance service module"""
# Built-In
from datetime import datetime
from typing import List

# Third-Party
from fastapi import HTTPException
from binance import BinanceSocketManager, AsyncClient  # type: ignore[attr-defined]
from sqlalchemy.ext.asyncio import AsyncSession

# App
from app.models import KlineIntervalEnum, MdLogs
from app.service.settings import get_settings_status, get_settings
from app.config import settings


async def build_stream_name(
    symbol_list: list,
    socket_name: str,
    interval_list: list[KlineIntervalEnum] | None = None,
) -> List[str]:
    """
    Build stream name, type <symbol>@kline_<interval> or <symbol>@trade
    :return: list, stream name I.e: ["adausdt@kline_1m", "btcusdt@kline_5m", "ethusdt@kline_15m"]
    """

    stream_name_ls = []
    for symbol in symbol_list:
        stream_name = symbol + "@" + socket_name
        if interval_list:
            for interval in interval_list:
                stream_name_interval = stream_name + "_" + interval.value
                stream_name_ls.append(stream_name_interval)
        else:
            stream_name_ls.append(stream_name)

    return stream_name_ls


async def init_binance_websocket(db_session: AsyncSession, _id: int | None = 1) -> None:
    """
    Initialize websocket from binance client

    multiplex_listener example: {
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
                'B':
                '0'
            }
        }
    }
    """

    binance_status = await get_settings_status(_id=_id, db_session=db_session)
    if binance_status["missing_fields"]:
        raise HTTPException(400, f"Missing field: {binance_status['missing_fields']}")

    binance_settings = await get_settings(_id=_id, db_session=db_session)

    kline_stream_list = await build_stream_name(
        symbol_list=binance_settings.pairs_list,
        socket_name="kline",  # optional socket_name="trade"
        interval_list=[
            KlineIntervalEnum.KLINE_INTERVAL_1MINUTE,
            KlineIntervalEnum.KLINE_INTERVAL_5MINUTE,
            KlineIntervalEnum.KLINE_INTERVAL_15MINUTE,
            KlineIntervalEnum.KLINE_INTERVAL_1HOUR,
            KlineIntervalEnum.KLINE_INTERVAL_4HOUR,
            KlineIntervalEnum.KLINE_INTERVAL_12HOUR,
            KlineIntervalEnum.KLINE_INTERVAL_1DAY,
            KlineIntervalEnum.KLINE_INTERVAL_1WEEK,
        ],
    )

    ws_client: AsyncClient = await AsyncClient.create(
        api_key=settings.BINANCE_API_KEY,
        api_secret=settings.BINANCE_API_SECRET,
        requests_params={"timeout": 20},
    )

    multiplex_socket = BinanceSocketManager(
        ws_client, user_timeout=60
    ).multiplex_socket(kline_stream_list)

    count = 0
    try:
        async with multiplex_socket as multiplex_listener:
            while True:
                count += 1
                if not (ml_resp := await multiplex_listener.recv()):
                    continue

                ml_data = ml_resp["data"]
                if "k" in ml_data:
                    event_type, event_time, symbol, ticks = ml_data.values()
                    if ticks["x"]:
                        # print(count, event_type, event_time, symbol, ticks)
                        log = MdLogs(
                            eventType=event_type,
                            eventTime=event_time,
                            intervalKline=(
                                ticks.get("i") if event_type == "kline" else None
                            ),
                            datetimeAt=datetime.utcnow(),
                            symbol=symbol,
                            ticks=ticks,
                        )
                        log.save()
    except Exception:
        await ws_client.close_connection()
        raise
