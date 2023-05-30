"""Strategy service module"""
# Third-Party
from fastapi import HTTPException
from mongoengine import DoesNotExist

# App
from app.models import Strategies
from app.schemas import StrategyRequest
from app.data_access import (
    insert_document,
    get_document,
    get_all_document,
    delete_document,
)


async def add_strategy(strategy_req: StrategyRequest):
    """
    Add strategy
    """

    strategy = Strategies(
        name=strategy_req.name,
        description=strategy_req.description,
        data=[data.dict(exclude_unset=True) for data in strategy_req.data],
    )
    return await insert_document(document=strategy)


async def get_strategy(_id: str | None = None):
    """
    Get strategy
    """

    try:
        doc = await get_document(_id=_id, document=Strategies)
    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Strategy not found",
        )
    return {
        item: str(getattr(doc, item)) if item == "id" else getattr(doc, item)
        for item in doc._fields
        if getattr(doc, item)
    }


async def get_all_strategy():
    """
    Get all strategy
    """

    try:
        strategy_list = await get_all_document(document=Strategies)
    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Strategy not found",
        )
    all_document = []
    for doc in strategy_list:
        doc_data = {
            item: str(getattr(doc, item)) if item == "id" else getattr(doc, item)
            for item in doc._fields
            if getattr(doc, item)
        }
        all_document.append(doc_data)
    return all_document


async def update_strategy(_id: int, strategy_req: StrategyRequest):
    """
    Update strategy
    """

    try:
        strategy_doc = await get_document(_id=_id, document=Strategies)
    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Strategy not found",
        )

    strategy_req_dict = strategy_req.dict(exclude_unset=True)
    for key, value in strategy_req_dict.items():
        setattr(strategy_doc, key, value)

    return await insert_document(document=strategy_doc)


async def delete_strategy(_id: str):
    """
    Delete strategy permanently by '_id'
    """

    try:
        await get_document(_id=_id, document=Strategies)
    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Strategy not found",
        )
    return await delete_document(document=Strategies, _id=_id)
