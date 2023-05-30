"""Strategy Enum module"""
# Built-In
from enum import Enum


class OhlcvValueEnum(str, Enum):
    """Define different ohlcv value"""

    OPEN_TIME = "open_time"
    OPEN = "open"
    HIGH = "high"
    LOW = "low"
    CLOSE = "close"
    VOLUME = "volume"
    CLOSE_TIME = "close_time"
    QUOTE_ASSET_VOLUME = "quote_asset_volume"
    NUMBER_OF_TRADES = "number_of_trades"
    TAKER_BUY_BASE_ASSET_VOLUME = "taker_buy_base_asset_volume"
    TAKER_BUY_QUOTE_ASSET_VOLUME = "taker_buy_quote_asset_volume"
    IGNORE = "ignore"


class SignalWhenValueIs(str, Enum):
    """Define different signal when value is"""

    LESS_THAN = "LESS_THAN (<)"
    LESS_THAN_OR_EQUAL = "LESS_THAN_OR_EQUAL  (<=)"
    EQUAL = "EQUAL (=)"
    GREATER_THAN_OR_EQUAL = "GREATER_THAN_OR_EQUAL (>=)"
    GREATER_THAN = "GREATER_THAN (>)"


class ChartPeriodSecEnum(str, Enum):
    """Define different chart period in seconds"""

    ONE_MIN = 60
    THREE_MIN = 180
    FIVE_MIN = 300
    FIFTEEN_MIN = 900
    THIRTY_MIN = 1800
    ONE_HOUR = 3600
    TWO_HOUR = 7200
    FOUR_HOUR = 14400
    SIX_HOUR = 21600
    EIGHT_HOUR = 28800
    ONE_DAY = 86400
    THREE_DAY = 259200
    ONE_WEEK = 604800
    ONE_MONTH = 2592000
