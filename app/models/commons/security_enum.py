"""Security Enum module"""
# Built-In
from enum import Enum


class CriptographyModeEnum(str, Enum):
    """
    Define the criptography mode
    """

    ENCRYPT = "encrypt"
    DECRYPT = "decrypt"
