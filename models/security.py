from pydantic import BaseModel, Field
from typing import Union


class Token(BaseModel):
    token_type: str = Field()
    access_token: str = Field()


class TokenData(BaseModel):
    user_id: str = Field(alias='userId')
    # expires : datetime

    class Config:
        allow_population_by_field_name = True


class SymmetricKeyModel(BaseModel):
    key: str = Field(min_length=44)


class SymmetricEncryptionInputModel(BaseModel):
    key: str = Field(min_length=44)
    data: str = Field()


class SymmetricDecryptionInputModel(BaseModel):
    key: str = Field(min_length=44)
    token: str


class SymmetricRotateTokenInputModel(BaseModel):
    new_key: str = Field(min_length=44, alias='newKey')
    token: str

    class Config:
        allow_population_by_field_name = True


class DecryptionOutputModel(BaseModel):
    data: str


class EncryptionOutputModel(BaseModel):
    cipher_text: str = Field(alias='cipherText')

    class Config:
        allow_population_by_field_name = True


class AsymmetricKeypairModel(BaseModel):
    private: bytes
    public: bytes


class AsymmetricEncryptionInputModel(BaseModel):
    private_key: str = Field(alias='privateKey')
    peer_public_key: str = Field(alias='peerPublicKey')
    salt: str
    info: str
    data: str

    class Config:
        allow_population_by_field_name = True


class RSAAsymmetricEncryptionInputModel(BaseModel):
    public_key: str = Field(alias='publicKey')
    message: str

    class Config:
        allow_population_by_field_name = True


class RSAAsymmetricDecryptionInputModel(BaseModel):
    private_key: str = Field(alias='privateKey')
    ciphertext: str

    class Config:
        allow_population_by_field_name = True


class RSASignInputModel(BaseModel):
    private_key: str = Field(alias='privateKey')
    message: str

    class Config:
        allow_population_by_field_name = True


class RSASignOutputModel(BaseModel):
    signature: str

    class Config:
        allow_population_by_field_name = True


class RSAVerifyInputModel(BaseModel):
    message: str
    signature: str
    public_key: str = Field(alias='publicKey')

    class Config:
        allow_population_by_field_name = True


class RSAVerifyOutputModel(BaseModel):
    is_valid_signature: bool

    class Config:
        allow_population_by_field_name = True


class AsymmetricDecryptionInputModel(BaseModel):
    private_key: str = Field(alias='privateKey')
    peer_public_key: str = Field(alias='peerPublicKey')
    salt: str
    info: str
    token: str

    class Config:
        allow_population_by_field_name = True


class ECDHKeyExchangeInputModel(BaseModel):
    peer_public_key: str = Field(alias='peerPublicKey')

    class Config:
        allow_population_by_field_name = True


class RSAKeyExchangeInputModel(BaseModel):
    peer_public_key: str = Field(alias='peerPublicKey')

    class Config:
        allow_population_by_field_name = True


class ECDHKeyExchangeOutputModel(BaseModel):
    peer_public_key: str = Field(alias='peerPublicKey')
    password: Union[str, None] = Field(
        min_length=128, default=None, description="[Encrypted field]")

    class Config:
        allow_population_by_field_name = True


class RSAKeyExchangeOutputModel(BaseModel):
    peer_public_key: str = Field(alias='peerPublicKey')
    password: Union[str, None] = Field(
        min_length=128, default=None, description="[Encrypted field]")

    class Config:
        allow_population_by_field_name = True


class ECDHKeyExchangeDBModel(BaseModel):
    peer_public_key: str = Field(alias='peerPublicKey')
    timestamp: float = Field(gt=0)
    client_id: str = Field(alias='clientId')

    class Config:
        allow_population_by_field_name = True


class RSAKeyExchangeDBModel(BaseModel):
    peer_public_key: str = Field(alias='peerPublicKey')
    timestamp: float = Field(gt=0)
    client_id: str = Field(alias='clientId')

    class Config:
        allow_population_by_field_name = True
