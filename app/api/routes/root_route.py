"""Root routes module"""
# Built-In
from typing import Dict

# Third-Party
from fastapi import APIRouter, status

# App
from app.config import settings

router = APIRouter()


@router.get(path="/", summary="Root", status_code=status.HTTP_200_OK)
async def root() -> Dict[str, str]:
    """
    Return api information
    - **return:** dict, api information. I.e: \n
            {
                "project": "Abechennon Free Backend [ CORE ]",
                "version": "0.1.0"
            }
    """

    return {"project": settings.PROJECT_NAME, "version": settings.PROJECT_VERSION}
