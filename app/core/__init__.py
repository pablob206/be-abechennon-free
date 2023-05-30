"""Initialize core layer modules"""
# App
from app.config import settings
from .cryptography import AesCipher


aes_cipher = AesCipher(key_aes=settings.KEY_AES)
