"""Loan schemas module"""
# Third-Party
from pydantic import BaseModel

# App
from app.schemas import TradingTypeEnum


class LoanSchema(BaseModel):
    """Loan schema"""

    asset: str
    amount: float
    trading_type: TradingTypeEnum
