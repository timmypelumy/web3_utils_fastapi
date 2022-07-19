from typing import Dict, Union
from pydantic import BaseModel, Field,  HttpUrl
from .transactions import get_timestamp


class ProfilePhotoUpload(BaseModel):
    uid: str = Field(min_length=32, max_length=128)
    tag: str = Field(default=None)
    filename: Union[str, None]

    # @validator('resource')
    # def is_valid_image(cls, v: UploadFile,  values):
    #     content_type = v.content_type
    #     ct1, ct2 = content_type.lower().split("/")

    #     extension_is_valid = constants.ALLOWED_IMAGE_EXTENSIONS.count(ct2) != 0
    #     file_type_is_valid = ct1 == 'image'

    #     if extension_is_valid and file_type_is_valid:
    #         return v

    #     else:

    #         raise ValueError("Unsupported MIME type")


class ProfilePhotoModel(ProfilePhotoUpload):
    created: float = Field(default_factory=get_timestamp)
    uri: str
    url: Union[None, HttpUrl] = Field(default=None)
