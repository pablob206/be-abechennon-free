"""Loan schemas module"""
# Third-Party
from pydantic import BaseModel

# App
from app.models import TradingTypeEnum


class LoanSchema(BaseModel):
    """Loan schema"""

    asset: str
    amount: float
    trading_type: TradingTypeEnum

    class Config:
        """Config"""

        schema_extra = {
            "example": {
                "asset": "USDT",
                "amount": 20.0,
                "trading_type": TradingTypeEnum.MARGIN,
            }
        }
