from typing import Dict, List
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Body
from config import settings
from web3 import Web3
from time import sleep
from models.wallet import GetBalanceInputModel, GetBalanceOutputModel
from lib import binance_wallet, celo_wallet, polygon_wallet, ethereum_wallet, bitcoin_wallet, litecoin_wallet


router = APIRouter(
    prefix='/conversions',
    responses={
        404: {"description": "Resource does not exist"}
    }
)


@router.post('/fiat', description="Convert any valid crypto asset to its equivalent value in any other valid fiat currency.")
def fiat_conversions():
    pass
