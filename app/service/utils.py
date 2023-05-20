"""Security layer module"""
# Built-In
from typing import TypeVar

# Third-Party
from Crypto.Cipher import AES
from pydantic import BaseModel

# App
from app.models import CriptographyModeEnum
from app.core.cryptography import aes_encrypt, aes_decrypt

TypeModel = TypeVar("TypeModel", bound=BaseModel)


def key_cryptography_proccess(
    settings_obj: TypeModel, mode: CriptographyModeEnum
) -> TypeModel:
    """
    Key encrypt/decrypt mode proccess
    """

    if settings_obj.binance_api_key:
        if mode == CriptographyModeEnum.ENCRYPT:
            settings_obj.binance_api_key = aes_encrypt(settings_obj.binance_api_key)
        else:
            settings_obj.binance_api_key = aes_decrypt(settings_obj.binance_api_key)

    if settings_obj.binance_api_secret:
        if mode == CriptographyModeEnum.ENCRYPT:
            settings_obj.binance_api_secret = aes_encrypt(
                settings_obj.binance_api_secret
            )
        else:
            settings_obj.binance_api_secret = aes_decrypt(
                settings_obj.binance_api_secret
            )

    return settings_obj
