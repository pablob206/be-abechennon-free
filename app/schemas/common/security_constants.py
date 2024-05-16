"""Module to store security constants used in the project"""
# Built-In
from enum import StrEnum


class CriptographyModeEnum(StrEnum):
    """
    Define the criptography mode types
    """

    ENCRYPT = "encrypt"
    DECRYPT = "decrypt"
