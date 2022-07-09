from fastapi import APIRouter


router = APIRouter(
    prefix='/secure-comm',
    responses={
        404: {"description": "Resource does not exist"}
    }
)
