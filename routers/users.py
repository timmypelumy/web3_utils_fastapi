
from hashlib import new
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import Field
from models.user import UserInModel, UserOutModel, UserDBModel
from fastapi.encoders import jsonable_encoder
from config import db
from datetime import datetime, timedelta
from config import settings
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime
from uuid import uuid4
from lib import bitcoin_wallet, secret_phrase, litecoin_wallet, ethereum_wallet, binance_wallet, celo_wallet


router = APIRouter(
    prefix='/users',
    tags=['users'],
    responses={
        404: {"description": "User does not exist"}
    }
)


# Helpers

def create_username(name: str):
    name = ''.join(name.split(" "))
    time = ''.join(str(datetime.now().timestamp()).split('.'))
    return "{0}_{1}".format(name, time)


@router.post('', response_model=UserOutModel, response_model_exclude={'phrase_hash'})
async def create_user(userData: UserInModel):
    data = userData.dict()

    while True:
        username = create_username(data['display_name'])
        existingUser = await db.users.find_one({username: username})
        if not existingUser:
            new_user = UserDBModel(**data, identifier=str(uuid4()),
                                   username=username, created=datetime.now().timestamp())
            await db.users.insert_one(new_user.dict())

            backup_phrase = secret_phrase.generate_secret_phrase()

            bitcoin_wallet_info = bitcoin_wallet.generate_bitcoin_wallet(
                backup_phrase, new_user.username)

            lietcoin_wallet_info = litecoin_wallet.generate_litecoin_wallet(
                backup_phrase, new_user.username)

            ethereum_wallet_info = ethereum_wallet.generate_ethereum_wallet(
                backup_phrase, new_user.username)

            binance_wallet_info = binance_wallet.generate_binance_wallet(
                backup_phrase, new_user.username)

            celo_wallet_info = celo_wallet.generate_celo_wallet(
                backup_phrase, new_user.username)

            return jsonable_encoder(new_user)


@router.get('/{username}', response_model=UserOutModel)
async def get_user_by_username(username: str = Field(min_length=3, max_length=48)):
    user = await db.users.find_one({'username': username})
    if not user:
        raise HTTPException(status_code=404, detail='User does not exist.')
    else:
        return user
