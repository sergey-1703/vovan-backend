from jose import jwt
from datetime import datetime, timedelta
from app.tools.config import get_secret_key, get_algorithm, get_lifetime_of_token

SECRET_KEY = get_secret_key()
ALGORITHM = get_algorithm()
ACCESS_TOKEN_LIFETIME = get_lifetime_of_token()


def create_token(user_id: int):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)