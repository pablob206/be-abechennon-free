"""Setting models module"""

# Third-Party
from mongoengine import DateTimeField, DictField, DynamicDocument, IntField, StringField
from sqlalchemy import JSON, Boolean, Column, DateTime, Float, Integer, String, func
from sqlalchemy.orm import class_mapper

# App
from app.config import Base


class Setting(Base):
    """Setting model"""

    __tablename__ = "settings"
    __table_args__ = {"schema": "be-abechennon-free"}

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True, index=True)
    binance_api_key = Column(String(255), nullable=False)
    binance_api_secret = Column(String(255), nullable=True)
    pairs = Column(JSON, nullable=False)
    trading_type = Column(String(255), nullable=True)
    order_type = Column(String(255), nullable=True)
    max_open_position = Column(Integer, nullable=True)
    max_open_position_per_coin = Column(Integer, nullable=True)
    currency_base = Column(String(255), nullable=True)
    amount_per_order = Column(Float, nullable=True)
    take_profit_at = Column(Float, nullable=True)
    enable_stop_loss = Column(Boolean, nullable=True)
    stop_loss = Column(Integer, nullable=True)
    enable_trailing_stop_loss = Column(Boolean, nullable=True)
    trailing_stop_loss = Column(Integer, nullable=True)
    time_frame = Column(String(255), nullable=True)
    is_real_time = Column(String(255), nullable=True)
    close_all_position = Column(Boolean, nullable=True)
    flag_back_testing = Column(Boolean, nullable=True)
    invert_signal = Column(Boolean, nullable=True)
    flag_on_magic = Column(Boolean, nullable=True)
    magic_amount = Column(Float, nullable=True)
    bot_status = Column(String(255), nullable=True)
    strategy_id = Column(String(255), nullable=True)
    strategy_name = Column(String(255), nullable=True)
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    created_at = Column(DateTime, nullable=False, default=func.now())

    def as_dict(self) -> dict:
        """Return model instance as dict"""

        return {column.key: getattr(self, column.key) for column in class_mapper(self.__class__).mapped_table.columns}


class MdLogs(DynamicDocument):
    """Logs by market-data"""

    eventType = StringField(max_length=200, required=True)
    eventTime = IntField(required=True)
    intervalKline = StringField(required=False)
    dateAt = DateTimeField(required=False)
    symbol = StringField(max_length=200, required=True)
    tick = DictField(required=False)

    class Config:
        """config"""

        arbitrary_types_allowed = True
