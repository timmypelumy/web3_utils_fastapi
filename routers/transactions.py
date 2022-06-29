from lib import constants
from lib.wallets import ethereum_wallet, binance_wallet, celo_wallet, bitcoin_wallet, polygon_wallet, litecoin_wallet
from fastapi import APIRouter, Depends, HTTPException
from config import db
from models.transactions import CreateTransactionOutputModel, TransactionInputModel, TransactionModel, AuthorizeTransactionInputModel
from lib.security.encryption import pipeline_encryption
from dependencies.security import get_logged_in_active_user, get_exchange_keys
from models.user import UserDBModel
from typing import Dict
from config import settings


router = APIRouter(
    prefix='/transactions',
    responses={
        404: {"description": "Resource does not exist"}
    }
)


@router.post('/create', response_model=CreateTransactionOutputModel, )
async def create_new_transaction(tx_data: TransactionInputModel,  user: UserDBModel = Depends(get_logged_in_active_user), exchange_keys: Dict[str, str] = Depends(get_exchange_keys)):

    tx = tx_data.dict()

    tx.update({
        'uid': str(tx_data.uid),
        'from_user_id': str(user.identifier),
        'to_user_id': str(tx_data.to_user_id)
    })

    await db.tx_buffers.insert_one(tx)

    saved_buffer = await db.tx_buffers.find_one({'uid': tx['uid']})

    if saved_buffer:

        return {
            'network_name': tx_data.network_name,
            'transaction_uid': tx_data.uid,
        }

    else:

        raise HTTPException(status_code=400, detail='')


@router.post('/authorize')
async def authorize_transaction(tx_info:  AuthorizeTransactionInputModel, user: UserDBModel = Depends(get_logged_in_active_user), exchange_keys: Dict[str, str] = Depends(get_exchange_keys)):
    uid = tx_info.uid
    passphrase = pipeline_encryption.pipeline_decrypt(
        exchange_keys['key'].encode(), exchange_keys['peer_key'].encode(), settings.encryption_salt, ''.encode(), bytes.fromhex(tx_info.encrypted_passphrase), halfway=True)

    tx = await db.tx_buffers.find_one({'uid': uid})

    if not tx:

        raise HTTPException(
            status_code=404, detail='No transaction matched the UID')

    else:

        if tx['from_user_id'] != user.identifier:
            raise HTTPException(status_code=403, detail="Invalid operation")

        # do stuff

        return None


@router.post('/gas-station')
def fetch_network_gas_fee(user: UserDBModel = Depends(get_logged_in_active_user), exchange_keys: Dict[str, str] = Depends(get_exchange_keys)):
    pass
