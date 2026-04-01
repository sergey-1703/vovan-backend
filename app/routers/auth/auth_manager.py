from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
    responses={404: {"description": "Not found"}},
)


@router.get("/register/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]