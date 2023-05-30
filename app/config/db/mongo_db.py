"""Config Mongo database instance"""
# Third-Party
from mongoengine import connect, disconnect  # pylint: disable=unused-import

# App
from app.config import settings


mongo_client = connect(
    db=settings.DB_MONGO,
    host=settings.HOST_MONGO,
    port=settings.PORT_MONGO,
    uuidRepresentation="standard",
)
