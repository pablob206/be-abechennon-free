"""Binance client routes"""
# Third-Party
from fastapi import APIRouter, Depends

# App
from app.service.binance import (
    binance_client,
    initialize_ws_binance_client,
)

router = APIRouter()


@router.post(path="/binance/initialize")
async def binance(initialize_ws=Depends(initialize_ws_binance_client)):
    """
    initialize binance websocket
    """

    return initialize_ws


@router.get(path="/binance/balance")
async def _get_binance_balance():
    """
    Get binance balance
    """

    client = binance_client.__call__()
    return await client.get_exchange_info()
