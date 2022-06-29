from eth_account import Account
from web3 import Web3
from config import settings

POLYGON_DERIVATION_PATH = "m/44'/60'/0'/0/0"
NETWORK_ID = 137


def generate_polygon_wallet(passphrase, username=None):
    if not passphrase:
        raise ValueError("Passphrase argument is required!")

    Account.enable_unaudited_hdwallet_features()
    account = Account.from_mnemonic(
        passphrase,  account_path=POLYGON_DERIVATION_PATH)

    account_info = {
        'private_key': account.key.hex(),
        "address": account.address,
        'path': POLYGON_DERIVATION_PATH,
    }

    return account_info


def get_balance(address: str):
    provider = Web3.HTTPProvider((settings.chain_nodes[NETWORK_ID])['http'])
    web3 = Web3(provider)

    balance = web3.eth.get_balance(address)

    return balance


def is_valid_address(address: str):
    web3 = Web3()

    return web3.isChecksumAddress(address)
