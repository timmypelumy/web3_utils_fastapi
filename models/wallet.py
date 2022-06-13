from pydantic import BaseModel, Field, AnyUrl
from typing import List
from config import db


class CoinWalletModel(BaseModel):
    coin_name: str = Field(alias='coinName', min_length=3)
    coin_ticker: str = Field(alias='coinTicker', min_length=2)
    coin_description: str | None = Field(alias='coinDescription', default=None)
    coin_logo_url: AnyUrl
    network_name: str = Field(alias='networkName', min_length=3)
    derivation_path:  str = Field(alias='derivationPath', min_length=3)
    created: float
    last_updated: float = Field(alias='lastUpdated')
    mainnet_network_id: int = Field(alias='mainnetNetworkId', gt=0)
    testnet_network_id: int = Field(alias='testnetNetworkId', gt=0)
    ownerId: str = Field(min_length=48)
    address: str = Field(min_length=32)
    public_key: str = Field(alias='publickey', min_length=32)
    pk_hash: str = Field(alias='pkHash',
                         title="Hash value of the wallet's private key", min_length=2048)

    def is_owner(self, identifier):
        return self.ownerId == identifier

    async def get_owner(self):
        return await db.users.find_one({'identifier': self.ownerId})

    class Config:
        allow_population_by_field_name = True


class CoinWalletModelDB(CoinWalletModel):
    mainnet_rpc_endpoints:  List[AnyUrl] = Field(alias='mainnetRpcEndpoints')
    testnet_rpc_endpoints:  List[AnyUrl] = Field(alias='testnetRpcEndpoints')

    class Config:
        allow_population_by_field_name = True
