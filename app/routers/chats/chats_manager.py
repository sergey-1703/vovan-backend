from fastapi import APIRouter, WebSocket, Depends, HTTPException, WebSocketDisconnect
from fastapi.security import HTTPAuthorizationCredentials
from app.db.db_manager import get_user_by_id, user_is_banned, get_user_chats, get_messages # , chat_is_exists, track_message, track_message_and_create_chat
from app.security.token_manager import get_id_by_token
from app.tools.config import security

router = APIRouter(
    prefix="/api/v1/chats",
    tags=["Чаты"],
    responses={404: {"description": "Not found"}},
)
active_connections = {}

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: HTTPAuthorizationCredentials = Depends(security)):
    global active_connections
    current_user_id = get_id_by_token(token.credentials)
    user = get_user_by_id(current_user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if user_is_banned(current_user_id):
        raise HTTPException(status_code=403, detail="User banned")
    await websocket.accept()
    active_connections[current_user_id] = websocket
    try:
        while True:
            data = await websocket.receive_json()
            receiver_id = data["to"]
            if receiver_id in active_connections:
                await active_connections[receiver_id].send_json({
                    "from": current_user_id,
                    "message": data["message"]
                })

    except WebSocketDisconnect:
        active_connections.pop(current_user_id, None)


@router.get("/get_chats/{user_id}")
def get_all_user_chats(limit: int, token: HTTPAuthorizationCredentials = Depends(security), offset: int = 0):
    current_user_id = get_id_by_token(token.credentials)
    if not get_user_by_id(current_user_id):
        raise HTTPException(status_code=401, detail="Unauthorized")
    if user_is_banned(current_user_id):
        raise HTTPException(status_code=403, detail="User banned")
    return get_user_chats(current_user_id, limit, offset)


@router.get("/get_messages/{chat_id}")
def get_all_messages_in_chat(chat_id: int, limit: int, token: HTTPAuthorizationCredentials = Depends(security), offset: int = 0):
    current_user_id = get_id_by_token(token.credentials)
    if not get_user_by_id(current_user_id):
        raise HTTPException(status_code=401, detail="Unauthorized")
    if user_is_banned(current_user_id):
        raise HTTPException(status_code=403, detail="User banned")
    return get_messages(current_user_id, chat_id, limit, offset)