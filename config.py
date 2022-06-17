from pydantic import BaseSettings
import motor.motor_asyncio
from typing import Union, Dict


class AppSettings(BaseSettings):
    app_name: str = "Beepo"
    db_url: str = 'mongodb://localhost:27017'
    secret_key: str = "@#$%^Ygtrdytfyiguo^Ou67798ouyxSD%IU7t65srdtuyiCXYTDFIUGOUC*^DDs57du6yiUSYDU"
    hash_algorithm: str = "HS256"
    access_token_expiration_in_minutes: int = 60
    client_url: str = 'http://localhost:3000'
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
        }

    }


settings = AppSettings()
db_client = motor.motor_asyncio.AsyncIOMotorClient(settings.db_url)
db = db_client.beepo_db
