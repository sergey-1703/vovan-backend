from fastapi import APIRouter, WebSocket, Depends, HTTPException, WebSocketDisconnect
from fastapi.security import HTTPAuthorizationCredentials
from app.db.db_manager import get_user_by_id, user_is_banned, get_user_chats, get_messages, \
    track_message_and_create_chat, track_message, get_chat_by_users
from app.security.token_manager import get_id_by_token
from app.tools.config import security

router = APIRouter(
    prefix="/api/v1/chats",
    tags=["Чаты"],
    responses={404: {"description": "Not found"}},
)
active_connections = {}

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, chat_id: int, need_track_message: bool):
    global active_connections
    token = websocket.query_params.get("token")
    current_user_id = get_id_by_token(token)
    user = get_user_by_id(current_user_id)
    if not user:
        await websocket.close(code=1008)
    if user_is_banned(current_user_id):
        await websocket.close(code=1008)
    await websocket.accept()
    active_connections[current_user_id] = websocket
    await broadcast({
        "type": "status",
        "user_id": current_user_id,
        "online": True
    })
    try:
        while True:
            data = await websocket.receive_json()
            receiver_id = data["to"]
            msg = data["message"]
            event = {
                "type": "new_message" if need_track_message else "new_chat",
                "chat_id": chat_id,
                "from": current_user_id,
                "message": msg
            }
            if receiver_id in active_connections:
                await active_connections[receiver_id].send_json(event)
            if need_track_message:
                track_message(current_user_id, chat_id, msg)

    except WebSocketDisconnect:
        active_connections.pop(current_user_id, None)
        await broadcast({
            "type": "status",
            "user_id": current_user_id,
            "online": False
        })


@router.get("/get_chats/")
def get_all_user_chats(limit: int, token: HTTPAuthorizationCredentials = Depends(security), offset: int = 0):
    current_user_id = get_id_by_token(token.credentials)
    if not get_user_by_id(current_user_id):
        raise HTTPException(status_code=401, detail="Unauthorized")
    if user_is_banned(current_user_id):
        raise HTTPException(status_code=403, detail="User banned")
    return [serialize_chat(chat) for chat in get_user_chats(current_user_id, limit, offset)]


@router.get("/get_messages/")
def get_messages_in_chat(chat_id: int, limit: int, token: HTTPAuthorizationCredentials = Depends(security), offset: int = 0):
    current_user_id = get_id_by_token(token.credentials)
    if not get_user_by_id(current_user_id):
        raise HTTPException(status_code=401, detail="Unauthorized")
    if user_is_banned(current_user_id):
        raise HTTPException(status_code=403, detail="User banned")
    return [serialize_msg(msg) for msg in get_messages(chat_id, limit, offset)]


@router.get("/check_chat_is_exists_by_receiver_id/")
def check_chat_is_exists_by_receiver_id(receiver_id: int, token: HTTPAuthorizationCredentials = Depends(security)):
    current_user_id = get_id_by_token(token.credentials)
    if not get_user_by_id(current_user_id):
        raise HTTPException(status_code=401, detail="Unauthorized")
    if user_is_banned(current_user_id):
        raise HTTPException(status_code=403, detail="User banned")
    chat_id = get_chat_by_users(current_user_id, receiver_id)
    if chat_id is None:
        raise HTTPException(status_code=404, detail="Chat not found")
    return {"chat_id": chat_id}


@router.post("/create_chat_if_not_exists/")
def create_chat_if_not_exists(first_msg_text: str, receiver_id: int, token: HTTPAuthorizationCredentials = Depends(security)):
    current_user_id = get_id_by_token(token.credentials)
    if not get_user_by_id(current_user_id):
        raise HTTPException(status_code=401, detail="Unauthorized")
    if user_is_banned(current_user_id):
        raise HTTPException(status_code=403, detail="User banned")
    return {"chat_id" : track_message_and_create_chat(current_user_id, receiver_id, first_msg_text)}


@router.get("/status/{user_id}")
def get_status(user_id: int, token: HTTPAuthorizationCredentials = Depends(security)):
    current_user_id = get_id_by_token(token.credentials)
    if not get_user_by_id(current_user_id):
        raise HTTPException(status_code=401, detail="Unauthorized")
    if user_is_banned(current_user_id):
        raise HTTPException(status_code=403, detail="User banned")
    return {
        "online": user_id in active_connections
    }


async def broadcast(data):
    for ws in active_connections.values():
        await ws.send_json(data)


def serialize_msg(msg):
    return {
        "sender_id": msg[0],
        "msg_body": msg[1],
        "created_at": msg[2]
    }


def serialize_chat(chat):
    return {
        "chat_id": chat[0],
        "receiver_id": chat[1],
        "receiver_nickname": chat[2],
        "last_msg": chat[3]
    }
