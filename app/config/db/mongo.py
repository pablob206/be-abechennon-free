"""Config Mongo database instance"""
# Third-Party
from mongoengine import connect, disconnect  # pylint: disable=unused-import

# App
from app.config import settings


conn = connect(
    db=settings.MONGO_DB,
    host=settings.MONGO_HOST,
    port=settings.MONGO_PORT,
    uuidRepresentation="standard",
)
