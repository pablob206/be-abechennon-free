"""Order request schemas module"""

# Third-Party
from pydantic import BaseModel

# App
from app.schemas import (
    TradingTypeEnum,
    OrdTypeEnum,
    SideEnum,
    TimeInForceEnum,
)


class OrderRequest(BaseModel):
    """Order request schema"""

    pair: str
    trading_type: TradingTypeEnum
    is_isolated: bool | None = False
    side: SideEnum
    ord_type: OrdTypeEnum
    orig_qty: float
    time_in_force: TimeInForceEnum | None = TimeInForceEnum.GTC
    limit_price: float | None = None
