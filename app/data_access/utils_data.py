"""Data access utilities module"""
# Built-In
from typing import TypeVar

# Third-Party
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

TypeModel = TypeVar("TypeModel", bound=SQLModel)


async def update_add_obj_query(
    item: TypeModel,
    db_session: AsyncSession,
) -> TypeModel:
    """
    Update or Add item model SQLModel
    """

    db_session.add(item)
    await db_session.flush()
    return item


async def delete_obj_query(
    item: TypeModel,
    db_session: AsyncSession,
) -> TypeModel:
    """
    Delete item model SQLModel
    """

    await db_session.delete(item)
    await db_session.flush()
    return item
