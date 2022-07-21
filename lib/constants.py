from enum import Enum


ALLOWED_IMAGE_EXTENSIONS = [
    'png', 'jpeg', 'jpg', 'jfif', 'webp'
]

MAX_PROFILE_PHOTO_SIZE = 0.001 * 1024 * 1024


class TransactionNetworks(str, Enum):
    bitcoin = 'bitcoin'
    litecoin = 'litecoin'
    celo = 'celo'
    binance = 'binance'
    ethereum = 'ethereum'
    polygon = 'polygon'
    ropsten = 'ropsten'
    binance_testnet = 'binance_testnet'
    polygon_mumbai = 'polygon_mumbai'


class NetworkSubunits(str, Enum):
    wei = 'wei'
    gwei = 'gwei'
    satoshi = 'satoshi'
    litoshi = 'litoshi'


LITECOIN_MAINNET = 'litecoin'
BITCOIN_MAINNET = 'bitcoin'
BINANCE_MAINNET = 'binance'
ETHEREUM_MAINNET = 'ethereum'
CELO_MAINNNET = 'celo'
POLYGON_MAINNET = 'polygon'
ROPSTEN_TESTNET = 'ropsten'
BINANCE_TESTNET = 'binance_testnet'
POLYGON_MUMBAI = 'polygon_mumbai'


VALID_NETWORKS = {
    LITECOIN_MAINNET,
    BITCOIN_MAINNET,
    BINANCE_MAINNET,
    ETHEREUM_MAINNET,
    CELO_MAINNNET,
    POLYGON_MAINNET,
    ROPSTEN_TESTNET,
    BINANCE_TESTNET,
    POLYGON_MUMBAI
}
