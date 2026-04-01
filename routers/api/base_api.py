from fastapi import APIRouter

router = APIRouter(
    prefix="/api",
    tags=["API"],
    responses={404: {"description": "Not found"}},
)

@router.get("/hash/{value}")
def hash_value(value: str):
    return hash(value)