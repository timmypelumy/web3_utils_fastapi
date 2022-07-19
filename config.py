from pydantic import BaseSettings
import motor.motor_asyncio
from typing import Union, Dict


class AppSettings(BaseSettings):
    master_encryption_key: bytes = b'FVSrpDX6K9twuDINKqyr3NIhJML5Du3ksyp8Go7QS5M='
    encryption_salt: bytes = b'BVJKUIYFTDFKCUJSTDT^DE^&RIUFIJCVCUYDKUVr3NIhJML5D*&*%&&^RUIBVjvyudS5M='
    key_encryption_key: str = "UVTYFYUFTDY%DYUIuvytrs%&^YFICGXCYIHKVJGHXTYUCJHGHXTSRT%*&&"
    app_name: str = "Beepo"
    db_url: str = 'mongodb://localhost:27017'
    api_layer_key: str = 'PZtaVnhWbgSDoy1ULZWTmomdSa89q74Z'
    coingecko_key: str = ""
    etherscan_key: str = 'XNSZYWDMS3126XC8BKSTIYKDIUNFR2VECM'
    bsccan_key: str = ''
    celoscan_key: str = ''
    ipfs_read_nodes: Dict = {
        'cloudflare': ' https://cloudflare-ipfs.com/ipfs'
    }
    secret_key: str = "@#$%^Ygtrdytfyiguo^Ou67798ouyxSD%IU7t65srdtuyiCXYTDFIUGOUC*^DDs57du6yiUSYDU"
    hash_algorithm: str = "HS256"
    access_token_expiration_in_minutes: float = 60
    client_url: str = 'http://localhost:3000'
    filecoin_node_url: str = 'https://2CAP8OkeTVTPaSV4cYipKHYHDZO:3e25403be4e9904c61bf62bea62e9a78@filecoin.infura.io'
    ipfs_node_url: str = 'https://ipfs.infura.io:5001'
    heroku_app_url: Union[str, None] = None
    chain_nodes: Dict[int, Dict[str, str]] = {
        42220: {
            'http': 'https://rpc.ankr.com/celo',
            'ws':  'wss://forno.celo.org/ws',
        },

        1: {
            'http': 'https://eth-mainnet.public.blastapi.io',
            'ws': ''
        },

        56: {
            'http': 'https://bsc-dataseed1.binance.org',
            'ws': ''

        },

        137: {
            'http': 'https://polygon-rpc.com',
            'ws': ''
        },

        5000: {
            'http': 'http://127.0.0.1:5000',
            'ws': ''
        },

        3: {
            'http': 'https://rpc.ankr.com/eth_ropsten',
            'ws': ''
        },

        97: {

            'http': 'https://data-seed-prebsc-1-s3.binance.org:8545',
            'ws': ''
        },

        44787: {
            'http': 'https://data-seed-prebsc-1-s3.binance.org:8545',
            'ws': ''
        },

        80001: {
            'http': 'https://matic-testnet-archive-rpc.bwarelabs.com',
            'ws': ''
        }

    }


settings = AppSettings()
db_client = motor.motor_asyncio.AsyncIOMotorClient(settings.db_url)
db = db_client.beepo_db
