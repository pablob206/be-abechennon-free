"""Config Redis instance"""

# Third-Party
import redis  # type: ignore

# App
from app.config import get_cache_settings


redis_client = redis.Redis(
    host=get_cache_settings().HOST_REDIS,
    port=get_cache_settings().PORT_REDIS,
)
