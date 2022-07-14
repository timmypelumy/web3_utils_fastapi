from eth_account import Account
from config import settings
from typing import Dict
from .ethereum_wallet import fetch_gas_oracle
from .web3_utils import create_http_web3


BINANCE_DERIVATION_PATH = "m/44'/60'/0'/0/0"
NETWORK_ID = 97


def generate_binance_testnet_wallet(passphrase, username=None):
    if not passphrase:
        raise ValueError("Passphrase argument is required!")

    Account.enable_unaudited_hdwallet_features()
    account = Account.from_mnemonic(
        passphrase,  account_path=BINANCE_DERIVATION_PATH)

    account_info = {
        'private_key': account.key.hex(),
        "address": account.address,
        'path': BINANCE_DERIVATION_PATH,
    }

    return account_info


def get_balance(address: str):
    web3 = create_http_web3((settings.chain_nodes[NETWORK_ID])['http'])
    balance = web3.eth.get_balance(address)

    return balance


def send_binance_testnet_transaction(tx: Dict, passphrase: str) -> Dict:
    if not passphrase:
        raise ValueError("Passphrase argument is required!")

    gas_metrics = fetch_gas_oracle()

    account = generate_binance_testnet_wallet(passphrase=passphrase)

    from_address = tx['from_address']
    to_address = tx['to_address']
    value = tx['value']

    if account['address'] != from_address:
        raise ValueError("Address from passphrase does not match with supplied address, {0} != {1}".format(
            account['address'], from_address))

    web3 = create_http_web3(settings.chain_nodes[NETWORK_ID]['http'])
    web3.eth.default_account = from_address

    signed_tx = web3.eth.account.sign_transaction({
        'to': to_address,
        'from': from_address,
        'value': web3.toWei(value, 'ether'),
        'chainId': NETWORK_ID,
        'nonce': web3.eth.get_transaction_count(from_address),
        'gas': web3.eth.estimate_gas({'to': to_address, 'from': from_address, 'value': web3.toWei(value, 'ether')}),
        'maxFeePerGas': web3.toWei(gas_metrics['fast']['value'] + gas_metrics['base_fee'], 'gwei'),
        'maxPriorityFeePerGas': web3.toWei(gas_metrics['fast']['value'], 'gwei')


    }, account['private_key'])

    return {
        'tx_hash': signed_tx.hash.hex(),
        'send_transaction': web3.eth.send_raw_transaction,
        'raw_tx': signed_tx.rawTransaction
    }
