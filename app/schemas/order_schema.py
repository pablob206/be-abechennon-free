"""Order schemas module"""
# Third-Party
from pydantic import BaseModel

# App
from app.schemas import (
    TradingTypeEnum,
    OrdTypeEnum,
    SideEnum,
    TimeInForceEnum,
)


class OrderSchema(BaseModel):
    """Order schema"""

    pair: str
    trading_type: TradingTypeEnum
    is_isolated: bool | None = False
    side: SideEnum
    ord_type: OrdTypeEnum
    orig_qty: float
    time_in_force: TimeInForceEnum | None = TimeInForceEnum.GTC
    limit_price: float | None = None
