"""Config Redis instance"""
# Third-Party
from redis.asyncio import Redis  # type: ignore

# App
from app.config import settings


redis_client = Redis(
    db=settings.DB_REDIS,
    host=settings.HOST_REDIS,
    port=settings.PORT_REDIS,
)
