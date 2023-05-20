"""Commons Enum module"""
# Built-In
from enum import Enum


class ExecTypeEnum(str, Enum):
    """Define different execute-type"""

    NEW = "NEW"  # 0
    DONE_FOR_DAY = "DONE_FOR_DAY"  # 3
    CANCELED = "CANCELED"  # 4
    REPLACE = "REPLACE"  # 5
    PENDING_CANCEL = "PENDING_CANCEL"  # 6
    STOPPED = "STOPPED"  # 7
    REJECTED = "REJECTED"  # 8
    SUSPENDEND = "SUSPENDEND"  # 9
    PENDING_NEW = "PENDING_NEW"  # A
    CALCULATED = "CALCULATED"  # B
    EXPIRED = "EXPIRED"  # C
    RESTATED = "RESTATED"  # D
    PENDING_REPLACE = "PENDING_REPLACE"  # E
    TRADE = "TRADE"  # F (partial fill or fill)
    TRADE_CORRECT = "TRADE_CORRECT"  # G
    TRADE_CANCEL = "TRADE_CANCEL"  # H
    ORDER_STATUS = "ORDER_STATUS"  # I


class SymbolTypeEnum(str, Enum):
    """Define diferent symbol type"""

    SYMBOL_TYPE_SPOT = "SPOT"


class OrdStatusEnum(str, Enum):
    """Define different order status"""

    ORDER_STATUS_NEW = "NEW"
    ORDER_STATUS_PARTIALLY_FILLED = "PARTIALLY_FILLED"
    ORDER_STATUS_FILLED = "FILLED"
    ORDER_STATUS_CANCELED = "CANCELED"
    ORDER_STATUS_PENDING_CANCEL = "PENDING_CANCEL"
    ORDER_STATUS_REJECTED = "REJECTED"
    ORDER_STATUS_EXPIRED = "EXPIRED"


class KlineIntervalEnum(str, Enum):
    """Define diferent timeframe interval"""

    KLINE_INTERVAL_1MINUTE = "1m"
    KLINE_INTERVAL_3MINUTE = "3m"
    KLINE_INTERVAL_5MINUTE = "5m"
    KLINE_INTERVAL_15MINUTE = "15m"
    KLINE_INTERVAL_30MINUTE = "30m"
    KLINE_INTERVAL_1HOUR = "1h"
    KLINE_INTERVAL_2HOUR = "2h"
    KLINE_INTERVAL_4HOUR = "4h"
    KLINE_INTERVAL_6HOUR = "6h"
    KLINE_INTERVAL_8HOUR = "8h"
    KLINE_INTERVAL_12HOUR = "12h"
    KLINE_INTERVAL_1DAY = "1d"
    KLINE_INTERVAL_3DAY = "3d"
    KLINE_INTERVAL_1WEEK = "1w"
    KLINE_INTERVAL_1MONTH = "1M"


class SideEnum(str, Enum):
    """Define different side type"""

    BUY = "BUY"  # 1
    SELL = "SELL"  # 2


class OrdTypeEnum(str, Enum):
    """Define different order type"""

    ORDER_TYPE_LIMIT = "LIMIT"
    ORDER_TYPE_MARKET = "MARKET"
    ORDER_TYPE_STOP_LOSS = "STOP_LOSS"
    ORDER_TYPE_STOP_LOSS_LIMIT = "STOP_LOSS_LIMIT"
    ORDER_TYPE_TAKE_PROFIT = "TAKE_PROFIT"
    ORDER_TYPE_TAKE_PROFIT_LIMIT = "TAKE_PROFIT_LIMIT"
    ORDER_TYPE_LIMIT_MAKER = "LIMIT_MAKER"


class TimeInForceEnum(str, Enum):
    """Define different timeinforce type"""

    TIME_IN_FORCE_GTC = "GTC"
    TIME_IN_FORCE_IOC = "IOC"
    TIME_IN_FORCE_FOK = "FOK"


class OrderRespEnum(str, Enum):
    """Define diferent order response type"""

    ORDER_RESP_TYPE_ACK = "ACK"
    ORDER_RESP_TYPE_RESULT = "RESULT"
    ORDER_RESP_TYPE_FULL = "FULL"


class AggTradeEnum(str, Enum):
    """
    Define diferent Aggregate trade.
    For accessing the data returned by Client.aggregate_trades().
    """

    AGG_ID = "a"
    AGG_PRICE = "p"
    AGG_QUANTITY = "q"
    AGG_FIRST_TRADE_ID = "f"
    AGG_LAST_TRADE_ID = "l"
    AGG_TIME = "T"
    AGG_BUYER_MAKES = "m"
    AGG_BEST_MATCH = "M"


class WsDeepthEnum(str, Enum):
    """
    Define diferent websocket depth.
    For Websocket Depth these are found on binance.websockets.BinanceSocketManager.
    """

    WEBSOCKET_DEPTH_5 = "5"
    WEBSOCKET_DEPTH_10 = "10"
    WEBSOCKET_DEPTH_20 = "20"
