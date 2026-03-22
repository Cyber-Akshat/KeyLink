import re
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import os
import base64
from cryptography.fernet import Fernet
from pyexpat.errors import messages


def validate_key(key):
    if len(key) < 15:
        raise ValueError("Key must be at least 15 characters long")

    if not re.search(r"[A-Z]", key):
        raise ValueError("Key must be at least one uppercase letter")

    if not re.search(r"""[!@#$%^&*()-_=+{}[]|\\:;\'",.?~]""", key):
        raise ValueError("Key must contain at least one special character")

def derive_key(password, salt):
    validate_key(password)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_data(data, password):
    validate_key(password)

    salt = os.urandom(16)
    key = derive_key(password, salt)

    fernet = Fernet(key)
    encrypt_data = fernet.encrypt(data.encode())

    return salt, encrypt_data

def decrypt_data(encrypted_data, password, salt):
    validate_key(password)
    key = derive_key(password, salt)
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_data).decode()

















