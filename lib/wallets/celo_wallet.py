from eth_account import Account
from config import settings
from .web3_utils import create_http_web3

CELO_DERIVATION_PATH = "m/44'/52752'/0'/0"
NETWORK_ID = 42220


def generate_celo_wallet(passphrase, username=None):
    if not passphrase:
        raise ValueError("Passphrase argument is required!")

    Account.enable_unaudited_hdwallet_features()
    account = Account.from_mnemonic(
        passphrase,  account_path=CELO_DERIVATION_PATH)
    account_info = {
        'private_key': account.key.hex(),
        "address": account.address,
        'path': CELO_DERIVATION_PATH,
    }

    return account_info


def get_balance(address: str):
    web3 = create_http_web3((settings.chain_nodes[NETWORK_ID])['http'])
    balance = web3.eth.get_balance(address)

    return balance
