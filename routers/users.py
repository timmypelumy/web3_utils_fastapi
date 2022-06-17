
from uuid import uuid4
from fastapi import APIRouter,  HTTPException, BackgroundTasks, WebSocket
from pydantic import Field
from models.user import UserInModel, UserOutModel, UserDBModel
from models.wallet import CoinWalletModel, CoinWalletModelDB
from fastapi.encoders import jsonable_encoder
from config import db
from datetime import datetime
from datetime import datetime
from uuid import uuid4
from lib import bitcoin_wallet, secret_phrase, litecoin_wallet, ethereum_wallet, binance_wallet, celo_wallet, polygon_wallet
from passlib.context import CryptContext
from typing import List


router = APIRouter(
    prefix='/users',
    responses={
        404: {"description": "User does not exist"}
    }
)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


# Helpers

def create_username(name: str):
    name = ''.join(name.split(" "))
    time = ''.join(str(datetime.now().timestamp()).split('.'))
    return "{0}_{1}".format(name, time)


def get_hash(text):
    return pwd_context.hash((text))


# Backkground tasks
async def create_wallets(new_user: UserOutModel, backup_phrase, seed):

    bitcoin_wallet_info = bitcoin_wallet.generate_bitcoin_wallet(
        backup_phrase, new_user.username)

    litecoin_wallet_info = litecoin_wallet.generate_litecoin_wallet(
        backup_phrase, new_user.username)

    ethereum_wallet_info = ethereum_wallet.generate_ethereum_wallet(
        backup_phrase, new_user.username)

    polygon_wallet_info = polygon_wallet.generate_polygon_wallet(
        backup_phrase, new_user.username)

    binance_wallet_info = binance_wallet.generate_binance_wallet(
        backup_phrase, new_user.username)

    celo_wallet_info = celo_wallet.generate_celo_wallet(
        backup_phrase, new_user.username)

    # solana_wallet_info = solana_wallet.generate_solana_wallet(
    #     seed, new_user.username)

    bitcoin_account_db = CoinWalletModelDB(
        identifier=str(uuid4()),
        coinName='Bitcoin',
        coinTicker='BTC',
        coinDescription="Bitcoin Protocol",
        created=datetime.now().timestamp(),
        derivationPath=bitcoin_wallet_info['path'],
        lastUpdated=datetime.now().timestamp(),
        networkId=None,
        networkName='Bitcoin',
        address=bitcoin_wallet_info['address'],
        ownerId=new_user.identifier,
        pkHash=get_hash(bitcoin_wallet_info['wif_key']),

    )

    litecoin_account_db = CoinWalletModelDB(
        identifier=str(uuid4()),
        coinName='Litecoin',
        coinTicker='LTC',
        coinDescription="Litecoin Protocol",
        created=datetime.now().timestamp(),
        derivationPath=litecoin_wallet_info['path'],
        lastUpdated=datetime.now().timestamp(),
        networkId=None,
        networkName='Litecoin',
        address=litecoin_wallet_info['address'],
        ownerId=new_user.identifier,
        pkHash=get_hash(litecoin_wallet_info['wif_key']),

    )

    binance_account_db = CoinWalletModelDB(
        identifier=str(uuid4()),
        coinName='Smartchain',
        coinTicker='BNB',
        coinDescription="Binance Smartchain",
        created=datetime.now().timestamp(),
        derivationPath=binance_wallet_info['path'],
        lastUpdated=datetime.now().timestamp(),
        networkId=56,
        networkName='Binance Smartchain Mainnet',
        address=binance_wallet_info['address'],
        ownerId=new_user.identifier,
        pkHash=get_hash(binance_wallet_info['private_key']),

    )

    ethereum_account_db = CoinWalletModelDB(
        identifier=str(uuid4()),
        coinName='Ether',
        coinTicker='ETH',
        coinDescription="Ethereum",
        created=datetime.now().timestamp(),
        derivationPath=ethereum_wallet_info['path'],
        lastUpdated=datetime.now().timestamp(),
        networkId=1,
        networkName='Ethereum Mainnet',
        address=ethereum_wallet_info['address'],
        ownerId=new_user.identifier,
        pkHash=get_hash(ethereum_wallet_info['private_key']),

    )

    polygon_account_db = CoinWalletModelDB(
        identifier=str(uuid4()),
        coinName='Matic',
        coinTicker='MATIC',
        coinDescription="Polygon",
        created=datetime.now().timestamp(),
        derivationPath=polygon_wallet_info['path'],
        lastUpdated=datetime.now().timestamp(),
        networkId=1,
        networkName='Polygon Mainnet',
        address=polygon_wallet_info['address'],
        ownerId=new_user.identifier,
        pkHash=get_hash(polygon_wallet_info['private_key']),

    )

    celo_account_db = CoinWalletModelDB(
        identifier=str(uuid4()),
        coinName='Celo',
        coinTicker='CELO',
        coinDescription="Celo",
        created=datetime.now().timestamp(),
        derivationPath=celo_wallet_info['path'],
        lastUpdated=datetime.now().timestamp(),
        networkId=42220,
        networkName='Celo Mainnet',
        address=celo_wallet_info['address'],
        ownerId=new_user.identifier,
        pkHash=get_hash(celo_wallet_info['private_key']),

    )

    # solana_account_db = CoinWalletModelDB(
    #     identifier=str(uuid4()),
    #     coinName='Solana',
    #     coinTicker='SOL',
    #     coinDescription="Solana",
    #     created=datetime.now().timestamp(),
    #     derivationPath=solana_wallet_info['path'],
    #     lastUpdated=datetime.now().timestamp(),
    #     networkId=None,
    #     networkName='Solana Mainnnet',
    #     address=solana_wallet_info['address'],
    #     ownerId=new_user.identifier,
    #     pkHash=get_hash(solana_wallet_info['private_key']),

    # )

    await db.coin_wallets.insert_many([
        # solana_account_db.dict(),
        bitcoin_account_db.dict(),
        litecoin_account_db.dict(),
        binance_account_db.dict(),
        ethereum_account_db.dict(),
        celo_account_db.dict(),
        polygon_account_db.dict()

    ])


