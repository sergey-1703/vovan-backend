from fastapi import HTTPException
from app.db.db_manager import get_user_by_id, user_is_banned


def check_auth(user_id):
    if not get_user_by_id(user_id):
        raise HTTPException(status_code=401, detail="Unauthorized")
    check_user_is_banned(user_id)


def check_user_is_banned(user_id):
    if user_is_banned(user_id):
        raise HTTPException(status_code=403, detail="User banned")