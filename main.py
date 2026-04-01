from fastapi import FastAPI
from routers.auth import auth_manager
from routers.api import base_api
import uvicorn

app = FastAPI()
app.include_router(auth_manager.router)
app.include_router(base_api.router)

@app.get("/")
def root():
    return {"Скоро здесь будет Vovan Messenger"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)