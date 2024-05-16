"""Order models module"""
# Third-Party
from sqlalchemy import Boolean, Column, DateTime, Integer, String, func, BIGINT, Float, JSON
from sqlalchemy.orm import class_mapper

# App
from app.schemas import OrdStatusEnum
from config import Base


class Order(Base):
    """Order model"""

    __tablename__ = "orders"
    __table_args__ = {"schema": "be-abechennon-free"}

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True, index=True)
    pair = Column(String(55), nullable=False)
    trading_type = Column(String(55), nullable=False)
    order_id = Column(Integer, default=None, nullable=True)
    client_order_id = Column(String(155),default=None, nullable=True)
    transact_time = Column(BIGINT, nullable=True)
    price = Column(Float, default=None, nullable=True)
    limit_price = Column(Float, default=None, nullable=True)
    orig_qty = Column(Float, nullable=False)
    executed_qty = Column(Float, default=None, nullable=True)
    cummulative_quote_qty = Column(Float, default=None, nullable=True)
    status: OrdStatusEnum = Column(String, nullable=False)
    time_in_force = Column(String, default=None, nullable=True)
    ord_type = Column(String, nullable=False)
    side = Column(String, nullable=False)
    margin_buy_borrow_amount = Column(Float, default=None, nullable=True)
    margin_buy_borrow_asset = Column(String, default=None, nullable=True)
    is_isolated = Column(Boolean, default=False, nullable=False)
    fills = Column(JSON, default=None, nullable=True)
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    created_at = Column(DateTime, nullable=False, default=func.now())

    def as_dict(self) -> dict:
        """Return model instance as dict"""

        return {column.key: getattr(self, column.key) for column in class_mapper(self.__class__).mapped_table.columns}
