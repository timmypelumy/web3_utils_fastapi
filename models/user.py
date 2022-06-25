from pydantic import BaseModel, Field
from typing import Union


class UserBaseModel(BaseModel):
    display_name: str = Field(
        alias='displayName', min_length=1, max_length=32, description="User display name")
    platform_info: Union[str, None] = Field(alias='platformInfo', default=None)

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
    phrase_hash: str = Field(alias='phraseHash', min_length=32)
    passphrase: str = Field(min_length=32)

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


class Token(BaseModel):
    token_type: str = Field(alias='tokenType')
    access_token: str = Field(alias='accessToken')
