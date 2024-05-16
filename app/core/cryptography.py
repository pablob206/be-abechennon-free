"""Cryptography layer module"""
# Third-Party
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# App
from config import get_cache_settings


class AesCipher:
    """AES Cipher"""

    def __init__(self, key_aes: str | None = get_cache_settings().KEY_AES):
        """Init"""

        self.key_aes: bytes = key_aes.encode("utf-8")
        self._iv = self.key_aes[:16]
        self.cipher = Cipher(
            algorithms.AES(self.key_aes), modes.CBC(self._iv), backend=default_backend()
        )

    def encrypt(self, text: str) -> str:
        """AES encrypt text"""

        encryptor = self.cipher.encryptor()
        length = 16
        count = len(text.encode("utf-8"))
        if count % length != 0:
            add = length - (count % length)
        else:
            add = 0
        text = text + ("\0" * add)
        ciphertext = encryptor.update(text.encode("utf-8")) + encryptor.finalize()
        return self.to_hex(ciphertext)

    def decrypt(self, text: str) -> str:
        """AES decrypt text"""

        decryptor = self.cipher.decryptor()
        ciphertext = self.from_hex(text)
        plain_text = decryptor.update(ciphertext) + decryptor.finalize()
        return plain_text.decode("utf-8").rstrip("\0")

    @staticmethod
    def to_hex(data):
        """Convert bytes to hex string"""

        return data.hex()

    @staticmethod
    def from_hex(hex_string):
        """Convert hex string to bytes"""

        return bytes.fromhex(hex_string)
