"""Main app module"""
# Third-Party
import asyncio
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware

# App
from app.config import settings
from app.api import api_router
from app.service.binance import init_binance_websocket_engine, binance_client


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


if __name__ == "main":
    asyncio.ensure_future(binance_client.start())
    asyncio.ensure_future(init_binance_websocket_engine())
