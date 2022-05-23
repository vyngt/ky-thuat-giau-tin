"""
Mô đun hỗ trợ mã hóa, giải mã để trích xuất thông điệp.

    - encrypt_message: Mã hóa thông điệp.
    - decrypt_message: Trích xuất thông điệp.
"""

import secrets
from base64 import urlsafe_b64encode as b64encode, urlsafe_b64decode as b64decode
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def __derive(password: str, salt: bytes):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return b64encode(kdf.derive(password.encode()))


def encrypt_message(message: str, password: str):
    """Mã hóa thông điệp"""
    salt = secrets.token_bytes(16)
    key = __derive(password, salt)
    token = b64encode(Fernet(key).encrypt(message.encode()))
    return b64encode(b"%b%b" % (salt, b64decode(token)))


def decrypt_message(token: bytes, password: str):
    """Giải mã để trích xuất thông điệp"""
    decoded = b64decode(token)
    salt, cipher_text = decoded[:16], decoded[16:]
    key = __derive(password, salt)
    return Fernet(key).decrypt(cipher_text)
