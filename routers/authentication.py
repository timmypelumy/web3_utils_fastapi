from time import time
from fastapi import APIRouter, Query, HTTPException, Depends
from config import db, settings
from lib.security.encryption.misc import symmetric
from lib.security.encryption.rsa import core as core_rsa, keypair as keypair_rsa
from models.security import *
from fastapi.security import OAuth2PasswordRequestForm
from dependencies.security import authenticate_client, generate_access_token, get_exchange_keys_raw, get_logged_in_active_user
from models.user import UserDBModel, UserOutModel
from lib.security.hashing import password_management


router = APIRouter(
    prefix='/auth',
    responses={
        404: {"description": "Resource does not exist"}
    }
)


@router.post('/new-key-exchange-session', description="Perform a new RSA key exchange : This involves exchange of public keys between the server and the client for encrypted communication", response_model=RSAKeyExchangeOutputModel)
async def perform_key_exchange(body: RSAKeyExchangeInputModel, user_identifier: str = Query(description='The `identifier` of the user requesting for a key exchange.')):

    await db.key_exchange_sessions.delete_many({"client_id": user_identifier})
    exchange_keys = await get_exchange_keys_raw(logged_in_user=None, replacement_id=user_identifier, strict=False)
    user = await db.users.find_one({'identifier': user_identifier})

    key_exchange_session_db = RSAKeyExchangeDBModel(
        peer_public_key=symmetric.encrypt(
            [settings.master_encryption_key, ], body.peer_public_key.encode()),
        client_id=user_identifier,
        timestamp=time()
    )
    await db.key_exchange_sessions.insert_one(key_exchange_session_db.dict())

    if user['password_sent']:
        return {
            "peer_public_key": exchange_keys['public_key'],
        }

    else:
        decrypted_password = symmetric.decrypt(
            [settings.master_encryption_key, ], user['password'].encode())

        keypair = keypair_rsa.load_rsa_keypair({
            # 'private': exchange_keys['key'],
            'public': body.peer_public_key
        })
        rsa_encrypted_password = core_rsa.encrypt_rsa(
            keypair['public'], decrypted_password)

        return {
            "peer_public_key": exchange_keys['public_key'],
            "password": rsa_encrypted_password.hex()
        }


@router.post("/login", response_model=Token)
async def login_for_access_token(form: OAuth2PasswordRequestForm = Depends()):

    exchange_keys = await get_exchange_keys_raw(logged_in_user=None, replacement_id=form.username)

    keypair = keypair_rsa.load_rsa_keypair({
        'private': exchange_keys['key'].decode(),
        # 'public': exchange_keys['public_key']
    })

    decrypted_password = core_rsa.decrypt_rsa(
        keypair['private'],  bytes.fromhex(form.password))

    user = await authenticate_client(form.username, decrypted_password)

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password", headers={
                            'WWW-Authenticate': 'Bearer'})

    if not user['password_sent']:
        password_hash = password_management.hash_with_scrypt(
            settings.encryption_salt, decrypted_password).hex()
        await db.users.update_one({"identifier": user['identifier']}, {"$set":  {"password_sent": True, "password": password_hash}})

    access_token = generate_access_token({'sub': user['identifier']})

    encrypted_access_token = symmetric.encrypt(
        [settings.master_encryption_key, ],  access_token.encode()).decode()

    return {
        "access_token": encrypted_access_token,
        'token_type': 'bearer'

    }


@router.post('/fetch-current-user', description="Fetch the currently logged in user.", response_model=UserOutModel)
def fetch_current_user(logged_in_user: UserDBModel = Depends(get_logged_in_active_user)):
    return logged_in_user
