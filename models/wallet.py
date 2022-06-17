from pydantic import BaseModel, Field, AnyUrl
from typing import Union
from config import db


class GetBalanceInputModel(BaseModel):
    address: str = Field(min_length=24)
    network_id: Union[int, None] = Field(alias='networkId', default=None, gt=0)
    network_name: str = Field(alias='networkName', default=None)
    denomination: Union[str, None] = Field(default=None)

    class Config:
        allow_population_by_field_name = True


class GetBalanceOutputModel(BaseModel):
    address: str = Field(min_length=24)
    network_id: Union[int, None] = Field(alias='networkId', default=None, gt=0)
    network_name: str = Field(alias='networkName', default=None)
    balance: float = Field(ge=0)

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
