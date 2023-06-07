"""Strategy service module"""
# Built-In
from typing import Any, List, Dict, Union

# Third-Party
from fastapi import HTTPException
from mongoengine import DoesNotExist
from mongoengine import DynamicDocument
import numpy as np
import talib as ta
import orjson

# App
from app.models import Strategies, Setting, SideEnum
from app.schemas import StrategyRequest
from app.data_access import (
    insert_document,
    get_document,
    get_all_document,
    delete_document,
    get_klines_cache,
)
from app.config import settings


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


async def strategy_temp(pair: str, setting_db: Setting):
    """
    A temporal 'hard-coded' strategy with RSI to testing (todo remove)
    """

    strategy_data: dict = await get_strategy(_id=setting_db.strategy_id)
    tick_cache_bytes = get_klines_cache(
        name=f"{pair}_{setting_db.time_frame}", db_redis=settings.DB_REDIS_KLINES
    )
    tick_cache = {
        key.decode("utf-8"): orjson.loads(value)
        for key, value in tick_cache_bytes.items()
    }

    close_list = np.array(tick_cache["c"])
    indicators_results_list = ta.RSI(close_list, 14)

    signal = None
    mapping = {"BUY": None, "SELL": None}

    for item in strategy_data["data"]:
        signal_type = item["signal_type"]
        signal_when_value = item["params"]["signal_when"]["signal_when_value"]
        if signal_type in mapping:
            mapping[signal_type] = signal_when_value

    indicators_results = indicators_results_list[-1]
    if indicators_results <= mapping["BUY"]:
        signal = SideEnum.BUY
    elif indicators_results >= mapping["SELL"]:
        signal = SideEnum.SELL

    return signal
