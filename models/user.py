from pydantic import BaseModel, Field
from uuid import UUID
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

    class Config:
        allow_population_by_field_name = True


class UserDBModel(UserOutModel):
    phrase_hash: str = Field(alias='phraseHash', min_length=56)

    class Config:
        allow_population_by_field_name = True


class UserInModel(UserBaseModel):
    pass


class Token(BaseModel):
    token_type: str = Field(alias='tokenType')
    access_token: str = Field(alias='accessToken')
