from time import time
from fastapi import APIRouter, Query, HTTPException
from config import db, settings
from lib.security.encryption import pipeline_encryption, symmetric
from models.security import *


router = APIRouter(
    prefix='/secure-comm',
    responses={
        404: {"description": "Resource does not exist"}
    }
)


@router.post('/new-ecdh-session', description="Perform a new ECDH key exchange : This involves exchange of public keys between the server and the client for encrypted communication", response_model=ECDHKeyExchangeOutputModel)
async def perform_key_exchange(body: ECDHKeyExchangeInputModel):

    await db.ecdh_sessions.delete_many({"client_id": body.identifier})

    server_ecdh = await db.ecdh_keypairs.find_one({"user_identifier": body.identifier})

    if not server_ecdh:
        raise HTTPException(status_code=404, detail='User not found')

    ecdh_session_db = ECDHKeyExchangeDBModel(
        peer_public_key=symmetric.encrypt(
            [settings.master_encryption_key, ], body.peer_public_key.encode()),
        client_id=body.identifier,
        timestamp=time()
    )
    await db.ecdh_sessions.insert_one(ecdh_session_db.dict())

    public_key = symmetric.decrypt(
        [settings.master_encryption_key, ], server_ecdh['encrypted_public'].encode())

    if public_key:

        return {
            "peer_public_key": public_key

        }

    else:

        raise HTTPException(status_code=401, detail="")


@router.post('/fetch-wallet-passphrase', description="Fetch wallet passphrase for client user. All fields must be encrypted both on the server and client.")
async def fetch_wallet_passphrase(lookup: str = Query(min_length=24, description=" `lookup` query parameter : This is the identifier of the client user ")):

    user = await db.users.find_one({'identifier': lookup})

    if not user:
        raise HTTPException(status_code=404, detail='user not found')

    server_ecdh = await db.ecdh_keypairs.find_one({"user_identifier": lookup})

    if not server_ecdh:
        raise HTTPException(status_code=404, detail='User ECDH not found')

    user_ecdh_session = await db.ecdh_sessions.find_one({"client_id": lookup})

    if not user_ecdh_session:
        raise HTTPException(status_code=400, detail='No User ECDH found')

    decrypted_phrase = symmetric.decrypt(
        [settings.master_encryption_key, ], user['passphrase'].encode())

    if decrypted_phrase:

        peer_public_key = symmetric.decrypt(
            [settings.master_encryption_key, ], user_ecdh_session['peer_public_key'].encode())
        private_key = symmetric.decrypt(
            [settings.master_encryption_key, ], server_ecdh['encrypted_private'].encode())

        if peer_public_key and private_key:

            return {
                "passphrase": decrypted_phrase,
                "encrypted_passphrase": pipeline_encryption.pipeline_encrypt(private_key=private_key, peer_public_key=peer_public_key, salt=''.encode(), info=''.encode(), halfway=True, data=decrypted_phrase).hex()
            }

    return None
