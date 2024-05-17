"""Settings module"""

# Built-In
from functools import lru_cache
from typing import Any, List, Union

# Third-Party
from pydantic import AnyHttpUrl, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL  # type: ignore

# App
from app.schemas import AppStatusEnum


@lru_cache
def get_cache_settings() -> Any:
    """Get cache settings"""

    return Settings()


class Settings(BaseSettings):
    """Get Settings from env file or env variables"""

    API_V1_STR: str = "/api/v1"

    DEBUG: bool = False

    PROJECT_NAME: str = "Abechennon Free Backend [ CORE ]"
    PROJECT_VERSION: str = "0.1.0"
    DESCRIPTION: str | None = "Margin trading bot backend for Binance"

    BACKEND_CORS_ORIGINS: List[Union[AnyHttpUrl, str]] | None = ["http://127.0.0.1:8000", "http://localhost:5173", "*"]

    APP_STATUS: str = AppStatusEnum.RUNNING

    # -----MYSQL-----
    TYPE_MYSQL: str = "mysql+aiomysql"
    DB_MYSQL: str = "be-abechennon-free"
    HOST_MYSQL: str = "localhost"
    PORT_MYSQL: int = 3306
    USER_MYSQL: str
    PASSWORD_MYSQL: str
    SQL_URL: str | URL = None  # Do not fill

    DB_MONGO: str
    HOST_MONGO: str
    PORT_MONGO: int = 27017
    USER_MONGO: str | None
    PASSWORD_MONGO: str | None

    DB_REDIS_KLINES: str
    HOST_REDIS: str
    PORT_REDIS: int | None = 6379
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

    @field_validator("SQL_URL", mode="before")
    @classmethod
    def sql_url(cls, value: str | URL | None, info: ValidationInfo) -> str | URL:
        """Create sql-url for sqlalchemy"""

        if value:
            return value
        return URL.create(
            drivername=info.data["TYPE_MYSQL"],
            username=info.data["USER_MYSQL"],
            password=info.data["PASSWORD_MYSQL"],
            host=info.data["HOST_MYSQL"],
            port=info.data["PORT_MYSQL"],
            database=info.data["DB_MYSQL"],
        )

    # -----SettingsConfigDict-----
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf8",
        arbitrary_types_allowed=True,
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
