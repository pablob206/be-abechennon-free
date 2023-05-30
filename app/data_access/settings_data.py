"""Settings data-access layer module"""
# Built-In
from typing import Union, TypeVar

# Third-Party
from sqlmodel import SQLModel, select, delete, update, desc
from sqlmodel.ext.asyncio.session import AsyncSession

# App
from app.models import Settings
from app.config import async_session

TypeModel = TypeVar("TypeModel", bound=SQLModel)


async def get_settings_query(
    _id: int | None = None, db_session: AsyncSession | None = None
) -> Settings | None:
    """
    Get settings
    """

    query = select(Settings).where(Settings.id == _id)
    if not _id:
        query = select(Settings).order_by(desc(Settings.id)).limit(1)
    if not db_session:
        async with async_session.begin() as db_session:
            pass

    result = await db_session.exec(query)
    await db_session.close()
    return result.one_or_none()


async def delete_settings_query(
    _id: int,
    db_session: AsyncSession,
) -> dict[str, Union[str, int]]:
    """
    Delete settings query
    """

    query = delete(Settings).where(Settings.id == _id)
    await db_session.exec(query)
    return {
        "delete": "success",
        "id": _id,
    }


async def update_settings_query(
    _id: int,
    settings: Settings,
    db_session: AsyncSession,
) -> Settings:
    """
    Update settings query
    """

    query = update(Settings).where(Settings.id == _id).values(**settings.dict())
    await db_session.exec(query)
    return settings
