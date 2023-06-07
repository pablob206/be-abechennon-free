"""Order models module"""
# Built-In
from datetime import datetime
from typing import Dict, List, Any

# Third-Party
from sqlmodel import SQLModel, Field, Column, JSON, BIGINT

# App
from app.models import (
    OrdStatusEnum,
    TimeInForceEnum,
    SideEnum,
    OrdTypeEnum,
    TradingTypeEnum,
)


class Order(SQLModel, table=True):  # type: ignore
    """
    Order db model
    """

    __tablename__ = "orders"
    id: int = Field(primary_key=True, nullable=False)
    pair: str
    trading_type: TradingTypeEnum
    order_id: int | None = None
    client_order_id: str | None = None
    transact_time: int | None = Field(sa_column=Column(BIGINT))
    price: float | None = None
    limit_price: float | None = None
    orig_qty: float
    executed_qty: float | None = None
    cummulative_quote_qty: float | None = None
    status: OrdStatusEnum = OrdStatusEnum.NEW
    time_in_force: TimeInForceEnum | None = None
    ord_type: OrdTypeEnum
    side: SideEnum
    margin_buy_borrow_amount: float | None = None
    margin_buy_borrow_asset: str | None = None
    is_isolated: bool = False
    fills: List[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow}
    )

    class Config:
        """config"""

        arbitrary_types_allowed = True
