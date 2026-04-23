from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from starlette.responses import JSONResponse

from app.security.token_manager import get_id_by_token
from app.tools.config import security
from app.db.db_manager import get_users_by_query, user_exists

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Пользователи"],
    responses={404: {"description": "Not found"}},
)


@router.get("/search/{query}/{limit}/{offset}")
def search(query: str, limit: int, token: HTTPAuthorizationCredentials = Depends(security), offset: int = 0):
    current_user_id = get_id_by_token(token.credentials)
    # if not user_exists(current_user_id):
    #     raise HTTPException(status_code=404, detail="User not found")
    users = get_users_by_query(query, limit, current_user_id, offset)
    return JSONResponse(status_code=200, content=users)


@router.get("/{user_id}")
def get_user(user_id: int):
    user = 1 # get_users_by_query(query)
    return user


@router.get("/me")
def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)):
    return