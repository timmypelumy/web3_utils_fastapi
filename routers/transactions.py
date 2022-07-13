from lib import constants
from lib.wallets import ethereum_wallet, binance_wallet, celo_wallet, bitcoin_wallet, polygon_wallet, litecoin_wallet
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from config import db
from models.transactions import AuthorizeTransactionOutputModel, CreateTransactionInputModel, CreateTransactionOutputModel, TransactionInputModel, TransactionModel, AuthorizeTransactionInputModel
from lib.security.encryption.rsa import core as core_rsa, keypair as keypair_rsa
from dependencies.security import get_logged_in_active_user, get_exchange_keys
from models.user import UserDBModel
from typing import Any, Dict
from config import settings


router = APIRouter(
    prefix='/transactions',
    responses={
        404: {"description": "Resource does not exist"}
    }
)


@router.post('/create', response_model=CreateTransactionOutputModel, )
async def create_new_transaction(tx_data: CreateTransactionInputModel,  user: UserDBModel = Depends(get_logged_in_active_user), exchange_keys: Dict[str, str] = Depends(get_exchange_keys)):

    tx = TransactionInputModel(**tx_data.dict()).dict()

    tx.update({
        'uid': str(tx['uid']),
        'from_user_id': str(user.identifier),
        'to_user_id': str(tx_data.to_user_id)
    })

    await db.tx_buffers.insert_one(tx)

    saved_buffer = await db.tx_buffers.find_one({'uid': tx['uid']})

    if saved_buffer:

        return {
            'network_name': tx_data.network_name,
            'tx_uid': tx['uid'],
        }

    else:

        raise HTTPException(status_code=400, detail='')


@router.post('/authorize', response_model=AuthorizeTransactionOutputModel)
async def authorize_transaction(tx_info:  AuthorizeTransactionInputModel,  background_tasks: BackgroundTasks, user: UserDBModel = Depends(get_logged_in_active_user), exchange_keys: Dict = Depends(get_exchange_keys)):
    uid = str(tx_info.tx_uid)
    encrypted_passphrase = tx_info.encrypted_passphrase

    keypair = keypair_rsa.load_rsa_keypair({
        'private': exchange_keys['key'].decode(),
        # 'public': exchange_keys['public_key']
    })
    decrypted_passphrase = core_rsa.decrypt_rsa(
        keypair['private'], bytes.fromhex(encrypted_passphrase)).decode()

    tx = await db.tx_buffers.find_one({'uid': uid})

    if not tx:

        raise HTTPException(
            status_code=404, detail='No transaction matched the UID')

    else:

        if tx['from_user_id'] != user.identifier:
            raise HTTPException(status_code=403, detail="Invalid operation")

        task = None
        network = tx['network_name']

        if network == constants.ETHEREUM_MAINNET:
            # task = ethereum_wallet.send_ethereum_transaction

            # background_tasks.add_task(
            #     task, passphrase=decrypted_passphrase, tx=tx)

            tx_hash = ethereum_wallet.send_ethereum_transaction(
                tx, passphrase=decrypted_passphrase)

            return {
                'tx_uid': uid,
                'network_name': network,
                'tx_hash': tx_hash
            }

        else:

            raise HTTPException(status_code=403, detail="Invalid network")


@ router.post('/gas-station')
def fetch_network_gas_fee(user: UserDBModel = Depends(get_logged_in_active_user), exchange_keys: Dict[str, str] = Depends(get_exchange_keys)):
    pass
