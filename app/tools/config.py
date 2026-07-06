from dotenv import load_dotenv
from pathlib import Path
from fastapi.security import HTTPBearer
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent
env_file = BASE_DIR / ".env"
if env_file.exists():
    load_dotenv()
security = HTTPBearer()

def get_secret_key():
    return os.getenv("SECRET_KEY")

def get_algorithm():
    return os.getenv("ALGORITHM")

def  get_db_host():
    return os.getenv("DB_HOST")

def  get_db_name():
    return os.getenv("DB_NAME")

def  get_db_user():
    return os.getenv("DB_USER")

def get_db_password():
    return os.getenv("DB_PASSWORD")

def get_min_password_length():
    return int(os.getenv("MIN_PASSWORD_LENGTH"))

def get_max_password_length():
    return int(os.getenv("MAX_PASSWORD_LENGTH"))