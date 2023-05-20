"""Settings routes module"""
# Built-In
from typing import Dict, List, Union

# Third-Party
from fastapi import APIRouter, status

# App
from app.service.settings import (
    get_settings_status,
    get_settings,
    update_settings,
    add_settings,
    delete_settings,
)
from app.schemas import SettingsSchema, SettingsRequest
from app.api import DBSessionDep

router = APIRouter()


@router.get(
    path="/settings/status",
    summary="Settings status",
    response_model=Dict[str, Union[str, List[str]]],
    status_code=status.HTTP_200_OK,
)
async def _get_settings_status(db_session: DBSessionDep, _id: int | None = 1):
    """
    Get settings status
    - **:param _id:** (int, Default: 1), setting id. I.e: 1
    - **:return:** dict, settings status and missing fields. I.e: \n
            {
                "status": "partial",
                "missing_fields": [
                    "pairs_list"
                ]
            }
    """

    return await get_settings_status(_id=_id, db_session=db_session)


@router.get(
    path="/settings",
    summary="Get settings",
    response_model=SettingsSchema,
    response_model_exclude=["id"],
    status_code=status.HTTP_200_OK,
)
async def _get_settings(db_session: DBSessionDep, _id: int | None = 1):
    """
    Get settings
    - **:param _id:** (int, Default: 1), setting id. I.e: 1
    - **:return:** dict, settings. I.e: \n
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

    return await get_settings(_id=_id, db_session=db_session)


@router.post(
    path="/settings",
    summary="Add settings",
    response_model=SettingsSchema,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
)
async def _add_settings(settings_req: SettingsRequest, db_session: DBSessionDep):
    """
    Add settings
    - **:Request body:** { \n
            "binance_api_key": (str, Optional) binance api key. I.e: "gak3ojhK3kNHg4UIU11I...",
            "binance_api_secret": (str, Optional) binance api secret. I.e: "gak3ojhK3kNHg4UIU11I...",
            "pairs_list": (list, Optional) pairs list. I.e: [
                "adausdt",
                "ethusdt",
                "etcusdt",
            ],
            ...
        }
    - **:return:** dict, item updated. I.e: \n
            {
                "binance_api_key": "gak3ojhK3kNHg4UIU11I...",
                "binance_api_secret": "gak3ojhK3kNHg4UIU11I...",
                ...
            }
    """

    return await add_settings(settings_req=settings_req, db_session=db_session)


@router.patch(
    path="/settings",
    summary="Update partial settings",
    response_model=SettingsSchema,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
)
@router.put(
    path="/settings",
    summary="Update complete settings",
    response_model=SettingsSchema,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
)
async def _update_settings(
    settings_req: SettingsRequest,
    db_session: DBSessionDep,
    _id: int | None = 1,
):
    """
    Update settings
    - **:param _id:** (int, Default: 1), setting id. I.e: 1
    - **:Request body:** { \n
            "binance_api_key": (str, Optional) binance api key. I.e: "gak3ojhK3kNHg4UIU11I...",
            "binance_api_secret": (str, Optional) binance api secret. I.e: "gak3ojhK3kNHg4UIU11I...",
            "pairs_list": (list, Optional) pairs list. I.e: [
                "adausdt",
                "ethusdt",
                "etcusdt",
            ],
            ...
        }
    - **:return:** dict, item updated. I.e: \n
            {
                "binance_api_key": "gak3ojhK3kNHg4UIU11I...",
                "binance_api_secret": "gak3ojhK3kNHg4UIU11I...",
                ...
            }
    """

    return await update_settings(
        _id=_id, settings_req=settings_req, db_session=db_session
    )


@router.delete(
    path="/settings", summary="Delete settings", status_code=status.HTTP_200_OK
)
async def _delete_settings(_id: int, db_session: DBSessionDep):
    """
    Delete settings
    - **:param _id:** int, setting id. I.e: 1
    - **:return:** dict, item deleted. I.e: \n
            {
                "delete": "success",
                "id": 1
            }
    """

    return await delete_settings(_id=_id, db_session=db_session)
