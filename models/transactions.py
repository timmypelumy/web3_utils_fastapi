from ctypes import Union
from datetime import datetime
from pydantic import BaseModel, Field, validator
from lib import constants
from uuid import UUID
from .wallet import get_timestamp, get_uuid4, is_valid_bitcoin_based_address, is_valid_evm_based_address
from typing import Union


class CreateTransactionInputModel(BaseModel):
    network_name:  constants.TransactionNetworks = Field(
        alias='networkName', description="Network the transaction took place on e.g Ethereum, Celo.")
    value: float = Field(ge=0)
    to_user_id: UUID = Field(alias='toUserId')
    is_contract_call: bool = Field(default=False, alias='isContractCall')
    from_address: str = Field(alias='fromAddress')
    to_address: str = Field(alias='toAddress')
    unit: constants.NetworkSubunits
    from_user_id: Union[UUID, None] = Field(alias='fromUserId', default=None)

    @validator('to_address', 'from_address', always=True)
    def is_valid_address(cls, v, values):

        if not 'network_name' in values:
            raise ValueError("Invalid network_name specified")

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

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {UUID: lambda v: str(v)}
        use_enum_values = True


class CreateTransactionOutputModel(BaseModel):
    network_name:  constants.TransactionNetworks = Field(
        alias='networkName', description="Network to place the transaction on e.g Ethereum, Celo.")
    tx_uid: UUID = Field(
        description="Transaction unique identifier ", alias='txUid')

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {UUID: lambda v: str(v)}
        use_enum_values = True


class AuthorizeTransactionInputModel(BaseModel):
    tx_uid: UUID = Field(
        description="Transaction unique identifier ", alias='txUid')
    encrypted_passphrase: str = Field(alias='encryptedPassphrase',
                                      min_length=24, description='User Passphrase, needed to sign transactions. [Encrypted] ')

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {UUID: lambda v: str(v)}
        use_enum_values = True


class AuthorizeTransactionOutputModel(BaseModel):

    tx_hash: str = Field(alias='txHash')
    tx_uid: UUID = Field(alias='txUid')
    network_name: constants.TransactionNetworks = Field(alias='networkName')

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {UUID: lambda v: str(v)}
        use_enum_values = True


class BaseTransactionModel(BaseModel):
    uid: UUID = Field(description="Unique identifier ",
                      default_factory=get_uuid4)
    created: float = Field(gt=0, default_factory=get_timestamp)
    network_name:  constants.TransactionNetworks = Field(
        alias='networkName', description="Network the transaction took place on e.g Ethereum, Celo.")
    value: float = Field(ge=0)
    to_user_id: UUID = Field(alias='toUserId')
    is_contract_call: bool = Field(default=False, alias='isContractCall')
    from_address: str = Field(alias='fromAddress')
    to_address: str = Field(alias='toAddress')
    unit: constants.NetworkSubunits

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {UUID: lambda v: str(v)}
        use_enum_values = True

    # @validator('network_name', always=True)
    # def is_valid_network_name(cls, v, values):
    #     if constants.VALID_NETWORKS.issuperset([v.lower(), ]):
    #         return v
    #     else:
    #         raise ValueError("Invalid network name")

    @validator('to_address', 'from_address', always=True)
    def is_valid_address(cls, v, values):

        if not 'network_name' in values:
            raise ValueError("Invalid network_name specified")

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


class TransactionModel(BaseTransactionModel):
    block_timestamp: float = Field(gt=0, alias='blockTimestamp')
    mined: bool = Field(default=False)
    dropped: bool = Field(default=False)
    transaction_hash: str = Field(min_length=24, alias='transactionHash')
    nonce: str = Field()
    pending: bool = Field(default=True)
    is_hidden: bool = Field(default=False, alias='isHidden')
    from_user_id: UUID = Field(alias='fromUserId')
    last_updated: float = Field(
        gt=0, default_factory=datetime.utcnow, alias='lastUpdated')


class TransactionInputModel(BaseTransactionModel):
    is_authorized: bool = Field(
        default=False, alias='isAuthorized')
    has_expired: bool = Field(default=False, alias='hasExpired')
    from_user_id: Union[UUID, None] = Field(alias='fromUserId', default=None)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {UUID: lambda v: str(v)}
        arbitrary_types_allowed = True
        use_enum_values = True
