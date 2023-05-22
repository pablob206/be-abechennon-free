"""Binance client routes"""
# Third-Party
from fastapi import APIRouter

# App
from app.service.binance import (
    binance_client,
    init_binance_websocket,
)

router = APIRouter()


@router.post(path="/binance/initialize")
async def binance():
    """
    initialize binance websocket
    """

    return await init_binance_websocket()


@router.get(path="/binance/balance")
async def _get_binance_balance():
    """
    Get binance balance
    """

    client = binance_client()
    return await client.get_exchange_info()
