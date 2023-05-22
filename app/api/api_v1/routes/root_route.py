"""Root routes module"""
# Built-In
from typing import Dict

# Third-Party
from fastapi import APIRouter, status

# App
from app.config import settings
from app.service.binance import binance_client
from app.config import disconnect

router = APIRouter()


@router.on_event(event_type="startup")
async def startup_event() -> None:
    """
    On startup
    """

    await binance_client.start()
    print("Welcome to the jungle! \nStart, Abechennon-Free")


@router.on_event(event_type="shutdown")
async def shutdown_event() -> None:
    """
    On shutdown
    """

    await binance_client.stop()
    disconnect()
    print("Bye! \nShutdown, Abechennon-Free")


@router.get(path="/", summary="Root", status_code=status.HTTP_200_OK)
async def root() -> Dict[str, str]:
    """
    Return api information
    - **return:** dict, api information. I.e: \n
            {
                "project": "Abechennon Free Backend [ CORE ]",
                "version": "0.1.0"
            }
    """

    return {"project": settings.PROJECT_NAME, "version": settings.PROJECT_VERSION}
