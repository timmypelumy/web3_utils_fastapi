from fastapi import FastAPI
from routers import exchanges, users, wallets, security,  authentication
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


@app.get('/ping', description='Check API server status', tags=["Check API server status"])
async def ping():
    return {
        "{0}_says".format(settings.app_name): "(v1) to the Moon!"
    }

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
    tags=['Users'],

)


app.include_router(
    router=authentication.router,
    prefix='/api/v1',
    tags=['Authentication'],

)


app.include_router(
    router=wallets.router,
    prefix='/api/v1',
    tags=['Wallets']
)


app.include_router(
    router=exchanges.router,
    prefix='/api/v1',
    tags=['Exchange and Conversion']
)


app.include_router(
    router=security.router,
    prefix='/api/v1',
    tags=['Security [ Testing only ]']
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
