"""Main app module"""

# Built-In
# Third-Party
import asyncio
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from app.api import api_router

# App
from app.config import get_cache_settings, settings
from app.service.binance import init_binance_websocket_engine

logger = logging.getLogger(name="WebSocketClient")


app = FastAPI(
    title=get_cache_settings().PROJECT_NAME,
    description=get_cache_settings().DESCRIPTION,
    version=get_cache_settings().PROJECT_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    default_response_class=ORJSONResponse,
    contact={
        "name": "Pablo Brocal",
        "email": "pablomb206@gmail.com",
    },
    lifespan=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in get_cache_settings().BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router=api_router, prefix=settings.API_V1_STR)


if __name__ == "main":
    asyncio.ensure_future(coro_or_future=init_binance_websocket_engine(cache_clear=True))
