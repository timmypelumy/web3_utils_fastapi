from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from lib import constants
from models.files import *
from config import db
from lib.security.hashing.password_management import generate_random_chars
import requests
from config import settings


router = APIRouter(
    prefix='/static',
    responses={
        404: {"description": "Resource does not exist"}
    }
)


@router.post('/profile-photo', response_model=ProfilePhotoModel)
async def upload_profile_photo(photo: UploadFile = File(),  uid: str = Form(min_length=32, max_length=128), tag: Union[str, None] = Form(default=None), filename: Union[str, None] = Form(default=None), ):

    existing_photo = await db.profile_photos.find_one({'uid': uid})

    if existing_photo:

        return existing_photo

    else:

        custom_filename = None

        if filename:
            custom_filename = filename
        else:
            custom_filename = photo.filename

        try:
            response = requests.post(
                '{0}/api/v0/add'.format(settings.ipfs_node_url), files={'fileOne': photo.file})

        except Exception as e:
            print('\n\nIPFS ERROR: ',  e, '\n\n')
            raise HTTPException(
                status_code=500, detail="Unable to save file ")

        else:

            if not response.ok:
                print(response.status_code, response.text)
                raise HTTPException(
                    status_code=500, detail="Unable to save file ")

            result = response.json()

            photo_model = ProfilePhotoModel(
                uid=uid, tag=tag, filename=custom_filename, uri=result['Hash'],
                url='{0}/{1}'.format(
                    settings.ipfs_read_nodes['cloudflare'], result['Hash'])
            )

            inserted_doc = await db.profile_photos.insert_one(photo_model.dict())

            return photo_model.dict()
