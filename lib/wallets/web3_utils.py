from web3 import Web3


def is_valid_address(address: str):
    web3 = Web3()

    return web3.isChecksumAddress(address)


def create_http_web3(url) -> Web3:
    return Web3(Web3.HTTPProvider(url))



