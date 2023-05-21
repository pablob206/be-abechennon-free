"""Binance client module"""
# Third-party
from binance import AsyncClient  # type: ignore[attr-defined]

# App
from app.config import settings


class BinanceClient:
    """Binance client"""

    client: AsyncClient | None = None

    def __init__(self, **kwargs) -> None:
        self.options = kwargs
        self.client = None
        self.session = None

    async def start(self) -> None:
        """Start client"""
        if not self.client:
            self.client = await AsyncClient.create(
                api_key=settings.BINANCE_API_KEY,
                api_secret=settings.BINANCE_API_SECRET,
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
