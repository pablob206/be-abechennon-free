"""Loan models module"""
# Third-Party
from sqlalchemy import Column, DateTime, Integer, String, func, FLOAT, BIGINT
from sqlalchemy.orm import class_mapper

# App
from config import Base
from models import LoanStatusEnum


class Loan(Base):
    """Loan model"""

    __tablename__ = "loans"
    __table_args__ = {"schema": "be-abechennon-free"}

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True, index=True)
    asset = Column(String(255), nullable=False)
    amount = Column(FLOAT, nullable=False)
    trading_type = Column(String(150), nullable=False)
    loan_operation_type = Column(String(150), nullable=False)
    status = Column(String(150), default=LoanStatusEnum.PENDING, nullable=False)
    tran_id = Column(BIGINT, default=None, nullable=True)
    client_tag = Column(String(150), default=None, nullable=True)
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    created_at = Column(DateTime, nullable=False, default=func.now())

    def as_dict(self) -> dict:
        """Return model instance as dict"""

        return {column.key: getattr(self, column.key) for column in class_mapper(self.__class__).mapped_table.columns}
