"""Loan request schemas module"""

# Third-Party
from pydantic import BaseModel

# App
from app.schemas import TradingTypeEnum


class LoanRequest(BaseModel):
    """Loan request schema"""

    asset: str
    amount: float
    trading_type: TradingTypeEnum
