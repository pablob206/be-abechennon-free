"""Settings service module"""
# Built-In
from datetime import datetime
from typing import Dict, List, Union, Any

# Third-Party
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

# App
from app.models import Settings, SettingsStatusEnum, CriptographyModeEnum
from app.schemas import SettingsSchema, SettingsRequest
from app.service.settings.utils import check_settings_fields
from app.data_access import (
    get_settings_query,
    update_add_obj_query,
    update_settings_query,
    delete_obj_query,
)
from app.service.utils import key_cryptography_proccess


async def get_settings_status(
    db_session: AsyncSession | None = None, _id: int | None = None
) -> Dict[str, Union[str, List[str]]]:
    """
    Get settings status
    """

    if not (settings := await get_settings_query(_id=_id, db_session=db_session)):
        return {"status": SettingsStatusEnum.BASIC}

    status = SettingsStatusEnum.PARTIAL
    if not (missing_fields := check_settings_fields(settings=settings)):
        status = SettingsStatusEnum.FULL
    return {"status": status, "missing_fields": missing_fields}


async def get_settings(
    db_session: AsyncSession, _id: int | None = None
) -> SettingsSchema | None:
    """
    Get settings
    """

    if not (settings_db := await get_settings_query(_id=_id, db_session=db_session)):
        raise HTTPException(404, f"Settings id: [{_id}], not found")

    return key_cryptography_proccess(
        settings_obj=SettingsSchema(**settings_db.dict()),
        mode=CriptographyModeEnum.DECRYPT,
    )


async def get_bot_status(db_session: AsyncSession) -> Dict[str, str]:
    """
    Get bot status
    """

    if not (settings_db := await get_settings_query(db_session=db_session)):
        raise HTTPException(404, "Settings not found")

    return {"status": settings_db.bot_status}


async def add_settings(
    settings_req: SettingsRequest, db_session: AsyncSession
) -> Settings | None:
    """
    Add settings
    """

    settings_req = key_cryptography_proccess(
        settings_obj=settings_req, mode=CriptographyModeEnum.ENCRYPT
    )
    return await update_add_obj_query(
        item=Settings(**settings_req.dict()), db_session=db_session
    )


async def update_settings(
    settings_req: SettingsRequest,
    db_session: AsyncSession,
    _id: int | None = None,
) -> Settings:
    """
    Update settings
    """

    settings_dto = await get_settings(
        _id=_id,
        db_session=db_session,
    )

    filters = {
        key: value for key, value in settings_req.dict().items() if value is not None
    }
    for key in filters:
        setattr(settings_dto, key, filters.get(key))
    settings_dto.updated_at = datetime.utcnow()

    settings_dto = key_cryptography_proccess(
        settings_obj=settings_dto, mode=CriptographyModeEnum.ENCRYPT
    )
    return await update_settings_query(
        _id=settings_dto.id,
        settings=Settings(**settings_dto.dict()),
        db_session=db_session,
    )


async def delete_settings(
    _id: int, db_session: AsyncSession
) -> Dict[str, Union[str, Dict[str, Any]]]:
    """
    Delete settings
    """

    if not (settings := await get_settings_query(_id=_id, db_session=db_session)):
        raise HTTPException(404, f"Settings id: [{_id}], not found")

    settings_deleted = await delete_obj_query(item=settings, db_session=db_session)
    return {"delete": "success", "settings": settings_deleted}
