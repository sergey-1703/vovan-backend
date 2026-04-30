from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from app.security.token_manager import get_id_by_token
from app.tools.config import security
from app.db.db_manager import get_users_by_query, get_user_by_id, change_attribute_by_id, user_is_banned

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Пользователи"],
    responses={404: {"description": "Not found"}},
)


@router.get("/search/{query}/{limit}/{offset}")
def search(query: str, limit: int, token: HTTPAuthorizationCredentials = Depends(security), offset: int = 0):
    current_user_id = get_id_by_token(token.credentials)
    if not get_user_by_id(current_user_id):
         raise HTTPException(status_code=401, detail="Unauthorized")
    if user_is_banned(current_user_id):
        raise HTTPException(status_code=403, detail="User banned")
    return serialize_users(get_users_by_query(query,limit,current_user_id, offset))


@router.get("/me")
def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)):
    current_user_id = get_id_by_token(token.credentials)
    user = get_user_by_id(current_user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if user_is_banned(current_user_id):
        raise HTTPException(status_code=403, detail="User banned")
    return serialize_user(user)

@router.patch("/me")
def change_user_attribute(attribute: str, value: str, token: HTTPAuthorizationCredentials = Depends(security)):
    current_user_id = get_id_by_token(token.credentials)
    user = get_user_by_id(current_user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if attribute == "id":
        raise HTTPException(status_code=400, detail="Invalid argument")
    if user_is_banned(current_user_id):
        raise HTTPException(status_code=403, detail="User banned")
    change_attribute_by_id(current_user_id, attribute, value)
    return serialize_user(get_user_by_id(current_user_id))


@router.get("/search/{user_id}")
def get_user(user_id: int, token: HTTPAuthorizationCredentials = Depends(security)):
    current_user_id = get_id_by_token(token.credentials)
    if not get_user_by_id(current_user_id):
        raise HTTPException(status_code=401, detail="Unauthorized")
    if user_is_banned(current_user_id):
        raise HTTPException(status_code=403, detail="User banned")
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return serialize_user(user)


def serialize_user(user):
    return {
        "id": user[0],
        "login": user[1],
        "nickname": user[2],
        "about": user[4]
    }


def serialize_users(users):
    return [{
        "id": user[0],
        "login": user[1],
        "nickname": user[2]
    } for user in users]