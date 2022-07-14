from enum import Enum


class TransactionNetworks(str, Enum):
    bitcoin = 'bitcoin'
    litecoin = 'litecoin'
    celo = 'celo'
    binance = 'binance'
    ethereum = 'ethereum'
    polygon = 'polygon'
    ropsten = 'ropsten'
    binance_testnet = 'binance_testnet'


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


VALID_NETWORKS = {
    LITECOIN_MAINNET,
    BITCOIN_MAINNET,
    BINANCE_MAINNET,
    ETHEREUM_MAINNET,
    CELO_MAINNNET,
    POLYGON_MAINNET,
    ROPSTEN_TESTNET,
    BINANCE_TESTNET
}
