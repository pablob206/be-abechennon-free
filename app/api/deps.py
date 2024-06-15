"""Abechennon Free reusable dependencies injection module"""

# Third-Party
from typing import Annotated

# Built-In
from fastapi import Depends, Header
from sqlmodel.ext.asyncio.session import AsyncSession

# App
from app.config import get_cache_settings, get_db_session


def verify_secret_key_dep(secret_key: Annotated[str, Header()]) -> None:
    """Verify secret key"""

    if secret_key != get_cache_settings().SECRET_KEY:
        raise PermissionError("Invalid secret-key")


DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]
