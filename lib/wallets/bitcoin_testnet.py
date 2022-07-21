from bitcoinlib.wallets import Wallet
from bitcoinlib.services.services import Service
from typing import Dict


def generate_bitcoin_testnet_wallet(passphrase, username, raw=False):
    if not passphrase:
        raise ValueError("Passphrase argument is required!")

    wallet = Wallet.create(username + 'bitcoin_testnet', network='testnet',
                           keys=passphrase, witness_type='segwit')

    if raw:

        return wallet

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
        'balance': balance,
        'name': username + 'bitcoin_testnet'

    }

    return account_info


def send_bitcoin_testnet_transaction(tx: Dict, passphrase: str, username) -> Dict:
    from_address = tx['from_address']
    to_address = tx['to_address']
    value = tx['value']

    account = generate_bitcoin_testnet_wallet(passphrase, username)

    w = Wallet(wallet=account['name'])

    main_output_utxo = (to_address, value)

    transaction = w.transaction_create(
        output_arr=[main_output_utxo], account_id=0, network='testnet'
    )

    print(transaction)

    return {}


def get_balance(address: str):
    srv = Service(network='testnet', max_providers=3, min_providers=1)
    return srv.getbalance(address)
