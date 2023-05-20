"""Settings schemas module"""
# Built-In
from datetime import datetime

# Third-Party
from pydantic import BaseModel, Field


class SettingsBase(BaseModel):
    """Settings base"""

    binance_api_key: str = Field(None, title="Binance API Key")
    binance_api_secret: str = Field(None, title="Binance API Secret")
    pairs_list: list = Field(None, title="Pairs List")
    order_type: str = Field(None, title="Order Type")
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
    created_at: datetime = Field(None, title="Created At")
    updated_at: datetime = Field(None, title="Updated At")


class SettingsSchema(SettingsBase):
    """Settings schema"""

    id: int


class SettingsRequest(SettingsBase):
    """Settings request"""

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
                "pairs_list": [
                    "adausdt",
                    "ethusdt",
                    "etcusdt",
                    "btcusdt",
                    "bnbusdt",
                    "iotausdt",
                    "xlmusdt",
                    "xrpusdt",
                    "ltcusdt",
                    "solusdt",
                ],
                "order_type": None,
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
            }
        }
