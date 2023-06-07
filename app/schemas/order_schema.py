"""Order schemas module"""
# Third-Party
from pydantic import BaseModel

# App
from app.models import (
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

    class Config:
        """Config"""

        schema_extra = {
            "example": {
                "pair": "BTCUSDT",
                "trading_type": TradingTypeEnum.MARGIN,
                "is_isolated": False,
                "side": SideEnum.BUY,
                "ord_type": OrdTypeEnum.MARKET,
                "orig_qty": 1.36,
                "time_in_force": TimeInForceEnum.GTC,
                "limit_price": 1802.30,
            }
        }
