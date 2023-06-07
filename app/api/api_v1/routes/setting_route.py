"""Setting routes module"""
# Built-In
from typing import Dict, List, Union

# Third-Party
from fastapi import APIRouter, status

# App
from app.service.setting import (
    get_setting_status,
    get_setting,
    update_setting,
    add_setting,
    delete_setting,
)
from app.schemas import SettingSchema, SettingRequest
from app.api import DBSessionDep

router = APIRouter()


@router.get(
    path="/setting/status",
    summary="Setting status",
    response_model=Dict[str, Union[str, List[str]]],
    status_code=status.HTTP_200_OK,
)
async def _get_setting_status(db_session: DBSessionDep, _id: int | None = None):
    """
    Get setting status by _id, or last setting (_id = None)
    - **:param _id:** (int, Optional), setting id. I.e: 1
    - **:return:** dict, setting status and missing fields. I.e: \n
            {
                "status": "partial",
                "missing_fields": [
                    "pairs_list"
                ]
            }
    """

    return await get_setting_status(_id=_id, db_session=db_session)


@router.get(
    path="/setting",
    summary="Get setting",
    response_model=SettingSchema,
    status_code=status.HTTP_200_OK,
)
async def _get_setting(db_session: DBSessionDep, _id: int | None = None):
    """
    Get setting by _id, or last setting (_id = None)
    - **:param _id:** (int, Optional), setting id. I.e: 1
    - **:return:** dict, setting. I.e: \n
            {
                "binance_api_key": "gak3ojhK3kNHg4UIU11I...",
                "binance_api_secret": "gak3ojhK3kNHg4UIU11I...",
                "pairs_list": [
                    "adausdt",
                    "ethusdt",
                    "etcusdt"
                ],
                ...
            }
    """

    return await get_setting(_id=_id, db_session=db_session)


@router.post(
    path="/setting",
    summary="Add setting",
    response_model=SettingSchema,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
)
async def _add_setting(setting_req: SettingRequest, db_session: DBSessionDep):
    """
    Add setting
    - **:Request body:** \n
            {
                "binance_api_key": (str, Optional) binance api key. I.e: "gak3ojhK3...",
                "binance_api_secret": (str, Optional) binance api secret. I.e: "gak3ojhK3...",
                "pairs_list": (list, Optional) pairs list. I.e: [
                    "adausdt",
                    "ethusdt",
                    "etcusdt",
                ],
                ...
            }
    - **:return:** dict, item updated. I.e: \n
            {
                "binance_api_key": "gak3ojhK3...",
                "binance_api_secret": "gak3ojhK3...",
                ...
            }
    """

    return await add_setting(setting_req=setting_req, db_session=db_session)


@router.patch(
    path="/setting",
    summary="Update partial setting",
    response_model=SettingSchema,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
)
@router.put(
    path="/setting",
    summary="Update complete setting",
    response_model=SettingSchema,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
)
async def _update_setting(
    setting_req: SettingRequest,
    db_session: DBSessionDep,
    _id: int | None = None,
):
    """
    Update setting by id, or last setting (_id = None)
    - **:param _id:** (int, Optional), setting id. I.e: 1
    - **:Request body:** \n
            {
                "binance_api_key": (str, Optional) binance api key. I.e: "gak3ojhK3...",
                "binance_api_secret": (str, Optional) binance api secret. I.e: "gak3ojhK3...",
                "pairs_list": (list, Optional) pairs list. I.e: [
                    "adausdt",
                    "ethusdt",
                    "etcusdt",
                ],
                ...
            }
    - **:return:** dict, item updated. I.e: \n
            {
                "binance_api_key": "gak3ojhK3...",
                "binance_api_secret": "gak3ojhK3...",
                ...
            }
    """

    return await update_setting(_id=_id, setting_req=setting_req, db_session=db_session)


@router.delete(
    path="/setting", summary="Delete setting", status_code=status.HTTP_200_OK
)
async def _delete_setting(_id: int, db_session: DBSessionDep):
    """
    Delete setting by _id
    - **:param _id:** int, setting id. I.e: 1
    - **:return:** dict, item deleted. I.e: \n
            {
                "delete": "success",
                "id": 1
            }
    """

    return await delete_setting(_id=_id, db_session=db_session)
