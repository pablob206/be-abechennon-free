"""Main app module"""
# Built-In
import logging

# Third-Party
import asyncio
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware

# App
from app.config import settings
from app.api import api_router
from app.service.binance import init_binance_websocket_engine

logger = logging.getLogger("WebSocketClient")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    default_response_class=ORJSONResponse,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router, prefix=settings.API_V1_STR)


def main(loop_is_running: bool | None = False) -> None:
    """Main function to initialize websocket"""

    try:
        if not loop_is_running:
            asyncio.run(init_binance_websocket_engine(cache_clear=True))
        else:
            asyncio.create_task(init_binance_websocket_engine(cache_clear=True))
    except KeyboardInterrupt:
        logger.info("exiting...")


if __name__ == "main":
    loop = asyncio.get_event_loop()
    main(loop_is_running=loop.is_running())
