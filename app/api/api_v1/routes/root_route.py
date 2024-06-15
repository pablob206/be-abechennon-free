"""Root routes module v1"""

# Built-In
from typing import Dict

# Third-Party
from fastapi import APIRouter, status

# App
from app.config import async_session, disconnect, get_cache_settings
from app.service import binance_client

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
    async with async_session.begin() as db_session:  # type: ignore
        await db_session.close()
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

    return {"project": get_cache_settings().PROJECT_NAME, "version": get_cache_settings().PROJECT_VERSION}
