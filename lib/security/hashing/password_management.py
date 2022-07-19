from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.exceptions import InvalidKey
import os

N = 2 ** 16
R = 10
P = 4
LENGTH = 64


def hash_with_scrypt(salt: bytes, data: bytes) -> bytes:
    kdf = Scrypt(
        salt=salt,
        length=LENGTH,
        n=N,
        r=R,
        p=P
    )

    return kdf.derive(data)


def generate_random_chars(n: int = 64 ) -> str:
    return str((os.urandom(n)).hex())


def generate_password() -> str:
    return generate_random_chars(32)


def verify_hash_with_scrypt(salt: bytes, key: bytes, data: bytes):
    kdf = Scrypt(
        salt=salt,
        length=LENGTH,
        n=N,
        r=R,
        p=P
    )

    try:
        kdf.verify(data, key)
    except InvalidKey:
        return False
    else:
        return True
