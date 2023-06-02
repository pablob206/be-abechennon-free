"""Settings module"""
# Built-In
from typing import List

# Third-Party
from pydantic import BaseSettings, AnyHttpUrl
from app.models import AppStatusEnum


class Settings(BaseSettings):
    """Get Settings from env file or env variables"""

    API_V1_STR: str = "/api/v1"

    DEBUG: bool = False

    PROJECT_NAME: str = "Abechennon Free Backend [ CORE ]"
    PROJECT_VERSION: str = "0.1.0"

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://127.0.0.1:8000",
        "http://localhost:5173",
    ]

    APP_STATUS: str = AppStatusEnum.RUNNING

    TYPE_MYSQL: str = "mysql+aiomysql"
    DB_MYSQL: str = "abechennon-free"
    HOST_MYSQL: str = "localhost"
    PORT_MYSQL: int = 3306
    USER_MYSQL: str = "root"
    PASSWORD_MYSQL: str | None

    DB_MONGO: str
    HOST_MONGO: str
    PORT_MONGO: int = 27017
    USER_MONGO: str | None
    PASSWORD_MONGO: str | None

    DB_REDIS_KLINES: str
    HOST_REDIS: str
    PORT_REDIS: int = 6379
    USER_REDIS: str | None
    PASSWORD_REDIS: str | None

    SECRET_KEY: str
    KEY_AES: str

    BINANCE_API_KEY: str
    BINANCE_API_SECRET: str
    BINANCE_REQUEST_TIMEOUT: int = 20
    BINANCE_SOCKET_NAME: list = ["kline"]
    BINANCE_SOCKET_INTERVAL: list = ["1m", "5m", "15m"]
    BINANCE_CACHE_LIMIT: int = 500

    class Config:
        """Config class Pydantic"""

        env_file = ".env"
        env_file_encoding = "utf-8"
        arbitrary_types_allowed = True


settings = Settings()
