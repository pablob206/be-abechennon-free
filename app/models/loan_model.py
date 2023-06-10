"""Loan models module"""
# Built-In
from datetime import datetime

# Third-Party
from sqlmodel import SQLModel, Field, Column, BIGINT

# App
from app.models import (
    TradingTypeEnum,
    LoanOperationTypeEnum,
    LoanStatusEnum,
)


class Loan(SQLModel, table=True):  # type: ignore
    """
    Loan db model
    """

    __tablename__ = "loans"
    id: int = Field(primary_key=True, nullable=False)
    asset: str
    amount: float
    trading_type: TradingTypeEnum
    loan_operation_type: LoanOperationTypeEnum
    status: LoanStatusEnum = LoanStatusEnum.PENDING
    tran_id: int | None = Field(sa_column=Column(BIGINT))
    client_tag: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow}
    )

    class Config:
        """config"""

        arbitrary_types_allowed = True
