"""Module to store commons constants used in the project"""
# Built-In
from enum import StrEnum


class BotStatusEnum(StrEnum):
    """
    Define different bot status types
    """

    RUNNING = "RUNNING"
    STOPPED = "STOPPED"
    MAINTANANCE = "MAINTANANCE"
    TESTING = "TESTING"


class AppStatusEnum(StrEnum):
    """
    Define different app status types
    """

    RUNNING = "RUNNING"
    STOPPED = "STOPPED"
    MAINTANANCE = "MAINTANANCE"
    TESTING = "TESTING"


class SocketTypeEnum(StrEnum):
    """Define different websocket types"""

    KLINE = "kline"
    TRADE = "trade"
    AGGTRADE = "aggTrade"
    DEPTH = "depth"
    TICKER = "ticker"


class TradingTypeEnum(StrEnum):
    """Define diferent trading types"""

    SPOT = "SPOT"
    MARGIN = "MARGIN"
    FUTURES = "FUTURES"
    P2P = "P2P"


class WalletTypeEnum(StrEnum):
    """Define different wallet types"""

    SPOT = "spot"
    MARGIN = "margin"
    FUTURES = "futures"
    OPTIONS = "options"
    FUNDING = "funding"


class CurrencyBaseEnum(StrEnum):
    """Define different currency types"""

    USDT = "USDT"


class ExecTypeEnum(StrEnum):
    """Define different execute-types"""

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


class OrdStatusEnum(StrEnum):
    """Define different order status types"""

    NEW = "NEW"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELED = "CANCELED"
    PENDING_CANCEL = "PENDING_CANCEL"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"


class KlineIntervalEnum(StrEnum):
    """Define diferent timeframe interval types"""

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


class SideEnum(StrEnum):
    """Define different side types"""

    BUY = "BUY"  # 1
    SELL = "SELL"  # 2


class OrdTypeEnum(StrEnum):
    """Define different order types"""

    LIMIT = "LIMIT"
    MARKET = "MARKET"
    STOP_LOSS = "STOP_LOSS"
    STOP_LOSS_LIMIT = "STOP_LOSS_LIMIT"
    TAKE_PROFIT = "TAKE_PROFIT"
    TAKE_PROFIT_LIMIT = "TAKE_PROFIT_LIMIT"
    LIMIT_MAKER = "LIMIT_MAKER"


class TimeInForceEnum(StrEnum):
    """Define different timeinforce types"""

    GTC = "GTC"
    IOC = "IOC"
    FOK = "FOK"


class OrderRespEnum(StrEnum):
    """Define diferent order response types"""

    ACK = "ACK"
    RESULT = "RESULT"
    FULL = "FULL"


class AggTradeEnum(StrEnum):
    """
    Define diferent Aggregate trade types.
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


class WsDeepthEnum(StrEnum):
    """
    Define diferent websocket depth types.
    For Websocket Depth these are found on binance.websockets.BinanceSocketManager.
    """

    WEBSOCKET_DEPTH_5 = "5"
    WEBSOCKET_DEPTH_10 = "10"
    WEBSOCKET_DEPTH_20 = "20"
