"""Config MySql database instance"""
# Built-In
from functools import wraps
from typing import AsyncGenerator

# Third-Party
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Field
from sqlmodel.ext.asyncio.session import AsyncSession

# App
from app.config import settings


sql_url = (
    settings.TYPE_MYSQL
    + "://"
    + settings.USER_MYSQL
    + ":"
    + settings.PASSWORD_MYSQL
    + "@"
    + settings.HOST_MYSQL
    + "/"
    + settings.DB_MYSQL
)

async_session = sessionmaker(
    create_async_engine(sql_url, future=True, echo=False),
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide a transactional scope around a series of operations.
    Generates a new session to be injected as a dependency.
    The context handler handles the commit or rollback, and closes the session
    """

    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
        finally:
            await session.close()


def set_default_index(func):
    """set default ddbb index"""

    @wraps(func)
    def inner(*args, index=False, **kwargs):
        return func(*args, index=index, **kwargs)

    return inner


Field = set_default_index(Field)
