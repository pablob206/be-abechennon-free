"""Utilities layer module"""
# Built-In
from typing import TypeVar

# Third-Party
from pydantic import BaseModel

# App
from app.schemas import CriptographyModeEnum
from app.core import aes_cipher

TypeModel = TypeVar("TypeModel", bound=BaseModel)


def key_cryptography_proccess(
    setting_obj: TypeModel, mode: CriptographyModeEnum
) -> TypeModel:
    """
    Key encrypt/decrypt mode proccess
    """

    if setting_obj.binance_api_key:
        if mode == CriptographyModeEnum.ENCRYPT:
            setting_obj.binance_api_key = aes_cipher.encrypt(
                setting_obj.binance_api_key
            )
        else:
            setting_obj.binance_api_key = aes_cipher.decrypt(
                setting_obj.binance_api_key
            )

    if setting_obj.binance_api_secret:
        if mode == CriptographyModeEnum.ENCRYPT:
            setting_obj.binance_api_secret = aes_cipher.encrypt(
                setting_obj.binance_api_secret
            )
        else:
            setting_obj.binance_api_secret = aes_cipher.decrypt(
                setting_obj.binance_api_secret
            )

    return setting_obj
