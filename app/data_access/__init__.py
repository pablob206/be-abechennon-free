"""Initialize data access layer modules"""
# App
from .setting_data import (
    get_setting_query,
    delete_setting_query,
    update_setting_query,
)
from .utils_data import (
    update_add_obj_query,
    delete_obj_query,
    insert_document,
    get_document,
    get_all_document,
    delete_document,
)
from .cache import (
    clear_cache,
    set_klines_cache,
    get_klines_cache,
)
from .order_management_data import (
    get_orders_query,
)
