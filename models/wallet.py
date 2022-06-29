from datetime import datetime
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, AnyUrl, validator
from typing import Union
from config import db
from web3 import Web3
from bitcoinlib.keys import Address, BKeyError, EncodingError
from lib import constants


def get_uuid4():
    return str(uuid4())


def get_timestamp():
    return datetime.now().timestamp()


def is_valid_evm_based_address(address: str):
    return Web3().isChecksumAddress(address)


def is_valid_bitcoin_based_address(address: str, network: str):
    try:
        parsed_address = Address.parse(address=address)
        data = parsed_address.as_dict()
        return data['network'].lower() == network.lower()

    except (BKeyError, EncodingError) as Exception:
        print(Exception)
        return False


class FetchBalanceInputModel(BaseModel):
    network_name: constants.TransactionNetworks = Field(alias='networkName', )
    address: str = Field(min_length=24)

    # @validator('network_name',  always=True)
    # def is_valid_network_name(cls, v, values):

    #     if v and not constants.VALID_NETWORKS.issuperset([v.lower(), ]):
    #         raise ValueError("Invalid network name")
    #     return v

    @validator('address',  always=True)
    def is_valid_address(cls, v, values):

        if 'network_name' in values:
            network = values['network_name']

            if network == constants.TransactionNetworks.litecoin or network == constants.TransactionNetworks.bitcoin:

                if is_valid_bitcoin_based_address(v, network=network):
                    return v
                else:
                    raise ValueError("Invalid {0} address".format(network))

            else:
                if is_valid_evm_based_address(v):
                    return v
                else:
                    raise ValueError("Invalid {0} address".format(network))

        else:
            raise ValueError("Invalid network_name specified")

    class Config:
        allow_population_by_field_name = True
        use_enum_values = True


class FetchBalanceOutputModel(FetchBalanceInputModel):
    balance: float = Field(ge=0)
    denomination: Union[str, None] = Field(default=None)

    class Config:
        allow_population_by_field_name = True
        use_enum_values = True


class CoinBalanceSubscriptionModel(BaseModel):
    network_id: int = Field(alias='networkId', gt=0)
    client_id:  str = Field(alias='clientId')

    class Config:
        allow_population_by_field_name = True


class CoinWalletModel(BaseModel):
    uid: UUID = Field(description="Unique identifier ",
                      default_factory=get_uuid4)
    coin_name: str = Field(alias='coinName', min_length=3)
    coin_ticker: str = Field(alias='coinTicker', min_length=2)
    coin_description: Union[str, None] = Field(
        alias='coinDescription', default=None)
    coin_logo_url: Union[None, AnyUrl] = Field(
        alias='coinLogoUrl', default=None)
    network_name: constants.TransactionNetworks = Field(
        alias='networkName', min_length=3)
    network_display_name: str = Field(alias='networkDisplayName', min_length=8)
    derivation_path:  Union[str, None] = Field(
        alias='derivationPath', min_length=3)
    created: float = Field(default_factory=get_timestamp)
    last_updated: float = Field(
        alias='lastUpdated', default_factory=get_timestamp)
    network_id: Union[int, None] = Field(alias='networkId', gt=0, default=None)
    ownerId: str = Field(min_length=32)
    address: str = Field(min_length=32)

    def is_owner(self, identifier):
        return self.ownerId == identifier

    async def get_owner(self):
        return await db.users.find_one({'identifier': self.ownerId})

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {UUID: str}
        use_enum_values = True


class CoinWalletModelDB(CoinWalletModel):
    pass

    class Config:
        allow_population_by_field_name = True
        use_enum_values = True
