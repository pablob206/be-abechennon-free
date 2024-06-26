"""Config Mongo database instance"""

# Third-Party
from mongoengine import connect, disconnect  # pylint: disable=unused-import # noqa: imported but unused

# App
from app.config.settings import get_cache_settings

mongo_client = connect(
    db=get_cache_settings().DB_MONGO,
    host=get_cache_settings().HOST_MONGO,
    port=get_cache_settings().PORT_MONGO,
    uuidRepresentation="standard",
)
