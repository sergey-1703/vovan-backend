from fastapi import APIRouter, Depends
from typing import Annotated
from app.security.token_manager import get_id_by_token
from app.main import oauth2_scheme

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Пользователи"],
    responses={404: {"description": "Not found"}},
)


@router.get("/search/{query}/{limit}/{offset}")
def search(token: Annotated[str, Depends(oauth2_scheme)], query: str, limit: int, offset: int = 0):
    current_user = get_id_by_token(token)
    users = []
    return users


@router.get("/{user_id}")
def get_user(user_id: int):
    user = 1 # get_users_by_query(query)
    return user


@router.get("/me")
def get_current_user(token: str = Depends(oauth2_scheme)):
    return