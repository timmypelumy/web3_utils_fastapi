from typing import Any, Dict, List
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Body
from pydantic import ValidationError
from config import settings
from web3 import Web3
from time import sleep
from models.wallet import GetBalanceInputModel, GetBalanceOutputModel
from lib import binance_wallet, celo_wallet, polygon_wallet, ethereum_wallet

ALLOWED_NETWORK_IDS = [1, 56, 137, 42220]


router = APIRouter(
    prefix='/wallets',
    responses={
        404: {"description": "Resource does not exist"}
    }
)


@router.post('/get-balance', response_model=GetBalanceOutputModel)
async def get_wallet_balance(body: GetBalanceInputModel = Body()):
    network_id = body.network_id
    address = body.address
    network_name = body.network_name

    if (not network_id) and (network_name != 'bitcoin' and network_name != 'litecoin'):
        raise ValidationError(['Network name is required when network ID is not applicable',
                              "Network must be either 'bitcoin' or 'litecoin' "], model=GetBalanceInputModel)

    if network_id:
        if(ALLOWED_NETWORK_IDS.index(network_id) == -1):
            raise ValidationError(['Invalid network ID',
                                   "Allowed network IDs are 1,56,137 and 4220' "], model=GetBalanceInputModel)

        is_valid_address = ethereum_wallet.is_valid_address(address)

        if not is_valid_address:
            raise ValidationError(['Invalid address for network with ID {0}'.format(
                network_id)], model=GetBalanceInputModel)

    balance = -1

    if network_id == 1:
        balance = ethereum_wallet.get_balance(address)

        return {
            'balance': balance,
            'networkName': 'Ethereum',
            'networkId': network_id,
            'address': address
        }

    if network_id == 56:
        balance = binance_wallet.get_balance(address)

        return {
            'balance': balance,
            'networkName': 'Binance',
            'networkId': network_id,
            'address': address
        }

    if network_id == 137:

        balance = polygon_wallet.get_balance(address)

        return {
            'balance': balance,
            'networkName': 'Polygon',
            'networkId': network_id,
            'address': address
        }

    if network_id == 42220:
        balance = celo_wallet.get_balance(address)

        return {
            'balance': balance,
            'networkName': 'celo',
            'networkId': network_id,
            'address': address
        }


class ConnnectionManager:
    def __init__(self):
        self.active_connections_map: Dict[str, WebSocket] = {}
        self.active_connections: List[WebSocket] = []
        self.rooms: Dict[str, Dict[str, Dict]] = {}
        self.providers = {
            1: Web3.HTTPProvider(settings.chain_nodes[1]['http']),
            56: Web3.HTTPProvider(settings.chain_nodes[56]['http']),
            42220: Web3.HTTPProvider(settings.chain_nodes[42220]['http']),
        }

    async def get_ganache_balances(self):
        room_id = 'LIVE_BALANCES_{0}'.format(5000)
        room = self.get_room(room_id)

        if not room:
            return

        web3 = Web3(self.providers[5000])

        while True:

            for client in room.values():

                address = client['address']

                balance = web3.eth.get_balance(address)

                await self.send_json({
                    "type": "BALANCE",
                    "address": address,
                    "value_in_wei": balance
                }, websocket=client['socket'])

            sleep(1)

    async def get_eth_balances(self):
        room_id = 'LIVE_BALANCES_{0}'.format(1)
        room = self.get_room(room_id)

        if not room:
            return

        web3 = Web3(self.providers[1])

        while True:

            for client in room.values():

                address = client['address']

                balance = web3.eth.get_balance(address)

                await self.send_json({
                    "type": "BALANCE",
                    "address": address,
                    "value_in_wei": balance
                }, websocket=client['socket'])

            sleep(1)

    def get_celo_balances(self):
        pass

    def get_bitcoin_balances(self):
        pass

    def get_litecoin_balances(self):
        pass

    def get_binance_balances(self):
        pass

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def get_room(self, room_id: str):
        return self.rooms[room_id]

    def add_room(self, room_id: str):
        room = self.rooms.get(room_id, None)

        if not room:
            self.rooms[room_id] = {}

    def remove_room(self, room_id: str):
        room = self.rooms.get(room_id, None)

        if room:
            self.rooms[room_id] = {}

    def _check_client_id(self, websocket: WebSocket, data: Dict):
        if not data.get('client_id', None):
            return False

        id = data['client_id']

        if self.active_connections_map.get(id, None):
            return True

        self.active_connections_map[id] = websocket

        return True

    def add_to_room(self, room_id: str, websocket: WebSocket, partcipant_data: Dict):

        if not self._check_client_id(websocket, partcipant_data):
            return

        partcipant_data['socket'] = websocket

        self.rooms[room_id][partcipant_data['client_id']] = partcipant_data

    def remove_from_room(self, room_id: str, client_id: str):
        self.rooms[room_id].pop(client_id, None)

    async def broadcast_to_room(self, room_id: str, json_data: Dict):
        for client in self.rooms[room_id].values():
            await client['socket'].send_json(json_data)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_json(self, json_data: Dict, websocket:  WebSocket):
        await websocket.send_json(json_data)

    async def broadcast(self, json_data: Dict):
        for connection in self.active_connections:
            await connection.send_json(json_data)


manager = ConnnectionManager()


@router.websocket('/subscribe-for-account-balances')
async def get_live_balances(websocket: WebSocket):

    await manager.connect(websocket)
    room_id = ''

    try:
        while True:

            data = await websocket.receive_json()
            network_id = data['network_id']
            room_id = 'LIVE_BALANCES_{0}'.format(network_id)
            manager.add_room(room_id)

            manager.add_to_room(
                room_id=room_id, websocket=websocket, partcipant_data=data)

    except WebSocketDisconnect:
        # manager.remove_from_room(room_id=room_id, websocket=websocket)
        manager.disconnect(websocket)
