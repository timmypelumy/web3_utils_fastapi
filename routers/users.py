from time import time
from uuid import uuid4
from fastapi import APIRouter,  HTTPException, BackgroundTasks, Depends, Query
from models.user import RSAkeypairDBModel, UserInModel, UserOutModel, UserDBModel, WalletPhrase
from models.wallet import CoinWalletModelDB
from config import db, settings
from datetime import datetime
from datetime import datetime
from uuid import uuid4
from lib.wallets import bitcoin_wallet, secret_phrase, litecoin_wallet, ethereum_wallet, celo_wallet, polygon_wallet, binance_wallet, ropsten_wallet, binance_testnet_wallet, bitcoin_testnet, polygon_mumbai_wallet
from passlib.context import CryptContext
from nanoid import generate
from slugify import slugify
from lib.security.hashing import password_management
from dependencies.security import get_exchange_keys_raw, get_logged_in_active_user
from lib import constants
from lib.security.encryption.rsa import core as core_rsa, keypair as keypair_rsa
from lib.security.encryption.fernet.core import encrypt as fernet_encrypt, decrypt as fernet_decrypt


router = APIRouter(
    prefix='/users',
    responses={
        404: {"description": "This path does not exist in router `users` "}
    }
)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


# Helpers

def create_username(name: str):
    slugified_name = slugify(name,  replacements=[['-', '_']])
    surfix = generate(size=8)
    return "{0}_{1}".format(slugified_name, surfix)


def get_hash(text):
    return pwd_context.hash((text))


