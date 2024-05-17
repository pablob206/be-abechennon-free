"""Test setup"""

# Built-In
from os import environ


def pytest_sessionstart() -> None:
    """
    Pytest session start
    """

    mock_envs = {
        "APP_STATUS": "RUNNING",
        "TYPE_MYSQL": "mysql+aiomysql",
        "DB_MYSQL": "abechennon-free",
        "HOST__MYSQL": "localhost",
        "PORT_MYSQL": "3306",
        "USER_MYSQL": "root",
        "PASSWORD_MYSQL": "PASSWORD_MYSQL",
        "DB_MONGO": "beAbechennonFree",
        "HOST_MONGO": "127.0.0.1",
        "PORT_MONGO": "27017",
        "USER_MONGO": "root",
        "PASSWORD_MONGO": "PASSWORD_MONGO",
        "DB_REDIS_KLINES": "0",
        "HOST_REDIS": "127.0.0.1",
        "PORT_REDIS": "6379",
        "USER_REDIS": "root",
        "PASSWORD_REDIS": "PASSWORD_REDIS",
        "SECRET_KEY": "a1s2",
        "KEY_AES": "1234567890123456",
        "BINANCE_API_KEY": "3286omTJA9wS3TTp6KdgL",
        "BINANCE_API_SECRET": "GRfQ6vINzIgFpeLrqH2mEIPN",
        "BINANCE_REQUEST_TIMEOUT": "20",
        "BINANCE_SOCKET_NAME": '["kline"]',
        "BINANCE_SOCKET_INTERVAL": '["1m", "5m", "15m"]',
        "BINANCE_CACHE_LIMIT": "500",
    }
    environ.update(mock_envs)
