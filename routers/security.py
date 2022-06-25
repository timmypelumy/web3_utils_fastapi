from fastapi import APIRouter
from codecs import decode
from lib.security.encryption import generate_symmetric_key, symmetric, keypair, asymmetric
from models.security import *


router = APIRouter(
    prefix='/security',
    responses={
        404: {"description": "Resource does not exist"}
    }
)


@router.get('/encryption/new-symmetric-key', description=" [ ⚠⚠⚠ TESTING ONLY ‼ ]  Generate a new key for symmetric encryption", response_model=SymmetricKeyModel)
def get_symmetric_key():

    key = generate_symmetric_key.generate_key()
    # print(len(key))

    return {
        "key": key
    }


@router.post('/encryption/symmetric-encryption', description=" [ ⚠⚠⚠ TESTING ONLY ‼ ]  Encrypt data using symmetric encryption", response_model=EncryptionOutputModel)
def symmetric_encryption(body:  SymmetricEncryptionInputModel):

    cipher = symmetric.encrypt([body.key], body.data.encode())

    return {
        "cipher_text": cipher.decode()
    }


@router.post('/encryption/symmetric-decryption', description=" [ ⚠⚠⚠ TESTING ONLY ‼ ]  Decrypt data using symmetric encryption", response_model=DecryptionOutputModel)
def symmetric_decryption(body:  SymmetricDecryptionInputModel):

    data = symmetric.decrypt([body.key], body.token.encode())

    if data:

        return {
            "data": data.decode()}

    else:
        return None


@router.post('/encryption/rotate-token-symmetric', description=" [ ⚠⚠⚠ TESTING ONLY ‼ ]  Rotate a token using a new key", response_model=EncryptionOutputModel)
def symmetric_rotate_token(body:  SymmetricRotateTokenInputModel):

    token = symmetric.rotate([body.new_key], body.token.encode())

    if token:

        return {
            "cipher_text": token.decode()}

    else:
        return None


@router.get('/encryption/new-X25519-keypair', description=" [ ⚠⚠⚠ TESTING ONLY ‼ ]  Generate a new keypair for X25519 asymmetric encryption", response_model=AsymmetricKeypairModel)
def get_X25519_asymmetric_keypair():

    key = keypair.generate_keypair(serialized=True)

    return {
        "private": key["private"], "public": key["public"]}


@router.post('/encryption/X25519-encryption', description=" [ ⚠⚠⚠ TESTING ONLY ‼ ]  Encrypt data using X25519 asymmetric encryption", response_model=EncryptionOutputModel)
def X25519_asymmetric_encryption(body:  AsymmetricEncryptionInputModel):

    private = keypair.load_private_key(body.private_key.encode())
    peer_public = keypair.load_public_key(body.peer_public_key.encode())

    shared = asymmetric.get_shared_key(private, peer_public)
    derived = asymmetric.get_derived_key(
        shared, body.salt.encode(), body.info.encode())

    cipher = asymmetric.encrypt(derived, body.data.encode())

    return {
        "cipher_text": cipher.hex(),

    }


@router.post('/encryption/X25519-decryption', description=" [ ⚠⚠⚠ TESTING ONLY ‼ ]  Decrypt data using X25519 asymmetric encryption", response_model=DecryptionOutputModel)
def X25519_asymmetric_decryption(body: AsymmetricDecryptionInputModel):

    private = keypair.load_private_key(body.private_key.encode())
    peer_public = keypair.load_public_key(body.peer_public_key.encode())

    shared = asymmetric.get_shared_key(private, peer_public)
    derived = asymmetric.get_derived_key(
        shared, body.salt.encode(), body.info.encode())

    data = asymmetric.decrypt(derived, bytes.fromhex(body.token))

    if data:

        return {
            "data": data.decode()}

    else:
        return None