# Backkground tasks
async def create_wallets(new_user: UserOutModel, backup_phrase, seed):

    bitcoin_wallet_info = bitcoin_wallet.generate_bitcoin_wallet(
        backup_phrase, new_user.username)

    bitcoin_testnet_wallet_info = bitcoin_testnet.generate_bitcoin_testnet_wallet(
        backup_phrase, new_user.username)

    litecoin_wallet_info = litecoin_wallet.generate_litecoin_wallet(
        backup_phrase, new_user.username)

    ethereum_wallet_info = ethereum_wallet.generate_ethereum_wallet(
        backup_phrase, new_user.username)

    polygon_wallet_info = polygon_wallet.generate_polygon_wallet(
        backup_phrase, new_user.username)

    polygon_mumbai_wallet_info = polygon_mumbai_wallet.generate_polygon_mumbai_wallet(
        backup_phrase, new_user.username)

    binance_wallet_info = binance_wallet.generate_binance_wallet(
        backup_phrase, new_user.username)

    binance_testnet_wallet_info = binance_testnet_wallet.generate_binance_testnet_wallet(
        backup_phrase, new_user.username)

    celo_wallet_info = celo_wallet.generate_celo_wallet(
        backup_phrase, new_user.username)

    # TEST WALLETS

    ropsten_wallet_info = ropsten_wallet.generate_ropsten_wallet(
        backup_phrase, new_user.username)

    # solana_wallet_info = solana_wallet.generate_solana_wallet(
    #     seed, new_user.username)

    bitcoin_account_db = CoinWalletModelDB(
        coinName='Bitcoin',
        coinTicker='BTC',
        coinDescription="Bitcoin Protocol",
        created=datetime.now().timestamp(),
        derivationPath=bitcoin_wallet_info['path'],
        lastUpdated=datetime.now().timestamp(),
        networkId=None,
        networkName=constants.TransactionNetworks.bitcoin,
        address=bitcoin_wallet_info['address'],
        ownerId=new_user.identifier,
        networkDisplayName="Bitcoin Protocol",


    )

    litecoin_account_db = CoinWalletModelDB(
        coinName='Litecoin',
        coinTicker='LTC',
        coinDescription="Litecoin Protocol",
        created=datetime.now().timestamp(),
        derivationPath=litecoin_wallet_info['path'],
        lastUpdated=datetime.now().timestamp(),
        networkId=None,
        networkName=constants.TransactionNetworks.litecoin,
        address=litecoin_wallet_info['address'],
        ownerId=new_user.identifier,
        networkDisplayName="Litecoin Protocol",


    )

    binance_account_db = CoinWalletModelDB(
        coinName='Smartchain',
        coinTicker='BNB',
        coinDescription="Binance Smartchain",
        created=datetime.now().timestamp(),
        derivationPath=binance_wallet_info['path'],
        lastUpdated=datetime.now().timestamp(),
        networkId=56,
        networkName=constants.TransactionNetworks.binance,
        address=binance_wallet_info['address'],
        ownerId=new_user.identifier,
        networkDisplayName="Binance Smartchain Network",


    )

    ethereum_account_db = CoinWalletModelDB(
        coinName='Ether',
        coinTicker='ETH',
        coinDescription="Ethereum",
        created=datetime.now().timestamp(),
        derivationPath=ethereum_wallet_info['path'],
        lastUpdated=datetime.now().timestamp(),
        networkId=1,
        networkName=constants.TransactionNetworks.ethereum,
        address=ethereum_wallet_info['address'],
        ownerId=new_user.identifier,
        networkDisplayName="Ethereum Network",


    )

    polygon_account_db = CoinWalletModelDB(
        coinName='Matic',
        coinTicker='MATIC',
        coinDescription="Polygon",
        created=datetime.now().timestamp(),
        derivationPath=polygon_wallet_info['path'],
        lastUpdated=datetime.now().timestamp(),
        networkId=1,
        networkName=constants.TransactionNetworks.polygon,
        address=polygon_wallet_info['address'],
        ownerId=new_user.identifier,
        networkDisplayName="Polygon Network",

    )

    celo_account_db = CoinWalletModelDB(
        coinName='Celo',
        coinTicker='CELO',
        coinDescription="Celo",
        created=datetime.now().timestamp(),
        derivationPath=celo_wallet_info['path'],
        lastUpdated=datetime.now().timestamp(),
        networkId=42220,
        networkName=constants.TransactionNetworks.celo,
        networkDisplayName="Celo Network",
        address=celo_wallet_info['address'],
        ownerId=new_user.identifier,

    )

    # TEST NETS

    ropsten_account_db = CoinWalletModelDB(
        coinName='RopstenETH',
        coinTicker='RopstenETH',
        coinDescription="Ropsten Ethereum",
        created=datetime.now().timestamp(),
        derivationPath=ropsten_wallet_info['path'],
        lastUpdated=datetime.now().timestamp(),
        networkId=3,
        networkName=constants.TransactionNetworks.ropsten,
        address=ropsten_wallet_info['address'],
        ownerId=new_user.identifier,
        networkDisplayName="Ropsten Network",
        is_testnet=True


    )

    bitcoin_testnet_account_db = CoinWalletModelDB(
        coinName='TestBitcoin',
        coinTicker='TestBitcoin',
        coinDescription="Test Bitcoin",
        created=datetime.now().timestamp(),
        derivationPath=bitcoin_testnet_wallet_info['path'],
        lastUpdated=datetime.now().timestamp(),
        networkId=None,
        networkName=constants.TransactionNetworks.bitcoin_testnet,
        address=bitcoin_testnet_wallet_info['address'],
        ownerId=new_user.identifier,
        networkDisplayName="Bitcoin Testnet Network",
        is_testnet=True

    )

    polygon_mumbai_account_db = CoinWalletModelDB(
        coinName='MumbaiMatic',
        coinTicker='MumbaiMatic',
        coinDescription="Mumbai Matic",
        created=datetime.now().timestamp(),
        derivationPath=polygon_mumbai_wallet_info['path'],
        lastUpdated=datetime.now().timestamp(),
        networkId=80001,
        networkName=constants.TransactionNetworks.polygon_mumbai,
        address=polygon_mumbai_wallet_info['address'],
        ownerId=new_user.identifier,
        networkDisplayName="Polygon Mumbai",
        is_testnet=True
    )

    binance_testnet_account_db = CoinWalletModelDB(
        coinName='TestBNB',
        coinTicker='TestBNB',
        coinDescription="Test BNB",
        created=datetime.now().timestamp(),
        derivationPath=binance_testnet_wallet_info['path'],
        lastUpdated=datetime.now().timestamp(),
        networkId=44787,
        networkName=constants.TransactionNetworks.binance_testnet,
        address=binance_testnet_wallet_info['address'],
        ownerId=new_user.identifier,
        networkDisplayName="Binance Test Network",
        is_testnet=True

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
        polygon_account_db.dict(),

        # TEST NETS

        polygon_mumbai_account_db.dict(),
        binance_testnet_account_db.dict(),
        bitcoin_testnet_account_db.dict(),
        ropsten_account_db.dict()

    ])


