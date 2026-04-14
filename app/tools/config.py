from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="../../test_cfg_change_this_in_prod.env")

def get_secret_key():
    return os.getenv("SECRET_KEY")

def get_algorithm():
    return os.getenv("ALGORITHM")

def get_lifetime_of_token():
    return os.getenv("ACCESS_TOKEN_EXPIRE_HOURS")

def  get_db_host():
    return os.getenv("DB_HOST")

def  get_db_name():
    return os.getenv("DB_NAME")

def  get_db_user():
    return os.getenv("DB_USER")

def get_db_password():
    return os.getenv("DB_PASSWORD")
