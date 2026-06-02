from fastapi import APIRouter
import json

router = APIRouter(
    prefix="/api/v1",
    tags=["API"],
    responses={404: {"description": "Not found"}},
)

@router.get("/hash/{value}")
def hash_value(value: str):
    return {
        "request": value,
        "result": hash(value)
    }

@router.get("/about")
def get_about():
    with open('../about.json', encoding="utf-8") as f:
        return json.load(f)