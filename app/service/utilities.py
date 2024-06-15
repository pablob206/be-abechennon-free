"""Utilities layer module"""

# Built-In
from typing import TypeVar

# Third-Party
from pydantic import BaseModel

from app.core import aes_cipher

# App
from app.schemas import CriptographyModeEnum

TypeModel = TypeVar("TypeModel", bound=BaseModel)


def key_cryptography_proccess(setting_obj: TypeModel, mode: CriptographyModeEnum) -> TypeModel:
    """
    Key encrypt/decrypt mode proccess
    """

    if setting_obj.binance_api_key:  # type: ignore
        if mode == CriptographyModeEnum.ENCRYPT:
            setting_obj.binance_api_key = aes_cipher.encrypt(setting_obj.binance_api_key)  # type: ignore
        else:
            setting_obj.binance_api_key = aes_cipher.decrypt(setting_obj.binance_api_key)  # type: ignore

    if setting_obj.binance_api_secret:  # type: ignore
        if mode == CriptographyModeEnum.ENCRYPT:
            setting_obj.binance_api_secret = aes_cipher.encrypt(setting_obj.binance_api_secret)  # type: ignore
        else:
            setting_obj.binance_api_secret = aes_cipher.decrypt(setting_obj.binance_api_secret)  # type: ignore

    return setting_obj
