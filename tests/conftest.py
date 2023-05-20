"""Test setup"""
# Built-In
from os import environ


def pytest_sessionstart() -> None:
    """
    Pytest session start
    """

    mock_envs = {
        "DB_TYPE": "mysql+aiomysql",
        "DB_IP": "localhost",
        "DB_USER": "root",
        "DB_PASSWORD": "password",
        "DB_NAME": "be-abechennon-free",
        "PORT": "3306",
        "MONGO_DB": "beAbechennonFree",
        "MONGO_HOST": "127.0.0.1",
        "MONGO_PORT": "27017",
        "KEY_AES_ENCRYPT": "1234567890123456",
        "SECRET_KEY": "a1s2",
    }
    environ.update(mock_envs)
