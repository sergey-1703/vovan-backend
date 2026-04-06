from fastapi import APIRouter
from app.schemas.user import UserCreate
from app.security.password_hash import hash_password, verify_password
from app.security.token_manager import create_token

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Пользователи"],
    responses={404: {"description": "Not found"}},
)


@router.post("/register/", status_code=201)
def registration(user_info: UserCreate):
    hashed_password = hash_password(user_info.password)
    # заносим данные в БД

@router.post("/login/", status_code=200)
def login(user_info: UserCreate):
    # db_user = await get_user_by_login(user.login)

    # if not db_user or not verify_password(user_info.password, db_user["password_hash"]):
    #     raise HTTPException(status_code=401, detail="Invalid credentials")
    #
    # token = create_token(db_user["id"])

    return {"access_token": "token"}