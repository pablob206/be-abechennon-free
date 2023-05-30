"""Strategies routes module"""
# Third-Party
from fastapi import APIRouter, status

# App
from app.service.strategy import (
    add_strategy,
    get_strategy,
    get_all_strategy,
    update_strategy,
    delete_strategy,
)
from app.schemas import StrategyRequest

router = APIRouter()


@router.post(
    path="/strategy", summary="Add strategy", status_code=status.HTTP_201_CREATED
)
async def _add_strategy(strategy_req: StrategyRequest):
    """
    Add strategy
    - **:Request body:** \n
            {
                "name": (str) strategy name. I.e: "Classic RSI strategy",
                "description": (str) strategy description. I.e: "This is a classic RSI strategy",
                "data": (list) strategy data. I.e: [
                    {
                        "name": "Relative Strength Index (RSI)",
                        "signal_type": "BUY",
                        "chartperiod": "900",
                        "candle_pattern": 0,
                        "necessary": True,
                        "keep_signal": "0",
                        "params": {
                            "candle_value": {
                                "type_": "select",
                                "name": "OHLCV Value",
                                ...
                            },
                            ...
                        },
                    },
                    {...},
                    {...}
                ]
            }
    - **:return:** dict, bot strategy. I.e: \n
            {
                "status": "success",
                "document": {
                    "_cls": "Strategies",
                    "_dynamic_lock": false
                }
            }
    """

    return await add_strategy(strategy_req=strategy_req)


@router.get(path="/strategy", summary="Get strategy", status_code=status.HTTP_200_OK)
async def _get_strategy(_id: str | None = None):
    """
    Get strategy by 'id' or 'last' record
    - **:return:** dict, bot strategy. I.e: \n
            {
                "name": "Classic RSI strategy",
                "description": "This is a classic RSI strategy (15m)",
                "createdAt": "2023-05-30T16:51:13.344000",
                "id": "6476298130c574e734a00b81",
                "data": [
                    {
                        "name": "Relative Strength Index (RSI)",
                        "signal_type": "BUY",
                        "chartperiod": "900",
                        "candle_pattern": false,
                        "necessary": true,
                        "keep_signal": 0,
                        "params": {
                            "period": {
                                "type_": "number",
                                "step": 1,
                                "min_": 1,
                                "max_": 500,
                                "name": "RSI Period",
                                "default": 14,
                                "value": 14
                            },
                            "candle_value": {
                                "type_": "select",
                                "name": "OHLCV Value",
                                "options": [
                                    "open",
                                    "close",
                                    "high",
                                    "low",
                                    "volume"
                                ],
                                "default": "close"
                            },
                            "signal_when": {
                                "type_": "value",
                                "signal_when": "<=",
                                "signal_when_value": 20,
                                "defaults": {
                                    "buy": {
                                        "signal_when": "<=",
                                        "signal_when_value": 20
                                    },
                                    "sell": {
                                        "signal_when": ">=",
                                        "signal_when_value": 80
                                    }
                                }
                            }
                        }
                    },
                    ...
                ]
            }
    """

    return await get_strategy(_id=_id)


@router.get(
    path="/strategy-list", summary="Get all strategy", status_code=status.HTTP_200_OK
)
async def _get_all_strategy():
    """
    Get all strategy
    - **:return:** dict, bot strategy. I.e: \n
            [
                {
                    "name": "Classic RSI strategy",
                    "description": "This is a classic RSI strategy (15m)",
                    "createdAt": "2023-05-30T16:51:13.344000",
                    "id": "6476298130c574e734a00b81",
                    "data": [
                        {
                            "name": "Relative Strength Index (RSI)",
                            "signal_type": "BUY",
                            "chartperiod": "900",
                            "candle_pattern": false,
                            "necessary": true,
                            "keep_signal": 0,
                            "params": {
                                "period": {
                                    "type_": "number",
                                    "step": 1,
                                    "min_": 1,
                                    "max_": 500,
                                    "name": "RSI Period",
                                    "default": 14,
                                    "value": 14
                                },
                                "candle_value": {
                                    "type_": "select",
                                    "name": "OHLCV Value",
                                    "options": [
                                        "open",
                                        "close",
                                        "high",
                                        "low",
                                        "volume"
                                    ],
                                    "default": "close"
                                },
                                "signal_when": {
                                    "type_": "value",
                                    "signal_when": "<=",
                                    "signal_when_value": 20,
                                    "defaults": {
                                        "buy": {
                                            "signal_when": "<=",
                                            "signal_when_value": 20
                                        },
                                        "sell": {
                                            "signal_when": ">=",
                                            "signal_when_value": 80
                                        }
                                    }
                                }
                            },
                            ...
                        },
                        {...},
                        {...}
                    ]
                }
            ]
    """

    return await get_all_strategy()


@router.patch(
    path="/strategy",
    summary="Update partial strategy",
    status_code=status.HTTP_200_OK,
)
async def _update_strategy(
    _id: str,
    strategy_req: StrategyRequest,
):
    """
    Update strategy by 'id'
    - **:param _id:** str, strategy id. I.e: "6476298130c574e734a00b81"
    - **:return:** dict, update strategy. I.e: \n
            {
                "status": "success",
                "document": {
                    "_cls": "Strategies",
                    "_dynamic_lock": false
                }
            }
    """

    return await update_strategy(_id=_id, strategy_req=strategy_req)


@router.delete(
    path="/strategy",
    summary="Delete strategy permanently",
    status_code=status.HTTP_200_OK,
)
async def _delete_strategy(_id: str):
    """
    Delete strategy permanently by 'id'
    - **:param _id:** str, strategy id. I.e: "6476377060fe99e210eb2fa6"
    - **:return:** dict, item deleted. I.e: \n
            {
                "status": "deleted",
                "id": "6476377060fe99e210eb2fa6"
            }
    """

    return await delete_strategy(_id=_id)
