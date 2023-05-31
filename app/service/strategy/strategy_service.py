"""Strategy service module"""
# Built-In
from typing import Any, List, Dict, Union

# Third-Party
from fastapi import HTTPException
from mongoengine import DoesNotExist
from mongoengine import DynamicDocument

# App
from app.models import Strategies
from app.schemas import StrategyRequest
from app.data_access import (
    insert_document,
    get_document,
    get_all_document,
    delete_document,
)


async def add_strategy(
    strategy_req: StrategyRequest,
) -> Dict[str, Union[str, DynamicDocument]]:
    """
    Add strategy
    """

    try:
        await get_document(name=strategy_req.name, document=Strategies)
    except DoesNotExist:
        strategy = Strategies(
            name=strategy_req.name,
            description=strategy_req.description,
            data=[data.dict(exclude_unset=True) for data in strategy_req.data],
        )
        return await insert_document(document=strategy)
    raise HTTPException(
        status_code=400,
        detail=f"Strategy [{strategy_req.name}] already exists",
    )


async def get_strategy(
    _id: str | None = None, name: str | None = None
) -> Dict[str, Any]:
    """
    Get strategy
    """

    try:
        doc = await get_document(_id=_id, name=name, document=Strategies)
    except DoesNotExist as exc:
        raise HTTPException(
            status_code=404,
            detail=f"Strategy not found [{exc}]",
        ) from exc
    return {
        item: str(getattr(doc, item)) if item == "id" else getattr(doc, item)
        for item in doc._fields
        if getattr(doc, item)
    }


async def get_all_strategy() -> List[Dict[str, Any]]:
    """
    Get all strategy
    """

    try:
        strategy_list = await get_all_document(document=Strategies)
    except DoesNotExist as exc:
        raise HTTPException(
            status_code=404,
            detail=f"Strategy not found [{exc}]",
        ) from exc
    all_document = []
    for doc in strategy_list:
        doc_data = {
            item: str(getattr(doc, item)) if item == "id" else getattr(doc, item)
            for item in doc._fields
            if getattr(doc, item)
        }
        all_document.append(doc_data)
    return all_document


async def update_strategy(
    strategy_req: StrategyRequest, _id: str | None = None, name: str | None = None
) -> Dict[str, Union[str, DynamicDocument]]:
    """
    Update strategy
    """

    try:
        strategy_doc = await get_document(_id=_id, name=name, document=Strategies)
    except DoesNotExist as exc:
        raise HTTPException(
            status_code=404,
            detail=f"Strategy not found [{exc}]",
        ) from exc

    strategy_req_dict = strategy_req.dict(exclude_unset=True)
    for key, value in strategy_req_dict.items():
        setattr(strategy_doc, key, value)

    return await insert_document(document=strategy_doc)


async def delete_strategy(
    _id: str | None = None, name: str | None = None
) -> Dict[str, str]:
    """
    Delete strategy permanently by '_id'
    """

    try:
        await get_document(_id=_id, name=name, document=Strategies)
    except DoesNotExist as exc:
        raise HTTPException(
            status_code=404,
            detail=f"Strategy not found [{exc}]",
        ) from exc
    return await delete_document(document=Strategies, _id=_id, name=name)
