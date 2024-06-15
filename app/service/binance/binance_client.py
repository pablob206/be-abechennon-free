"""Binance client module"""

# Built-in
from functools import lru_cache
from typing import Any

# Third-party
from binance import AsyncClient

# App
from app.config import get_cache_settings


@lru_cache
def binance_client_cache() -> Any:
    """Get binance client cache"""

    return BinanceClient(
        binance_api_key=get_cache_settings().BINANCE_API_KEY,
        binance_api_secret=get_cache_settings().BINANCE_API_SECRET,
        requests_params={"timeout": get_cache_settings().BINANCE_REQUEST_TIMEOUT},
    )


class BinanceClient:
    """Binance client"""

    def __init__(self, **kwargs) -> None:  # type: ignore
        """Constructor"""

        self.options: dict = kwargs
        self.session = None
        self.client: AsyncClient | None = None

    async def start(self) -> None:
        """Start client"""

        if not self.client:
            self.client = await AsyncClient.create(
                api_key=self.options.get("binance_api_key"),
                api_secret=self.options.get("binance_api_secret"),
                requests_params=self.options.get("requests_params"),
            )

    async def stop(self) -> None:
        """Close client"""

        if self.client:
            await self.client.close_connection()
        self.session = None

    def __call__(self) -> AsyncClient:
        """Call client"""

        if not self.client:
            raise RuntimeError("Binance Client is not started")

        return self.client


binance_client = BinanceClient(
    binance_api_key=get_cache_settings().BINANCE_API_KEY,
    binance_api_secret=get_cache_settings().BINANCE_API_SECRET,
    requests_params={"timeout": get_cache_settings().BINANCE_REQUEST_TIMEOUT},
)
