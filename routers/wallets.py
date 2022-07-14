from typing import Dict, List
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Body
from config import settings
from web3 import Web3
from time import sleep
from models.wallet import FetchBalanceInputModel, FetchBalanceOutputModel
from lib.wallets import celo_wallet, polygon_wallet, ethereum_wallet, bitcoin_wallet, litecoin_wallet, binance_wallet, ropsten_wallet
from lib import constants


router = APIRouter(
    prefix='/wallets',
    responses={
        404: {"description": "Resource does not exist"}
    }
)


@router.post('/fetch-balance', response_model=FetchBalanceOutputModel, description='Fetch an address balance from the corresponding network, `networkName` can be celo, ethereum, binance, and so on.  ')
async def fetch_wallet_balance(body: FetchBalanceInputModel = Body()):
    address = body.address
    network_name = body.network_name

    balance = None

    if network_name == constants.ETHEREUM_MAINNET:
        balance = ethereum_wallet.get_balance(address)

        return {
            'balance': balance,
            'networkName': 'Ethereum',
            'address': address,
            'denomination': 'wei'

        }

    if network_name == constants.BINANCE_MAINNET:
        balance = binance_wallet.get_balance(address)

        return {
            'balance': balance,
            'networkName': 'Binance',
            'address': address,
            'denomination': 'wei'

        }

    if network_name == constants.POLYGON_MAINNET:

        balance = polygon_wallet.get_balance(address)

        return {
            'balance': balance,
            'networkName': 'Polygon',
            'address': address,
            'denomination': 'wei'

        }

    if network_name == constants.CELO_MAINNNET:
        balance = celo_wallet.get_balance(address)

        return {
            'balance': balance,
            'networkName': 'celo',
            'address': address,
            'denomination': 'wei'

        }

    if network_name.lower() == constants.LITECOIN_MAINNET:
        balance = litecoin_wallet.get_balance(address)
        return {
            'balance': balance,
            'networkName': 'litecoin',
            'address': address,
            'denomination': 'litoshi'

        }

    if network_name.lower() == constants.BITCOIN_MAINNET:
        balance = bitcoin_wallet.get_balance(address)
        return {

            'balance': balance,
            'networkName': 'bitcoin',
            'address': address,
            'denomination': 'satoshi'
        }

    if network_name.lower() == constants.ROPSTEN_TESTNET:
        balance = ropsten_wallet.get_balance(address)
        return {

            'balance': balance,
            'networkName': 'ropsten',
            'address': address,
            'denomination': 'wei'
        }

    # print(balance, network_name)


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
            network_name = data['network_name']
            room_id = 'LIVE_BALANCES_{0}'.format(network_name)
            manager.add_room(room_id)

            manager.add_to_room(
                room_id=room_id, websocket=websocket, partcipant_data=data)

    except WebSocketDisconnect:
        # manager.remove_from_room(room_id=room_id, websocket=websocket)
        manager.disconnect(websocket)
