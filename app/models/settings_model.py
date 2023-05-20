"""Settings models module"""
# Built-In
from enum import Enum
from datetime import datetime

# Third-Party
from mongoengine import (
    StringField,
    DynamicDocument,
    IntField,
    DictField,
    DateTimeField,
)
from sqlalchemy import Column
from sqlmodel import SQLModel, Field, JSON


class SettingsStatusEnum(str, Enum):
    """
    Define different settings status enum
    """

    BASIC = "basic"
    PARTIAL = "partial"
    FULL = "full"


class Settings(SQLModel, table=True):
    """
    Settings db model
    """

    id: int = Field(primary_key=True, nullable=False)
    binance_api_key: str | None = None
    binance_api_secret: str | None = None
    pairs_list: list = Field(sa_column=Column(JSON))
    order_type: str | None = None
    max_open_position: int | None = None
    max_open_position_per_coin: int | None = None
    currency_base: str | None = None
    amount_per_order: float | None = None
    take_profit_at: float | None = None
    enable_stop_loss: bool | None = None
    stop_loss: int | None = None
    enable_trailing_stop_loss: bool | None = None
    trailing_stop_loss: int | None = None
    time_frame: str | None = None
    is_real_time: str | None = None
    close_all_position: bool | None = None
    flag_back_testing: bool | None = None
    invert_signal: bool | None = None
    flag_on_magic: bool | None = None
    magic_amount: float | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow}
    )

    class Config:
        arbitrary_types_allowed = True


class MdLogs(DynamicDocument):
    """Logs by market-data"""

    eventType = StringField(max_length=200, required=True)
    eventTime = IntField(required=True)
    intervalKline = StringField(required=False)
    dateAt = DateTimeField(required=False)
    symbol = StringField(max_length=200, required=True)
    ticks = DictField(required=False)

    class Config:
        """config"""

        arbitrary_types_allowed = True
