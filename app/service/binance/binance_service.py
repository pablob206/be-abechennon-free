"""Binance service module"""
# Built-In
from datetime import datetime
from typing import List

# Third-Party
from fastapi import HTTPException
from binance import BinanceSocketManager

# App
from app.models import KlineIntervalEnum, MdLogs
from app.service.binance import binance_client
from app.service.settings import get_settings_status, get_settings


async def build_stream_name(
    symbol_list: list,
    socket_name: str,
    interval_list: list[KlineIntervalEnum] | None = None,
) -> List[str]:
    """
    Build stream name, type <symbol>@kline_<interval> or <symbol>@trade
    :return: list, stream name I.e: ["adausdt@kline_1m", "btcusdt@kline_1m", "ethusdt@kline_1m"]
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


async def initialize_ws_binance_client():
    """
    Initialize websocket from binance client
    """

    binance_status = await get_settings_status()
    if "error_fields" in binance_status:
        raise HTTPException(400, f"Missing field: {binance_status.get('error_fields')}")

    binance_settings = await get_settings()

    kline_stream_list = await build_stream_name(
        symbol_list=binance_settings.get("pairsList"),
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

    # client = await AsyncClient.create( # <binance.client.AsyncClient object at 0x7fb9a233f7f0>
    # <class 'binance.client.AsyncClient'>

    #     api_key=get_settings().BINANCE_API_KEY,
    #     api_secret=get_settings().BINANCE_API_SECRET,
    #     requests_params={"timeout": 20}
    # )
    client = (
        binance_client.__call__()
    )  # <binance.client.AsyncClient object at 0x7f3a8824a5f0> <class 'binance.client.AsyncClient'>
    print(client, type(client))

    bm = BinanceSocketManager(client, user_timeout=60)
    ms = bm.multiplex_socket(kline_stream_list)

    count = 0
    async with ms as ms_listener:
        while True:
            count += 1
            resp = (
                await ms_listener.recv()
            )  # {'stream': 'adausdt@kline_1m', 'data': {'e': 'kline', 'E': 1670257782485,
            # 's': 'ADAUSDT', 'k': {'t': 1670257740000, 'T': 1670257799999, 's': 'ADAUSDT', 'i': '1m',
            # 'f': 418874080, 'L': 418874096, 'o': '0.32040000', 'c': '0.32030000', 'h': '0.32040000',
            # 'l': '0.32030000', 'v': '6994.90000000', 'n': 17, 'x': False, 'q': '2241.10655000',
            # 'V': '2508.80000000', 'Q': '803.81952000', 'B': '0'}}}
            resp = resp.get("data")

            if "k" in resp:
                eventType, eventTime, symbol, ticks = resp.values()
                if ticks.get("x"):
                    print(count, eventType, eventTime, symbol, ticks)
                    log = MdLogs(
                        eventType=eventType,
                        eventTime=eventTime,
                        intervalKline=(
                            ticks.get("i") if eventType == "kline" else None
                        ),
                        datetimeAt=datetime.utcnow(),
                        symbol=symbol,
                        ticks=ticks,
                    )
                    log.save()

    # return await client.close_connection()
