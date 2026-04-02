from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="../test_cfg_change_this_in_prod.env")

def get_secret_key():
    return os.getenv("SECRET_KEY")

def get_algorithm():
    return os.getenv("ALGORITHM")

def get_lifetime_of_token():
    return os.getenv("ACCESS_TOKEN_EXPIRE_HOURS")