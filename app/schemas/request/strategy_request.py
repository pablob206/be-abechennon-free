"""Strategy request schemas module"""

# Built-In
from typing import Dict, List

# Third-Party
from pydantic import BaseModel, Field

# App
from app.schemas import ChartPeriodSecEnum, SideEnum


class CandleValue(BaseModel):
    """Candle Value schema"""

    type_: str = Field("select", title="Type Input")
    name: str = Field("OHLCV Value", title="Name of the Candle Value")
    options: List = Field(["open", "high", "low", "close", "volume"], title="Options")
    default: str = Field("close", title="Default")


class Period(BaseModel):
    """Period schema"""

    type_: str = Field("number", title="Type Input")
    step: int = Field(1, title="Step")
    min_: int = Field(1, title="Min")
    max_: int = Field(500, title="Max")
    name: str = Field("RSI Period", title="Name Period")
    default: int = Field(14, title="Default")
    value: int = Field(14, title="Value")


class SignalWhen(BaseModel):
    """Signal When schema"""

    type_: str = Field("value", title="Type Input")
    signal_when: str = Field(">=", title="Signal When")
    signal_when_value: int = Field(80, title="Signal When Value")
    defaults: Dict = Field(None, title="Defaults")


class ShortPeriod(BaseModel):
    """Short Period schema"""

    type_: str = Field("number", title="Type Input")
    step: int = Field(1, title="Step")
    min_: int = Field(1, title="Min")
    max_: int = Field(500, title="Max")
    name: str = Field("Short Period", title="Name Period")
    default: int = Field(5, title="Default")


class LongPeriod(BaseModel):
    """Long Period schema"""

    type_: str = Field("number", title="Type Input")
    step: int = Field(1, title="Step")
    min_: int = Field(1, title="Min")
    max_: int = Field(500, title="Max")
    name: str = Field("Long Period", title="Name Period")
    default: int = Field(20, title="Default")


class BaseParams(BaseModel):
    """Base Type schema"""

    period: Period = Field(None, title="Period")
    candle_value: CandleValue = Field(None, title="Candle Value")
    signal_when: SignalWhen = Field(None, title="Signal When")
    short_period: ShortPeriod = Field(None, title="Short Period")
    long_period: LongPeriod = Field(None, title="Long Period")


class StrategyData(BaseModel):
    """Strategy data base schema"""

    name: str = Field(None, title="Indicator Name")
    signal_type: SideEnum = Field(SideEnum.BUY, title="Signal Type", description="BUY or SELL")
    chartperiod: ChartPeriodSecEnum = Field(
        ChartPeriodSecEnum.FIFTEEN_MIN,
        title="Chart Period",
        description="Chart Period in seconds",
    )
    candle_pattern: bool = Field(False, title="Candle Pattern")
    necessary: bool = Field(True, title="Necessary Signal")
    keep_signal: int = Field(None, title="Keep Signal")
    params: BaseParams = Field(None, title="Indicators parameters")


class StrategyRequest(BaseModel):
    """Strategy request schema"""

    name: str = Field(None, title="Strategy Name")
    description: str = Field(None, title="Strategy Description")
    data: List[StrategyData] = Field(None, title="Strategy Data")
