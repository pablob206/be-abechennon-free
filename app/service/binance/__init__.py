"""Initialize binance layer modules"""
# App
from app.config import settings
from .binance_service import init_binance_websocket
from .binance_client import BinanceClient

binance_client = BinanceClient(
    binance_api_key=settings.BINANCE_API_KEY,
    binance_api_secret=settings.BINANCE_API_SECRET,
)
