"""Bot functions module"""

# Built-In
from typing import List, Dict, Any
from collections import defaultdict
import orjson

# Third-Party
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

# App
from app.config import settings
from app.schemas import TradingTypeEnum, WalletTypeEnum
from app.service.binance import binance_client
from app.data_access import set_klines_cache, get_klines_cache, get_setting_query


def build_stream_name(
    pair_list: list,
    socket_name: str,
    interval_list: list | None = None,
) -> List[str]:
    """
    Build stream name for websocket. I.e: <symbol>@kline_<interval> or <symbol>@trade
    :param pair_list: list, pair list. I.e: ["ADAUSDT", "BTCUSDT", "ETHUSDT"]
    :param socket_name: str, socket name. I.e: "kline_1m" or "trade"
    :return: list, stream name. I.e: ["adausdt@kline_1m", "btcusdt@kline_5m", "ethusdt@kline_15m"]
    """

    stream_name_list = [f"{pair.lower()}@{socket_name}" for pair in pair_list]
    if interval_list:
        stream_name_list = [
            f"{stream_name}_{interval}" for stream_name in stream_name_list for interval in interval_list
        ]
    return stream_name_list


async def get_assets_details(db_session: AsyncSession, wallet: WalletTypeEnum) -> Dict[str, Any]:
    """
    Get assets details
    """

    if wallet != WalletTypeEnum.MARGIN:
        raise HTTPException(
            status_code=400,
            detail=f"Assets details not available for wallet [{wallet}]",
        )

    if not (setting_db := await get_setting_query(db_session=db_session)):
        raise HTTPException(status_code=404, detail="Setting not found")

    if not (margin_account := await binance_client().get_margin_account()):
        raise HTTPException(status_code=404, detail="Margin account not found")

    total_margin_account = {}
    for user_assets in margin_account["userAssets"]:
        current_data = {}
        for pair in setting_db.pairs:
            if user_assets["asset"] == pair.replace(setting_db.currency_base, ""):
                price = 0
                if pair != "USDT":
                    if not (ticker := await binance_client().get_symbol_ticker(symbol=pair)):
                        raise HTTPException(status_code=404, detail=f"Ticker [{pair}] not found")

                    price = ticker["price"]
                current_data["asset"] = user_assets["asset"]
                current_data["free"] = float(user_assets["free"])
                current_data["locked"] = float(user_assets["locked"])
                current_data["borrowed"] = float(user_assets["borrowed"])
                current_data["interest"] = float(user_assets["interest"])
                current_data["netAsset"] = float(user_assets["netAsset"])
                current_data["free_usdt"] = float(user_assets["free"]) * float(price)
                current_data["borrowed_usdt"] = float(user_assets["borrowed"]) * float(price)

                total_margin_account[pair] = current_data
    return total_margin_account


async def get_pairs_availables(
    currency_base: str, trading_type: TradingTypeEnum | None = TradingTypeEnum.MARGIN
) -> Dict[str, str]:
    """
    Get pairs availables by currency-base and trading-type, format: 'pair'-'currency'.
    """

    if trading_type == TradingTypeEnum.MARGIN:
        if margin_account := await binance_client().get_all_isolated_margin_symbols():
            pairs_availables = {
                item["symbol"].upper(): item["base"].upper()
                for item in margin_account
                if item["isMarginTrade"]
                and item["isBuyAllowed"]
                and item["isSellAllowed"]
                and item["quote"] == currency_base.upper()
            }
            if not pairs_availables:
                raise HTTPException(status_code=404, detail=f"[{currency_base}] pairs not found")
            return pairs_availables
        raise HTTPException(status_code=404, detail=f"[{trading_type}] pairs not found")
    raise HTTPException(status_code=400, detail=f"Only support [{TradingTypeEnum.MARGIN}] trading type")


async def set_klines(
    pair_list: list,
    interval: str,
    limit: int | None = 500,
    is_real_time: bool | None = False,
) -> Dict[str, defaultdict[str, List[float]]]:
    """
    Set klines to cache
    :param pair_list: list, pair list. I.e: ["ADAUSDT", "ETHUSDT", "BTCUSDT", ...]
    :param interval: str, interval. I.e: "1m", "5m", "15m", "1h", "4h", "1d", "1w", "1M"
    :param limit: int, limit. I.e: 500
    :param is_real_time: bool, is real-time. I.e: True, False
    :return: dict, klines. I.e: {
        "ADAUSDT": {
            "o": [0.3621, 0.3622, 0.3623],
            "h": [0.3623, 0.3623, 0.3624],
            "l": [0.362, 0.3619, 0.3612],
            "c": [0.3622, 0.362, 0.361],
            "v": [98704.4, 166018.2, 166018.5]
        },
        "ETHUSDT": {
            "o": [1818.8, 1819.08, 1819.09],
            "h": [1819.92, 1819.41, 1819.43],
            "l": [1818.79, 1818.56, 1818.57],
            "c": [1819.09, 1818.59, 1818.57],
            "v": [740.3435, 296.5204, 296.5304]
        },
        ...
    }
    """

    klines_proccessed_dict = {}
    for pair in pair_list:
        historical_klines_list = await binance_client().get_historical_klines(
            symbol=pair.upper(), interval=interval, limit=limit
        )
        if is_real_time:
            historical_klines_list.pop()

        temp_dict = defaultdict(list)
        for historical_klines in historical_klines_list:
            temp_dict["o"].append(float(historical_klines[1]))
            temp_dict["h"].append(float(historical_klines[2]))
            temp_dict["l"].append(float(historical_klines[3]))
            temp_dict["c"].append(float(historical_klines[4]))
            temp_dict["v"].append(float(historical_klines[5]))

        temp_dict_bytes = {key: orjson.dumps(value) for key, value in temp_dict.items()}
        set_klines_cache(
            name=f"{pair}_{interval}",
            mapping=temp_dict_bytes,
            db_redis=settings.DB_REDIS_KLINES,
        )
        klines_proccessed_dict[f"{pair}_{interval}"] = temp_dict

    return klines_proccessed_dict


def update_klines(pair: str, tick: dict) -> None:
    """
    Update klines to cache
    :param pair: str, pair. I.e: "ADAUSDT"
    :param tick: dict, tick data. I.e: {
        't': 1684713600000,
        'T': 1685318399999,
        's': 'BTCUSDT',
        'i': '1d',
        'f': 3123210913,
        'L': 3124672724,
        'o': '26747.78000000',
        'c': '27181.21000000',
        'h': '27495.83000000',
        'l': '26538.21000000',
        'v': '62503.70702000',
        'n': 1461812,
        'x': False,
        'q': '1691918401.25784200',
        'V': '30308.57098000',
        'Q': '820436172.02136090',
        'B': '0'
    }
    """

    interval = tick["i"]
    if not (tick_cache_bytes := get_klines_cache(name=f"{pair}_{interval}", db_redis=settings.DB_REDIS_KLINES)):
        return
    tick_cache = {}
    for key, value in tick_cache_bytes.items():
        key = key.decode("utf-8")
        value = orjson.loads(value)
        if tick["x"]:
            value = value[1:]
            value.append(float(tick[key]))
        else:
            value.pop()
            value.append(float(tick[key]))
        tick_cache[key] = value
    temp_dict_bytes: dict = {key: orjson.dumps(value) for key, value in tick_cache.items()}
    return set_klines_cache(
        name=f"{pair}_{interval}",
        mapping=temp_dict_bytes,
        db_redis=settings.DB_REDIS_KLINES,
    )
