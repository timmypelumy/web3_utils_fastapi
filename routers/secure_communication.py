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
