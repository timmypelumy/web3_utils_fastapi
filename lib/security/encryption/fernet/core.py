from cryptography.fernet import Fernet, InvalidToken, MultiFernet
from typing import Union, List


def encrypt(keys: List[Union[str, bytes]], data: bytes) -> bytes:
    if not keys or len(keys) == 0:
        raise ValueError("Encryption key(s) is required")

    fernet_list = [Fernet(key) for key in keys]

    fernet = MultiFernet(fernet_list)
    encrypted = fernet.encrypt(data)

    return encrypted


def rotate(keys: List[str], token: bytes) -> Union[bytes, None]:
    if not keys or len(keys) == 0:
        raise ValueError("Encryption key(s) is required")

    fernet_list = [Fernet(key) for key in keys]

    fernet = MultiFernet(fernet_list)

    try:
        rotated = fernet.rotate(token)
        return rotated

    except InvalidToken:
        return None


def decrypt(keys: List[Union[str, bytes]], token: bytes):
    if not keys or len(keys) == 0:
        raise ValueError("Encryption key(s) is required")

    fernet_list = [Fernet(key) for key in keys]

    fernet = MultiFernet(fernet_list)
    try:
        decrypted = fernet.decrypt(token)
        return decrypted

    except InvalidToken:
        return None
