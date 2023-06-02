"""Config Redis instance"""
# Third-Party
import redis  # type: ignore

# App
from app.config import settings


redis_client = redis.Redis(
    host=settings.HOST_REDIS,
    port=settings.PORT_REDIS,
)