@router.post('', response_model=UserOutModel)
async def create_user(userData: UserInModel, background_tasks: BackgroundTasks):
    data = userData.dict()

    while True:
        username = create_username(data['display_name'])
        existingUser = await db.users.find_one({username: username})
        if not existingUser:

            backup = secret_phrase.generate_secret_phrase()
            backup_phrase = backup['passphrase']
            seed = backup['seed']

            new_user = UserDBModel(**data, identifier=str(uuid4()),
                                   username=username, created=datetime.now().timestamp(),
                                   last_updated=datetime.now().timestamp(),
                                   phrase_hash=get_hash(backup_phrase),
                                   backup_phrase=backup_phrase
                                   )

            await db.users.insert_one(new_user.dict())

            background_tasks.add_task(
                create_wallets,  new_user=new_user, backup_phrase=backup_phrase, seed=seed)

            return new_user


@router.get('/{user_identifier}', response_model=UserOutModel)
async def get_user_by_user_identifier(user_identifier: str = Field(min_length=32, max_length=48)):
    user = await db.users.find_one({'identifier': user_identifier})
    if not user:
        raise HTTPException(status_code=404, detail='User does not exist.')
    else:
        return user


@router.get('/{user_identifier}/wallets', response_model=List[CoinWalletModelDB])
async def get_user_wallets(user_identifier: str = Field(min_length=32, max_length=48)):
    user = await db.users.find_one({'identifier': user_identifier})
    if not user:
        raise HTTPException(status_code=404, detail='user does not exist.')
    else:
        cursor = db.coin_wallets.find(
            {'ownerId': user_identifier}).sort('network_name', 1)
        docs = await cursor.to_list(length=6)
        return docs
