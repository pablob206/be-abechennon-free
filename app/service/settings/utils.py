"""Settings utilities functions"""
# Built-In
from typing import List

# App
from app.models import Settings


def check_settings_fields(settings: Settings) -> List[str]:
    """
    Check settings fields
    Returns a list with incomplete fields
    """

    settings_dict = settings.dict(exclude={"id"})
    return [field for field in settings_dict if settings_dict.get(field) is None]
