from distutils.command.config import config
from cryptography.hazmat.primitives.asymmetric import rsa
from typing import Dict, Any
from cryptography.hazmat.primitives import serialization
from config import settings


PUBLIC_EXPONENT = 65537
DEFAULT_KEY_SIZE = 4096


def generate_rsa_keypair(serialized=True) -> Dict[str, Any]:

    private_key = rsa.generate_private_key(
        public_exponent=PUBLIC_EXPONENT,
        key_size=DEFAULT_KEY_SIZE
    )

    public_key = private_key.public_key()

    if not serialized:
        return {
            'private': private_key,
            'public': public_key
        }

    pem_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(
            settings.key_encryption_key.encode())
    )

    pem_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return {
        'private': pem_private.decode(),
        'public': pem_public.decode()
    }


def load_rsa_keypair(keypair: Dict) -> Dict:

    keys = {}

    if 'private' in keypair:
        keys['private'] = serialization.load_pem_private_key(
            keypair['private'].encode(),
            password=settings.key_encryption_key.encode()
        )

    if 'public' in keypair:
        keys['public'] = serialization.load_pem_public_key(
            keypair['public'].encode()
        )

    return keys
