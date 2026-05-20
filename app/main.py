from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPAuthorizationCredentials
from app.security.token_manager import get_id_by_token
from app.routers.auth import auth_manager
from app.routers.chats import chats_manager
from app.tools.config import security
from app.routers.api import base_api
from app.routers.users import user_manager
from app.db.db_main import db_init, add_test_data, get_user_by_id
import platform
import uvicorn

app = FastAPI()
app.include_router(auth_manager.router)
app.include_router(base_api.router)
app.include_router(user_manager.router)
app.include_router(chats_manager.router)

@app.get("/")
def root(token: HTTPAuthorizationCredentials = Depends(security)):
    if not token:
        return RedirectResponse("/login")
    current_user_id = get_id_by_token(token.credentials)
    user = get_user_by_id(current_user_id)
    if not user:
        return RedirectResponse("/login")
    return RedirectResponse("/chats")

if __name__ == "__main__":
    db_init()
    if platform.system() != "Linux":
        add_test_data()
        print("Added test data")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)