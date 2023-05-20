"""Binance client routes"""
# Third-Party
from fastapi import APIRouter

# App
from app.service.binance import (
    binance_client,
    initialize_ws_binance_client,
)
from app.api import DBSessionDep

router = APIRouter()


@router.post(path="/binance/initialize")
async def binance(db_session: DBSessionDep, _id: int | None = 1):
    """
    initialize binance websocket
    """

    return initialize_ws_binance_client(db_session=db_session, _id=_id)


@router.get(path="/binance/balance")
async def _get_binance_balance():
    """
    Get binance balance
    """

    client = binance_client()
    return await client.get_exchange_info()
