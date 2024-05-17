"""Module to store settings constants used in the project"""

# Built-In
from enum import StrEnum


class SettingStatusEnum(StrEnum):
    """
    Define different setting status types
    """

    BASIC = "BASIC"
    PARTIAL = "PARTIAL"
    FULL = "FULL"
