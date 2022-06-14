from fastapi import APIRouter, WebSocket
from .wallets import router as walletRouter


router = APIRouter(
    tags=['Websocket endpoints'],
    responses={
        404: {"description": "Resource does not exist"}
    },

)


router.include_router(
    router=walletRouter,
    prefix='/wallets',

)


@router.websocket('/')
async def ping(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
