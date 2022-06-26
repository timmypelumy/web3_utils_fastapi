from time import time
from fastapi import APIRouter, Query, HTTPException, Depends
from config import db, settings
from lib.security.encryption import pipeline_encryption, symmetric
from models.security import *
from fastapi.security import OAuth2PasswordRequestForm
from dependencies.security import authenticate_client, generate_access_token, get_exchange_keys_raw, get_logged_in_active_user
from models.user import UserDBModel, UserOutModel


router = APIRouter(
    prefix='/secure-comm',
    responses={
        404: {"description": "Resource does not exist"}
    }
)


@router.post("/login", response_model=Token)
async def login_for_access_token(form: OAuth2PasswordRequestForm = Depends()):

    exchange_keys = await get_exchange_keys_raw(logged_in_user=None, replacement_id=form.username)

    decrypted_password = pipeline_encryption.pipeline_decrypt(
        exchange_keys['key'], exchange_keys['peer_key'], salt=settings.encryption_salt, info=''.encode(), cipher=bytes.fromhex(form.password), halfway=True)

    user = await authenticate_client(form.username, decrypted_password)

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password", headers={
                            'WWW-Authenticate': 'Bearer'})

    access_token = generate_access_token({'sub': user['identifier']})

    encrypted_access_token = symmetric.encrypt(
        [settings.master_encryption_key, ],  access_token.encode()).decode()

    # encrypted_access_token = access_token

    return {
        "access_token": encrypted_access_token,
        "access_token_unencrypted": access_token,
        'token_type': 'bearer'

    }


@router.post('/new-ecdh-session', description="Perform a new ECDH key exchange : This involves exchange of public keys between the server and the client for encrypted communication", response_model=ECDHKeyExchangeOutputModel)
async def perform_key_exchange(body: ECDHKeyExchangeInputModel, user_identifier: str = Query(description='The `identifier` of the user requesting for a key exchange.')):

    await db.ecdh_sessions.delete_many({"client_id": user_identifier})
    exchange_keys = await get_exchange_keys_raw(logged_in_user=None, replacement_id=user_identifier, strict=False)
    user = await db.users.find_one({'identifier': user_identifier})

    ecdh_session_db = ECDHKeyExchangeDBModel(
        peer_public_key=symmetric.encrypt(
            [settings.master_encryption_key, ], body.peer_public_key.encode()),
        client_id=user_identifier,
        timestamp=time()
    )
    await db.ecdh_sessions.insert_one(ecdh_session_db.dict())

    if user['password_sent']:
        return {
            "peer_public_key": exchange_keys['public_key'],
        }

    else:
        decrypted_password = symmetric.decrypt(
            [settings.master_encryption_key, ], user['password'].encode())

        ecdh_encrypted_password = pipeline_encryption.pipeline_encrypt(
            exchange_keys['key'], body.peer_public_key.encode(), salt=settings.encryption_salt, info=''.encode(), data=decrypted_password, halfway=True
        )
        return {
            "peer_public_key": exchange_keys['public_key'],
            "password": ecdh_encrypted_password.hex()
        }


@router.post('/fetch-wallet-passphrase', description="Fetch wallet passphrase for client user. All fields are encrypted. [ Left out some fields since encryption/decryption isn't ready on client side yet ] ")
async def fetch_wallet_passphrase(logged_in_user: UserDBModel = Depends(get_logged_in_active_user)):

    exchange_keys = await get_exchange_keys_raw(logged_in_user)

    decrypted_phrase = symmetric.decrypt(
        [settings.master_encryption_key, ], logged_in_user['passphrase'].encode())

    if decrypted_phrase and exchange_keys:

        return {
            "passphrase": decrypted_phrase,
            "encrypted_passphrase": pipeline_encryption.pipeline_encrypt(private_key=exchange_keys['key'], peer_public_key=exchange_keys['peer_key'], salt=settings.encryption_salt, info=''.encode(), halfway=True, data=decrypted_phrase).hex()
        }

    return None


@router.post('/fetch-current-user', description="Fetch the currently logged in user.", response_model=UserOutModel)
def fetch_current_user(logged_in_user: UserDBModel = Depends(get_logged_in_active_user)):
    return logged_in_user
