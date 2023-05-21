"""Cryptography layer module"""
# Third-Party
import pytest

# App
from app.core.cryptography import aes_encrypt, aes_decrypt


class TestCryptography:
    """
    Unit test to cryptography layer
    """

    @pytest.mark.parametrize(
        "text, expected_result",
        [
            (
                "gak3ojhK3kNHg4UIU222",
                "c005cb31d555778f69bde872fc9f23348bf7870fadb83a10d175ae81e46db7c7",
            ),
            (
                "asd5sgd5s8dg8vcdb5a5sf8",
                "a25f774f1848f122ef1cb3709483f4cc3229529e7aaf73d22aa271acee6ccfbb",
            ),
            (
                "2fdsdgfsdgf58sdgfsdfdsa",
                "30417842533002f7aabe8d2bbc0193da65f20c9b3293c9ac75bda18251980b8c",
            ),
        ],
    )
    def test_aes_encrypt(self, text, expected_result):
        """
        Test aes encrypt
        """

        assert aes_encrypt(text) == expected_result

    @pytest.mark.parametrize(
        "ciphertext, expected_result",
        [
            (
                "c005cb31d555778f69bde872fc9f23348bf7870fadb83a10d175ae81e46db7c7",
                "gak3ojhK3kNHg4UIU222",
            ),
            (
                "a25f774f1848f122ef1cb3709483f4cc3229529e7aaf73d22aa271acee6ccfbb",
                "asd5sgd5s8dg8vcdb5a5sf8",
            ),
            (
                "30417842533002f7aabe8d2bbc0193da65f20c9b3293c9ac75bda18251980b8c",
                "2fdsdgfsdgf58sdgfsdfdsa",
            ),
        ],
    )
    def test_aes_decrypt(self, ciphertext, expected_result):
        """
        Test aes decrypt
        """

        assert aes_decrypt(ciphertext) == expected_result
