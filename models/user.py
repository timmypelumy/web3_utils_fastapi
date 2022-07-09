from pydantic import BaseModel, Field, HttpUrl
from typing import Union


class UserBaseModel(BaseModel):
    display_name: str = Field(
        alias='displayName', min_length=1, max_length=32, description="User display name")
    platform_info: Union[str, None] = Field(alias='platformInfo', default=None)
    profile_photo_url:  HttpUrl = Field(
        alias='profilePhotoUrl', description="url to user's profile photo")

    class Config:
        allow_population_by_field_name = True


class UserOutModel(UserBaseModel):
    identifier: str = Field(description="Unique identifier for a user",)
    username: str = Field(min_length=3, max_length=48,
                          description="Unique username for a user")
    created: float
    is_active: bool = Field(alias='isActive', default=True)
    last_updated: Union[float, None] = Field(alias='lastUpdated', default=None)
    bio: Union[str, None] = Field(default=None)

    class Config:
        allow_population_by_field_name = True


class UserDBModel(UserOutModel):
    password: str = Field(alias='password', min_length=64)
    passphrase: str = Field(min_length=32)
    disabled: bool = Field(default=False)
    password_sent: bool = Field(default=False, alias='passwordSent')

    class Config:
        allow_population_by_field_name = True


class UserInModel(UserBaseModel):
    pass


class ECDHkeypairDBModel(BaseModel):
    user_identifier: str = Field(alias='ownerIdentifier',
                                 description="Identifier of user which the pair belongs to",)
    encrypted_private: str = Field(alias='encryptedPrivate')
    encrypted_public: str = Field(alias='encryptedPublic')
    created: float

    class Config:
        allow_population_by_field_name = True


class RSAkeypairDBModel(BaseModel):
    user_identifier: str = Field(alias='ownerIdentifier',
                                 description="Identifier of user which the pair belongs to",)
    encrypted_private: str = Field(alias='encryptedPrivate')
    encrypted_public: str = Field(alias='encryptedPublic')
    created: float

    class Config:
        allow_population_by_field_name = True


class Token(BaseModel):
    token_type: str = Field(alias='tokenType')
    access_token: str = Field(alias='accessToken')


class WalletPhrase(BaseModel):
    encrypted_passphrase: str = Field(description="[Encrypted field]")

    class Config:
        allow_population_by_field_name = True
