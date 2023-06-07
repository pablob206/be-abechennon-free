"""Setting utilities module"""
# Built-In
from typing import List

# App
from app.models import Setting


def check_setting_fields(setting: Setting) -> List[str]:
    """
    Check setting fields
    Returns a list with incomplete fields
    """

    setting_dict = setting.dict(exclude={"id"})
    return [field for field in setting_dict if setting_dict.get(field) is None]
