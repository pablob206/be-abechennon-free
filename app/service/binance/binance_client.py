"""Binance client module"""
# Third-party
from binance import AsyncClient  # type: ignore[attr-defined]


class BinanceClient:
    """Binance client"""

    def __init__(self, **kwargs) -> None:
        self.options: dict = kwargs
        self.session = None
        self.client: AsyncClient | None = None

    async def start(self) -> None:
        """Start client"""
        if not self.client:
            self.client = await AsyncClient.create(
                api_key=self.options.get("binance_api_key"),
                api_secret=self.options.get("binance_api_secret"),
                requests_params={"timeout": 20},
            )

    async def stop(self) -> None:
        """Close client"""
        if self.client:
            await self.client.close_connection()
        self.session = None

    def __call__(self) -> AsyncClient:
        if not self.client:
            raise RuntimeError("Binance Client is not started")
        return self.client
