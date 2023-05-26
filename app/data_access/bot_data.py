"""Binance cache data-access layer module"""
# Third-Party
from typing import Dict

# App
from app.config import redis_client


async def clear_cache() -> None:
    """
    Clear cache
    """

    await redis_client.flushdb()


async def set_klines_cache(
    name: str,
    mapping: Dict[bytes, bytes],
) -> None:
    """
    Set klines cache
    """

    return await redis_client.hmset(name=name, mapping=mapping)


async def get_klines_cache(
    name: str,
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

    return await redis_client.hgetall(name=name)
