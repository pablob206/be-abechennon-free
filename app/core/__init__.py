"""Initialize core layer modules"""

# App
from app.config import get_cache_settings
from .cryptography import AesCipher
from .sql_dao import SqlDao

aes_cipher = AesCipher(key_aes=get_cache_settings().KEY_AES)
