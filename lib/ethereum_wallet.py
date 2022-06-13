from eth_account import Account

ETHEREUM_DERIVATION_PATH = "m/44'/60'/0'/0/0"


def generate_ethereum_wallet(passphrase, username=None):
    if not passphrase:
        raise ValueError("Passphrase argument is required!")

    Account.enable_unaudited_hdwallet_features()
    account = Account.from_mnemonic(
        passphrase,  account_path=ETHEREUM_DERIVATION_PATH)

    account_info = {
        'private_key': account.key.hex(),
        "address": account.address,
        'path': ETHEREUM_DERIVATION_PATH,
    }

    return account_info
