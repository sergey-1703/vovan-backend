from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Пользователи"],
    responses={404: {"description": "Not found"}},
)


@router.get("/search/{query}")
def search(query: str):
    users = 1 # get_users_by_query(query)
    return users


@router.get("/{user_id}")
def get_user(user_id: int):
    user = 1 # get_users_by_query(query)
    return user


# @router.get("/me")
# def get_current_user(token: str = Depends(oauth2_scheme)):
#     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])