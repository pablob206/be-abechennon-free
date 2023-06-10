"""Setting Enum module"""
# Built-In
from enum import Enum


class SettingStatusEnum(str, Enum):
    """
    Define different setting status enum
    """

    BASIC = "BASIC"
    PARTIAL = "PARTIAL"
    FULL = "FULL"
