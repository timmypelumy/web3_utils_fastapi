from pydantic import BaseSettings
import motor.motor_asyncio
from typing import Union


class AppSettings(BaseSettings):
    app_name: str = "Beepo"
    db_url: str = 'mongodb://localhost:27017'
    secret_key: str = "@#$%^Ygtrdytfyiguo^Ou67798ouyxSD%IU7t65srdtuyiCXYTDFIUGOUC*^DDs57du6yiUSYDU"
    hash_algorithm: str = "HS256"
    access_token_expiration_in_minutes: int = 60
    client_url: str = 'http://localhost:3000'
    heroku_app_url: Union[str, None] = None


settings = AppSettings()
db_client = motor.motor_asyncio.AsyncIOMotorClient(settings.db_url)
db = db_client.beepo_db
