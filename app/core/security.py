"""Security layer module"""
# Built-In
from enum import Enum
from typing import TypeVar

# Third-Party
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
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
    iv = key[:16]
    cryptos = AES.new(key.encode("utf-8"), mode, iv.encode("utf-8"))
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
    iv = key[:16]
    cryptos = AES.new(key.encode("utf-8"), mode, iv.encode("utf-8"))
    plain_text = cryptos.decrypt(a2b_hex(text))
    return plain_text.decode("utf-8").rstrip("\0")


def key_cryptography_proccess(
    settings: TypeModel, mode: CriptographyModeEnum
) -> TypeModel:
    """
    Key encrypt/decrypt mode proccess
    """

    if settings.binance_api_key:
        if mode == CriptographyModeEnum.ENCRYPT:
            settings.binance_api_key = aes_encrypt(settings.binance_api_key)
        else:
            settings.binance_api_key = aes_decrypt(settings.binance_api_key)

    if settings.binance_api_secret:
        if mode == CriptographyModeEnum.ENCRYPT:
            settings.binance_api_secret = aes_encrypt(settings.binance_api_secret)
        else:
            settings.binance_api_secret = aes_decrypt(settings.binance_api_secret)

    return settings
