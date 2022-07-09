from cryptography.fernet import Fernet


def generate_fernet_key():
    key = Fernet.generate_key()

    return key
