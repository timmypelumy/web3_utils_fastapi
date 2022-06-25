from .import symmetric
from .import asymmetric
from .keypair import load_private_key, load_public_key
from config import settings


def pipeline_get_derived_key(private_key: bytes, peer_public_key: bytes, salt: bytes, info: bytes):
    private = load_private_key(private_key)
    peer_public = load_public_key(peer_public_key)

    shared = asymmetric.get_shared_key(private, peer_public)

    derived = asymmetric.get_derived_key(
        shared, salt, info)

    return derived


def pipeline_encrypt(private_key: bytes, peer_public_key: bytes, salt: bytes, info: bytes,  data: bytes, halfway=False):

    derived = pipeline_get_derived_key(
        private_key, peer_public_key, salt, info)

    cipher_1 = asymmetric.encrypt(derived, data)

    if halfway:
        print("\nHalfway encrypted\n")
        return cipher_1

    cipher_2 = symmetric.encrypt(
        [settings.master_encryption_key.encode(), ], cipher_1)

    return cipher_2


def pipeline_decrypt(private_key: bytes, peer_public_key: bytes, salt: bytes, info: bytes,  cipher: bytes, halfway=False, only_master=False):

    derived = pipeline_get_derived_key(
        private_key, peer_public_key, salt, info)

    if halfway:
        print("\nHalfway decrypted\n")
        data = asymmetric.decrypt(derived, cipher)
        return data

    cipher_1 = symmetric.decrypt([settings.master_encryption_key, ], cipher)

    if cipher_1 is not None:
        if only_master:
            return cipher_1

        else:
            data = asymmetric.decrypt(derived, cipher_1)
            return data

    else:

        return None
