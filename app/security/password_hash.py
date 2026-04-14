from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"])

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, password_hash: str):
    return pwd_context.verify(password, password_hash)