from pydantic import BaseModel, Field, AnyUrl, validator, root_validator
from typing import Union
from config import db
from web3 import Web3
from bitcoinlib.keys import Address, BKeyError, EncodingError


ALLOWED_NETWORK_IDS = {1, 56, 137, 42220}
ALLOWED_NETWORK_NAMES = {'binance', 'ethereum',
                         'celo', 'litecoin', 'bitcoin', 'polygon'}


def is_valid_address(address: str):
    return Web3().isChecksumAddress(address)


def is_valid_bitcoin_based_address(address: str, network: str):
    try:
        parsed_address = Address.parse(address=address)
        data = parsed_address.as_dict()
        # print(data)
        return data['network'].lower() == network.lower()

    except (BKeyError, EncodingError) as Exception:
        print(Exception)
        return False


class GetBalanceInputModel(BaseModel):
    network_id: Union[int, None] = Field(alias='networkId', default=None, gt=0)
    network_name: str = Field(alias='networkName', default=None)
    address: str = Field(min_length=24)

    @validator('address', always=True)
    def is_valid_address(cls, v, values):
        if values.get('network_id', None) and not is_valid_address(v):
            raise ValueError('Invalid EVM Wallet Address')

        if values.get('network_name', None) and not is_valid_bitcoin_based_address(v, values['network_name']):
            raise ValueError('Invalid {0} Wallet Address'.format(
                values["network_name"]))

        return v

    @validator('network_id',  always=True)
    def is_valid_network_id(cls, v):

        if v and not ALLOWED_NETWORK_IDS.issuperset([v, ]):
            raise ValueError("Invalid Network ID")
        return v

    @validator('network_name',  always=True)
    def is_valid_network_name(cls, v: str):

        if v and not ALLOWED_NETWORK_NAMES.issuperset([v.lower(), ]):
            raise ValueError("Invalid Network Name")
        return v

    @root_validator()
    def either_name_or_network_id(cls,  values):
        if not values.get('network_name', None) and not values.get('network_id', None):
            raise ValueError("Either Network ID or Network Name is required")
        return values

    class Config:
        allow_population_by_field_name = True


class GetBalanceOutputModel(GetBalanceInputModel):
    balance: float = Field(ge=0)
    denomination: Union[str, None] = Field(default=None)

    class Config:
        allow_population_by_field_name = True


class CoinBalanceSubscriptionModel(BaseModel):
    network_id: int = Field(alias='networkId', gt=0)
    client_id:  str = Field(alias='clientId')

    class Config:
        allow_population_by_field_name = True


class CoinWalletModel(BaseModel):
    identifier: str = Field(description="Unique identifier ",)
    coin_name: str = Field(alias='coinName', min_length=3)
    coin_ticker: str = Field(alias='coinTicker', min_length=2)
    coin_description: Union[str, None] = Field(
        alias='coinDescription', default=None)
    coin_logo_url: Union[None, AnyUrl] = Field(
        alias='coinLogoUrl', default=None)
    network_name: str = Field(alias='networkName', min_length=3)
    derivation_path:  Union[str, None] = Field(
        alias='derivationPath', min_length=3)
    created: float
    last_updated: float = Field(alias='lastUpdated')
    network_id: Union[int, None] = Field(alias='networkId', gt=0, default=None)
    ownerId: str = Field(min_length=32)
    address: str = Field(min_length=32)
    pk_hash: str = Field(alias='pkHash',
                         title="Hash value of the wallet's private key", min_length=56)

    def is_owner(self, identifier):
        return self.ownerId == identifier

    async def get_owner(self):
        return await db.users.find_one({'identifier': self.ownerId})

    class Config:
        allow_population_by_field_name = True


class CoinWalletModelDB(CoinWalletModel):
    pass

    class Config:
        allow_population_by_field_name = True
