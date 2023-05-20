"""Security layer module"""
# Built-In
from enum import Enum
from typing import TypeVar
from binascii import b2a_hex, a2b_hex

# Third-Party
from pydantic import BaseModel
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

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

    key = settings.KEY_AES_ENCRYPT.encode("utf-8")
    _iv = key[:16]
    cipher = Cipher(algorithms.AES(key), modes.CBC(_iv), backend=default_backend())
    encryptor = cipher.encryptor()

    length = 16
    count = len(text.encode("utf-8"))
    if count % length != 0:
        add = length - (count % length)
    else:
        add = 0
    text = text + ("\0" * add)

    ciphertext = encryptor.update(text.encode("utf-8")) + encryptor.finalize()
    return b2a_hex(ciphertext).decode("utf-8")


def aes_decrypt(text: str) -> str:
    """
    AES decrypt text
    """

    key = settings.KEY_AES_ENCRYPT.encode("utf-8")
    _iv = key[:16]
    cipher = Cipher(algorithms.AES(key), modes.CBC(_iv), backend=default_backend())
    decryptor = cipher.decryptor()

    ciphertext = a2b_hex(text)
    plain_text = decryptor.update(ciphertext) + decryptor.finalize()
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
