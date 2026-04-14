from fastapi import APIRouter, HTTPException
from app.security.password_hash import hash_password, verify_password
from app.security.token_manager import create_token
from app.db.db_manager import add_user, get_user_attribute_by_login, user_exists
from app.tools.config import get_max_password_length, get_min_password_length

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Пользователи"],
    responses={404: {"description": "Not found"}},
)


@router.post("/register/", status_code=201)
def registration(user_login: str, nickname: str, password: str):
    psd_len = len(password)
    if psd_len < get_min_password_length() or psd_len > get_max_password_length():
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if user_exists(user_login):
        raise HTTPException(status_code=409, detail="User already exists")
    hashed_password = hash_password(password)
    user_id = add_user(user_login, nickname, hashed_password, about="")
    token = create_token(user_id)
    return {"access_token": token}


@router.post("/login/", status_code=200)
def login(user_login: str, password: str):
    if (not user_exists(user_login) or not
    verify_password(password, get_user_attribute_by_login(user_login, "password_hash"))):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token(get_user_attribute_by_login(user_login, "id"))
    return {"access_token": token}