@router.post('', response_model=UserOutModel)
async def create_user(userData: UserInModel, background_tasks: BackgroundTasks):
    data = userData.dict()

    while True:
        username = create_username(data['display_name'])
        existingUser = await db.users.find_one({username: username})
        if not existingUser:

            backup = secret_phrase.generate_secret_phrase()
            passphrase = backup['passphrase']
            seed = backup['seed']
            new_keypair = keypair_rsa.generate_rsa_keypair()

            identifier = str(uuid4())

            encrypted_password = fernet_encrypt(
                [settings.master_encryption_key, ], data=password_management.generate_password().encode())
            encrypted_passphrase = fernet_encrypt(
                [settings.master_encryption_key, ], data=passphrase.encode())

            new_user = UserDBModel(**data, identifier=identifier,
                                   username=username, created=datetime.now().timestamp(),
                                   last_updated=datetime.now().timestamp(),
                                   password=encrypted_password.decode(),
                                   passphrase=encrypted_passphrase.decode()
                                   )

            await db.users.insert_one(new_user.dict())

            new_rsa_db = RSAkeypairDBModel(
                user_identifier=new_user.identifier,
                created=time(),
                encrypted_private=fernet_encrypt(
                    [settings.master_encryption_key, ], new_keypair['private'].encode()),
                encrypted_public=fernet_encrypt(
                    [settings.master_encryption_key, ], new_keypair['public'].encode())
            )

            await db.rsa_keypairs.insert_one(new_rsa_db.dict())

            background_tasks.add_task(
                create_wallets,  new_user=new_user, backup_phrase=passphrase, seed=seed)

            return new_user

        else:
            raise HTTPException(
                status_code=400, detail='Username exists already.')


@router.get('/fetch-user', response_model=UserOutModel)
async def fetch_user_by_user_identifier(user_identifier: str = Query(min_length=32, max_length=48)):
    user = await db.users.find_one({'identifier': user_identifier})
    if not user:
        raise HTTPException(
            status_code=404, detail='User with ID {0} does not exist'.format(user_identifier))
    else:
        return user


@router.post('/retreive-passphrase', response_model=WalletPhrase, description="Fetch user's account passphrase. ")
async def fetch_wallet_passphrase(logged_in_user: UserDBModel = Depends(get_logged_in_active_user)):

    exchange_keys = await get_exchange_keys_raw(logged_in_user)

    decrypted_phrase = fernet_decrypt(
        [settings.master_encryption_key, ], logged_in_user.passphrase.encode())

    keypair = keypair_rsa.load_rsa_keypair({
        # 'private': exchange_keys['key'],
        'public': exchange_keys['peer_key'].decode()
    })
    rsa_encrypted_passphrase = core_rsa.encrypt_rsa(
        keypair['public'], decrypted_phrase)

    if decrypted_phrase:

        return {
            "encrypted_passphrase": rsa_encrypted_passphrase.hex(),

        }

    return None
