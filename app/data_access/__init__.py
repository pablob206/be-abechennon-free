"""Initialize data access layer modules"""
# App
from .settings_data import (
    get_settings_query,
    delete_settings_query,
    update_settings_query,
)
from .utils_data import (
    update_add_obj_query,
    delete_obj_query,
)