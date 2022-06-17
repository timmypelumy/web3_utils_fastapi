from fastapi import FastAPI
from routers import users
from routers import wallets
# from routers.user import authenticate_user, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
# from models.user import Token
from fastapi.middleware.cors import CORSMiddleware
from config import settings


app = FastAPI()

origins = [
    settings.client_url,
    settings.heroku_app_url,
    'localhost:3000'
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    router=users.router,
    prefix='/api/v1',
    tags=['Users endpoints'],

)


app.include_router(
    router=wallets.router,
    prefix='/api/v1',
    tags=['Wallets endpoints']
)

# ---------------------
# Start Up and Shutdown events
# ---------------------


@app.on_event('startup')
def startup_event():
    print("\nApplication starting up...")


@app.on_event('shutdown')
def shutdown_event():
    print("\nApplication shutting down...")


# ? lOGIN URL


# @app.post("/api/v1/login", response_model= Token )
# @app.post("/login", response_model= Token )
# async def login_for_access_token( form : OAuth2PasswordRequestForm = Depends() ):
#     user = await authenticate_user(form.username, form.password)
#     if not user:
#         raise HTTPException(status_code=401, detail="Incorrect username or password", headers = {'WWW-Authenticate' : 'Bearer'})

#     access_token = create_access_token({ 'sub' : user.get('_id') })
#     return {
#         "accessToken" : access_token , 'tokenType'  :'bearer'
#     }


@app.get('/ping')
async def ping():
    return {
        "message": "It worked!",
        "allowed_origins": origins
    }
