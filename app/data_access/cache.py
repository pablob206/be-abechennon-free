"""Cache data-access layer module"""

# Third-Party
from typing import Dict

# App
from app.config import redis_client


def clear_cache(db_redis: str) -> None:
    """
    Clear cache
    """

    redis_client.select(index=db_redis)
    redis_client.flushdb()


def set_klines_cache(
    name: str,
    mapping: Dict[bytes, bytes],
    db_redis: str,
) -> None:
    """
    Set klines cache
    """

    redis_client.select(index=db_redis)
    return redis_client.hmset(name=name, mapping=mapping)  # type: ignore


def get_klines_cache(
    name: str,
    db_redis: str,
) -> Dict[bytes, bytes]:
    """
    Get klines cache
    :return: dict[bytes, bytes], klines cache. I.e: {
        b'o': b'[0.1,0.2,0.3,0.4,0.5]',
        b'h': b'[0.1,0.2,0.3,0.4,0.5]',
        b'l': b'[0.1,0.2,0.3,0.4,0.5]',
        b'c': b'[0.1,0.2,0.3,0.4,0.5]',
        b'v': b'[0.1,0.2,0.3,0.4,0.5]'
    }
    """

    redis_client.select(index=db_redis)
    return redis_client.hgetall(name=name)
