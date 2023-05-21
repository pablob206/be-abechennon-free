"""Initialize binance layer modules"""
# App
from .binance_service import initialize_ws_binance_client
from .binance_client import BinanceClient

binance_client = BinanceClient()
