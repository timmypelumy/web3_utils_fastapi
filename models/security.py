from pydantic import BaseModel, Field


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
    identifier: str

    class Config:
        allow_population_by_field_name = True


class ECDHKeyExchangeOutputModel(BaseModel):
    peer_public_key: str = Field(alias='peerPublicKey')

    class Config:
        allow_population_by_field_name = True


class ECDHKeyExchangeDBModel(BaseModel):
    peer_public_key: str = Field(alias='peerPublicKey')
    timestamp: float = Field(gt=0)
    client_id: str = Field(alias='clientId')

    class Config:
        allow_population_by_field_name = True
