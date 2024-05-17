"""Setting data-access layer module"""

# Built-In
from typing import Union, TypeVar

# Third-Party
from sqlmodel import SQLModel, select, delete, update, desc
from sqlmodel.ext.asyncio.session import AsyncSession

# App
from app.models import Setting
from app.config import async_session

TypeModel = TypeVar("TypeModel", bound=SQLModel)


async def get_setting_query(_id: int | None = None, db_session: AsyncSession | None = None) -> Setting | None:
    """
    Get setting
    """

    query = select(Setting).where(Setting.id == _id)
    if not _id:
        query = select(Setting).order_by(desc(Setting.id)).limit(1)
    if not db_session:
        async with async_session.begin() as db_session:
            pass

    result = await db_session.execute(query)
    await db_session.close()
    return result.one_or_none()


async def delete_setting_query(
    _id: int,
    db_session: AsyncSession,
) -> dict[str, Union[str, int]]:
    """
    Delete setting query
    """

    query = delete(Setting).where(Setting.id == _id)
    await db_session.exec(query)
    return {
        "delete": "success",
        "id": _id,
    }


async def update_setting_query(
    _id: int,
    setting: Setting,
    db_session: AsyncSession,
) -> Setting:
    """
    Update setting query
    """

    query = update(Setting).where(Setting.id == _id).values(**setting.dict())
    await db_session.exec(query)
    return setting
