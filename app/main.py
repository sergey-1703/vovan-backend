from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from app.routers.auth import auth_manager
from app.routers.api import base_api
from app.routers.users import user_manager
from app.db.db_main import db_init
import uvicorn

app = FastAPI()
app.include_router(auth_manager.router)
app.include_router(base_api.router)
app.include_router(user_manager.router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/")
def root():
    return "null"

if __name__ == "__main__":
    db_init()
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)