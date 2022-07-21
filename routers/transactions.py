from lib import constants
from lib.wallets import ethereum_wallet, binance_wallet, celo_wallet, bitcoin_wallet, polygon_wallet, litecoin_wallet, ropsten_wallet, binance_testnet_wallet, polygon_mumbai_wallet
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


async def initiate_transaction(task, tx_uid, raw_tx):

    try:
        task(raw_tx)
    except Exception as e:
        print(e)

    else:
        await db.tx_buffers.update_one({'uid': tx_uid}, {'$set': {'is_authorized': True}})


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

        raise HTTPException(status_code=500, detail='')


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
            raise HTTPException(
                status_code=403, detail="Current user and Transaction `from_user_id` field do not match")

        if tx['is_authorized']:
            raise HTTPException(
                status_code=403, detail='Transaction already authorized')

        if tx['has_expired']:
            raise HTTPException(
                status_code=403, detail='Transaction has expired')

        task = None
        network = tx['network_name']

        if network == constants.TransactionNetworks.ethereum:
            task = ethereum_wallet.send_ethereum_transaction
        elif network == constants.TransactionNetworks.ropsten:
            task = ropsten_wallet.send_ropsten_transaction
        elif network == constants.TransactionNetworks.binance_testnet:
            task = binance_testnet_wallet.send_binance_testnet_transaction
        elif network == constants.TransactionNetworks.binance:
            task = binance_wallet.send_binance_transaction
        elif network == constants.TransactionNetworks.polygon:
            task = polygon_wallet.send_polygon_transaction
        elif network == constants.TransactionNetworks.polygon_mumbai:
            task = polygon_mumbai_wallet.send_polygon_mumbai_transaction
        elif network == constants.TransactionNetworks.bitcoin:
            task = bitcoin_wallet.send_bitcoin_transaction

        if task:
            if network == constants.TransactionNetworks.bitcoin or network == constants.TransactionNetworks.litecoin:
                task_result = task(
                    tx=tx, passphrase=decrypted_passphrase, username=user.identifier)
            else:
                task_result = task(tx=tx, passphrase=decrypted_passphrase)

            background_tasks.add_task(initiate_transaction, tx_uid=uid,
                                      task=task_result['send_transaction'], raw_tx=task_result['raw_tx'])

            return {
                'tx_uid': uid,
                'network_name': network,
                'tx_hash': task_result['tx_hash']
            }
        else:
            raise HTTPException(status_code=403, detail="Invalid network")


@router.post('/gas-station')
def fetch_network_gas_fee(user: UserDBModel = Depends(get_logged_in_active_user), exchange_keys: Dict[str, str] = Depends(get_exchange_keys)):
    pass
