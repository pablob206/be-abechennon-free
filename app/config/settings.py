"""Settings module"""
# Built-In
from typing import List

# Third-Party
from pydantic import BaseSettings, AnyHttpUrl


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

    DB_TYPE: str = "mysql+aiomysql"
    DB_IP: str = "localhost"
    DB_USER: str = "root"
    DB_PASSWORD: str | None
    DB_NAME: str = "abechennon-free"
    PORT: int = 3306

    MONGO_DB: str
    MONGO_HOST: str
    MONGO_PORT: int

    class Config:
        """Config class Pydantic"""

        env_file = ".env"
        env_file_encoding = "utf-8"
        arbitrary_types_allowed = True


settings = Settings()
