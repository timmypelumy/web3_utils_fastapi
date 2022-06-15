import base58
from solana.keypair import Keypair
from base58 import b58decode, b58encode


def generate_solana_wallet(seed: str, username=None):
    if not seed:
        raise ValueError("Seed argument is required!")

    # Create Wallet from 32 bytes seed
    seedbytes32 = b58encode(seed)[:32]
    account = Keypair.from_seed(seedbytes32)

    # Private Key is equivalent to the first 32 chars of the secret_key
    private_key_bytes = account.secret_key[:32]
    # print(seed, ' ---- ', seedbytes32, ' ---- ', account.secret_key[:32])

    account_info = {
        'private_key': private_key_bytes.decode(),
        "address": str(account.public_key),
        'path': None,
    }

    return account_info
