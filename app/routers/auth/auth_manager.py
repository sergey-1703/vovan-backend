from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.security.password_hash import hash_password, verify_password
from app.security.token_manager import create_token
from app.db.db_manager import add_user, get_user_attribute_by_login, user_exists, user_is_banned
from app.tools.config import get_max_password_length, get_min_password_length
from app.tools.extensions import check_user_is_banned

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Авторизация"],
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
    return create_response(token)


@router.post("/login/", status_code=200)
def login(user_login: str, password: str):
    if (not user_exists(user_login) or not
    verify_password(password, get_user_attribute_by_login(user_login, "password_hash"))):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user_id = get_user_attribute_by_login(user_login, "id")
    check_user_is_banned(user_id)
    token = create_token(user_id)
    return create_response(token)


def create_response(token: str):
    response = JSONResponse({
        "access_token": token
    })
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=False,
        secure=False,
        samesite="lax"
    )
    return response