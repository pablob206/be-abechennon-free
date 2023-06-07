"""Setting schemas module"""
# Built-In
from datetime import datetime

# Third-Party
from pydantic import BaseModel, Field

# App
from app.models import BotStatusEnum, TradingTypeEnum, OrdTypeEnum


class SettingBase(BaseModel):
    """Setting base"""

    binance_api_key: str = Field(None, title="Binance API Key")
    binance_api_secret: str = Field(None, title="Binance API Secret")
    pairs: list = Field(None, title="Pairs")
    trading_type: TradingTypeEnum = Field(None, title="Trading Type")
    order_type: OrdTypeEnum = Field(None, title="Order Type")
    max_open_position: int = Field(None, title="Max Open Position")
    max_open_position_per_coin: int = Field(None, title="Max Open Position Per Coin")
    currency_base: str = Field(None, title="Currency Base")
    amount_per_order: float = Field(None, title="Amount Per Order")
    take_profit_at: float = Field(None, title="Take Profit At")
    enable_stop_loss: bool = Field(None, title="Enable Stop Loss")
    stop_loss: int = Field(None, title="Stop Loss")
    enable_trailing_stop_loss: bool = Field(None, title="Enable Trailing Stop Loss")
    trailing_stop_loss: int = Field(None, title="Trailing Stop Loss")
    time_frame: str = Field(None, title="Time Frame")
    is_real_time: str = Field(None, title="Is Real Time")
    close_all_position: bool = Field(None, title="Close All Position")
    flag_back_testing: bool = Field(None, title="Flag Back Testing")
    invert_signal: bool = Field(None, title="Invert Signal")
    flag_on_magic: bool = Field(None, title="Flag On Magic")
    magic_amount: float = Field(None, title="Magic Amount")
    bot_status: BotStatusEnum = Field(None, title="Bot Status")
    strategy_id: str = Field(None, title="Strategy ID")
    strategy_name: str = Field(None, title="Strategy Name")
    created_at: datetime = Field(None, title="Created At")
    updated_at: datetime = Field(None, title="Updated At")


class SettingSchema(SettingBase):
    """Setting schema"""

    id: int


class SettingRequest(SettingBase):
    """Setting request"""

    class Config:
        """Config request schema"""

        fields = {
            "created_at": {"exclude": True},
            "updated_at": {"exclude": True},
        }
        schema_extra = {
            "example": {
                "binance_api_key": "gak3ojhK3kNHg4UIU11I",
                "binance_api_secret": "gak3ojhK3kNHg4UIU11I",
                "pairs": [
                    "XLMUSDT",
                    "NEOUSDT",
                    "UNIUSDT",
                    "CRVUSDT",
                    "COMPUSDT",
                    "DOTUSDT",
                    "IOTAUSDT",
                    "THETAUSDT",
                    "ALGOUSDT",
                    "1INCHUSDT",
                ],
                "trading_type": "MARGIN",
                "order_type": "MARKET",
                "max_open_position": 20,
                "max_open_position_per_coin": 3,
                "currency_base": "USDT",
                "amount_per_order": 33.33,
                "take_profit_at": 33.33,
                "enable_stop_loss": True,
                "stop_loss": 10,
                "enable_trailing_stop_loss": True,
                "trailing_stop_loss": 10,
                "time_frame": "15m",
                "is_real_time": "",
                "close_all_position": True,
                "flag_back_testing": False,
                "invert_signal": False,
                "flag_on_magic": False,
                "magic_amount": 100.0,
                "bot_status": "RUNNING",
                "strategy_id": "64772fa930e6d90f266ce7ad",
                "strategy_name": "Classic RSI strategy",
            }
        }
