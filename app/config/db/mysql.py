"""Config MySql database instance"""

# Built-In
from functools import wraps
from typing import Any, AsyncGenerator

from pydantic import Field
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession

# Third-Party
from sqlalchemy.orm import sessionmaker

# App
from app.config.settings import get_cache_settings

sql_url = (
    get_cache_settings().TYPE_MYSQL
    + "://"
    + get_cache_settings().USER_MYSQL
    + ":"
    + get_cache_settings().PASSWORD_MYSQL
    + "@"
    + get_cache_settings().HOST_MYSQL
    + "/"
    + get_cache_settings().DB_MYSQL
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
        except:  # noqa
            await session.rollback()
            raise
        finally:
            await session.close()


def set_default_index(func) -> Any:  # type: ignore
    """set default ddbb index"""

    @wraps(func)
    def inner(*args, index=False, **kwargs) -> Any:  # type: ignore
        """Inner function"""

        return func(*args, index=index, **kwargs)

    return inner


Field = set_default_index(func=Field)
