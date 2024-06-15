"""Data access utilities module"""

# Built-In
from typing import Dict, List, TypeVar, Union

from mongoengine import DynamicDocument

# Third-Party
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

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
    await db_session.commit()
    return item


async def delete_obj_query(
    item: TypeModel,
    db_session: AsyncSession,
) -> TypeModel:
    """
    Delete item model SQLModel (MySql)
    """

    await db_session.delete(item)
    await db_session.commit()
    return item


async def insert_document(
    document: DynamicDocument,
) -> Dict[str, Union[str, DynamicDocument]]:
    """
    Insert document (Mongo DB)
    """

    document.save()
    return {"status": "success", "document": document}


async def get_document(document: DynamicDocument, _id: str | None = None, name: str | None = None) -> Strategies:
    """
    Get document by '_id' or 'name' or last record (Mongo DB)
    """

    if _id and not name:
        return document.objects.get(id=_id)
    if not _id and name:
        return document.objects.get(name=name)
    return document.objects().order_by("-_id").first()


async def get_all_document(document: DynamicDocument) -> List[Strategies]:
    """
    Get all document (Mongo DB)
    """

    return document.objects().all()


async def delete_document(document: DynamicDocument, _id: str | None = None, name: str | None = None) -> Dict[str, str]:
    """
    Delete document permanently by '_id' or 'name' (Mongo DB)
    """

    if _id and not name:
        document.objects(id=_id).delete()
        return {"status": "deleted", "id": _id}
    if not _id and name:
        document.objects(name=name).delete()
        return {"status": "deleted", "name": name}
    raise ValueError("You must specify '_id' or 'name' parameter")
