"""Security layer module"""
# Built-In
from enum import Enum
from typing import TypeVar
from binascii import b2a_hex, a2b_hex

# Third-Party
from Crypto.Cipher import AES
from pydantic import BaseModel

# App
from app.config import settings

TypeModel = TypeVar("TypeModel", bound=BaseModel)


class CriptographyModeEnum(str, Enum):
    """
    Define the criptography mode
    """

    ENCRYPT = "encrypt"
    DECRYPT = "decrypt"


def aes_encrypt(text: str) -> str:
    """
    AES encrypt text
    """

    key = settings.KEY_AES_ENCRYPT
    mode = AES.MODE_CBC
    ivv = key[:16]
    cryptos = AES.new(key.encode("utf-8"), mode, ivv.encode("utf-8"))
    length = 16
    count = len(text.encode("utf-8"))
    if count % length != 0:
        add = length - (count % length)
    else:
        add = 0
    text = text + ("\0" * add)
    ciphertext = cryptos.encrypt(text.encode("utf-8"))
    return b2a_hex(ciphertext).decode("utf-8")


def aes_decrypt(text: str) -> str:
    """
    AES decrypt text
    """

    key = settings.KEY_AES_ENCRYPT
    mode = AES.MODE_CBC
    ivv = key[:16]
    cryptos = AES.new(key.encode("utf-8"), mode, ivv.encode("utf-8"))
    plain_text = cryptos.decrypt(a2b_hex(text))
    return plain_text.decode("utf-8").rstrip("\0")


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
