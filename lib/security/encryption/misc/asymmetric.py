from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESSIV


def get_shared_key(private_key: X25519PrivateKey, peer_public_key: X25519PublicKey) -> bytes:
    if not private_key:
        raise ValueError("Argument `private_key` is required")

    if not peer_public_key:
        raise ValueError("Argument `peer_public_key` is required")

    shared_key = private_key.exchange(peer_public_key)

    return shared_key


def get_derived_key(shared_key: bytes, salt: bytes, info: bytes) -> bytes:

    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=64,
        salt=salt,
        info=info,
    ).derive(shared_key)

    return derived_key


def encrypt(key: bytes, data: bytes) -> bytes:
    aessiv = AESSIV(key)
    ct = aessiv.encrypt(data, associated_data=None)
    return ct


def decrypt(key: bytes, token: bytes) -> bytes:
    aessiv = AESSIV(key)
    data = aessiv.decrypt(token, associated_data=None)
    return data
