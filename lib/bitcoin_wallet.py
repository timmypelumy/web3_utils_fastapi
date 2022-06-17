from bitcoinlib.wallets import Wallet


def generate_bitcoin_wallet(passphrase, username):
    if not passphrase:
        raise ValueError("Passphrase argument is required!")

    wallet = Wallet.create(username + 'bitcoin', network='bitcoin',
                           keys=passphrase, witness_type='segwit')

    wif = wallet.account(0).wif
    wif_public = wallet.account(0).key().wif_public()
    address = wallet.account(0).address
    derivation_path = wallet.account(0).path
    balance = wallet.account(0).balance()

    account_info = {
        "wif_key": wif,
        "wif_public_key": wif_public,
        "address": address,
        'path': derivation_path,
        'balance': balance

    }

    return account_info
