"""Setting service module"""
# Built-In
from datetime import datetime
from typing import Dict, List, Union, Any

# Third-Party
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

# App
from app.models import Setting, SettingStatusEnum, CriptographyModeEnum
from app.schemas import SettingSchema, SettingRequest
from app.service.setting.utils import check_setting_fields
from app.data_access import (
    get_setting_query,
    update_add_obj_query,
    update_setting_query,
    delete_obj_query,
)
from app.service.utils import key_cryptography_proccess


async def get_setting_status(
    db_session: AsyncSession | None = None, _id: int | None = None
) -> Dict[str, Union[str, List[str]]]:
    """
    Get setting status
    """

    if not (setting := await get_setting_query(_id=_id, db_session=db_session)):
        return {"status": SettingStatusEnum.BASIC}

    status = SettingStatusEnum.PARTIAL
    if not (missing_fields := check_setting_fields(setting=setting)):
        status = SettingStatusEnum.FULL
    return {"status": status, "missing_fields": missing_fields}


async def get_setting(
    db_session: AsyncSession | None = None,
    _id: int | None = None,
) -> SettingSchema | None:
    """
    Get setting
    """

    if not (setting_db := await get_setting_query(_id=_id, db_session=db_session)):
        raise HTTPException(404, f"Setting id: [{_id}], not found")

    return key_cryptography_proccess(
        setting_obj=SettingSchema(**setting_db.dict()),
        mode=CriptographyModeEnum.DECRYPT,
    )


async def get_bot_status(db_session: AsyncSession) -> Dict[str, str]:
    """
    Get bot status
    """

    if not (setting_db := await get_setting_query(db_session=db_session)):
        raise HTTPException(404, "Setting not found")

    return {"status": setting_db.bot_status}


async def add_setting(
    setting_req: SettingRequest, db_session: AsyncSession
) -> Setting | None:
    """
    Add setting
    """

    setting_req = key_cryptography_proccess(
        setting_obj=setting_req, mode=CriptographyModeEnum.ENCRYPT
    )
    return await update_add_obj_query(
        item=Setting(**setting_req.dict()), db_session=db_session
    )


async def update_setting(
    setting_req: SettingRequest,
    db_session: AsyncSession,
    _id: int | None = None,
) -> Setting:
    """
    Update setting
    """

    setting_dto = await get_setting(
        _id=_id,
        db_session=db_session,
    )

    filters = {
        key: value for key, value in setting_req.dict().items() if value is not None
    }
    for key in filters:
        setattr(setting_dto, key, filters.get(key))
    setting_dto.updated_at = datetime.utcnow()

    setting_dto = key_cryptography_proccess(
        setting_obj=setting_dto, mode=CriptographyModeEnum.ENCRYPT
    )
    return await update_setting_query(
        _id=setting_dto.id,
        setting=Setting(**setting_dto.dict()),
        db_session=db_session,
    )


async def delete_setting(
    _id: int, db_session: AsyncSession
) -> Dict[str, Union[str, Dict[str, Any]]]:
    """
    Delete setting
    """

    if not (setting := await get_setting_query(_id=_id, db_session=db_session)):
        raise HTTPException(404, f"Setting id: [{_id}], not found")

    setting_deleted = await delete_obj_query(item=setting, db_session=db_session)
    return {"delete": "success", "setting": setting_deleted}
