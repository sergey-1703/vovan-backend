import random
from jose import jwt
from app.tools.config import get_secret_key, get_algorithm

SECRET_KEY = get_secret_key()
ALGORITHM = get_algorithm()


def create_token(user_id: int):
    payload = {
        "user_id": user_id,
        "salt": random.randint(1, 100_000)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_id_by_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)["user_id"]