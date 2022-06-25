from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
from cryptography.hazmat.primitives import serialization
from typing import Dict, Any


def generate_keypair(serialized=False) -> Dict[str, Any]:
    private_key = X25519PrivateKey.generate()
    public_key = private_key.public_key()

    if not serialized:

        return {
            'private': private_key,
            'public': public_key
        }

    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8,  encryption_algorithm=serialization.NoEncryption())

    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)

    return {
        'private': private_bytes,
        'public': public_bytes
    }


def load_public_key(data: bytes):
    key = serialization.load_pem_public_key(data)
    return key


def load_private_key(data: bytes):
    key = serialization.load_pem_private_key(data, password=None)
    return key
