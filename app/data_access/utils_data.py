"""Data access utilities module"""
# Built-In
from typing import TypeVar, Dict, List, Union

# Third-Party
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from mongoengine import DynamicDocument

# App
from app.models import Strategies

TypeModel = TypeVar("TypeModel", bound=SQLModel)


async def update_add_obj_query(
    item: TypeModel,
    db_session: AsyncSession,
) -> TypeModel:
    """
    Update or Add item model SQLModel (MySql)
    """

    db_session.add(item)
    await db_session.flush()
    return item


async def delete_obj_query(
    item: TypeModel,
    db_session: AsyncSession,
) -> TypeModel:
    """
    Delete item model SQLModel (MySql)
    """

    await db_session.delete(item)
    await db_session.flush()
    return item


async def insert_document(
    document: DynamicDocument,
) -> Dict[str, Union[str, DynamicDocument]]:
    """
    Insert document (Mongo DB)
    """

    document.save()
    return {"status": "success", "document": document}


async def get_document(document: DynamicDocument, _id: str | None = None) -> Strategies:
    """
    Get document by '_id' or by last record (Mongo DB)
    """

    if not _id:
        return document.objects().order_by("-_id").first()
    return document.objects.get(id=_id)


async def get_all_document(document: DynamicDocument) -> List[Strategies]:
    """
    Get all document (Mongo DB)
    """

    return document.objects().all()


async def delete_document(document: DynamicDocument, _id: str) -> Dict[str, str]:
    """
    Delete document permanently by '_id' (Mongo DB)
    """

    document.objects(id=_id).delete()
    return {"status": "deleted", "id": _id}
