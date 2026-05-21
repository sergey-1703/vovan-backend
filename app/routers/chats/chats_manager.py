from fastapi import APIRouter, WebSocket, Depends, HTTPException, WebSocketDisconnect
from fastapi.security import HTTPAuthorizationCredentials
from app.db.db_manager import get_user_by_id, user_is_banned, get_user_chats, get_messages, \
    track_message_and_create_chat, track_message, get_chat_by_users, set_message_is_read, \
    get_first_message, set_messages_read_in_chat, set_all_messages_is_read
from app.security.token_manager import get_id_by_token
from app.tools.config import security
from app.tools.extensions import check_auth

router = APIRouter(
    prefix="/api/v1/chats",
    tags=["Чаты"],
    responses={404: {"description": "Not found"}},
)
active_connections = {}


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global active_connections
    token = websocket.cookies.get("access_token")
    if not token:
        await websocket.close(code=1008, reason="Token required")
        return
    current_user_id = get_id_by_token(token)
    user = get_user_by_id(current_user_id)
    if not user:
        await websocket.close(code=1008, reason="User not found")
        return
    if user_is_banned(current_user_id):
        await websocket.close(code=1008, reason="User banned")
        return
    await websocket.accept()
    active_connections[current_user_id] = websocket
    await broadcast(create_online_event(True, current_user_id))
    try:
        while True:
            data = await websocket.receive_json()
            receiver_id = data["to"]
            chat_id = data["chat_id"]
            msg = data["message"]
            msg_id = track_message(current_user_id, chat_id, msg)
            if receiver_id in active_connections:
                event = create_msg_event(msg_id, int(chat_id), int(current_user_id), msg)
                try:
                    await active_connections[receiver_id].send_json(event)
                except WebSocketDisconnect:
                    active_connections.pop(receiver_id, None)
    except WebSocketDisconnect:
        active_connections.pop(current_user_id, None)
        await broadcast(create_online_event(False, current_user_id))


def create_msg_event(msg_id: int, chat_id: int, sender_id: int, message: str):
    return {
        "type": "new_message",
        "msg_id": msg_id,
        "chat_id": chat_id,
        "from": sender_id,
        "message": message
    }


def create_online_event(status: bool, user_id: int):
    return {
        "type": "status",
        "user_id": user_id,
        "online": status
    }

# Остальные эндпоинты без изменений (они уже используют Bearer token из заголовка)
@router.get("/get_chats/")
def get_all_user_chats(limit: int, token: HTTPAuthorizationCredentials = Depends(security), offset: int = 0):
    current_user_id = get_id_by_token(token.credentials)
    check_auth(current_user_id)
    return [serialize_chat(chat) for chat in get_user_chats(current_user_id, limit, offset)]


@router.get("/get_messages/")
def get_messages_in_chat(chat_id: int, limit: int, token: HTTPAuthorizationCredentials = Depends(security),
                         offset: int = 0):
    current_user_id = get_id_by_token(token.credentials)
    check_auth(current_user_id)
    return [serialize_msg(msg) for msg in get_messages(chat_id, limit, offset)]


@router.get("/check_chat_is_exists_by_receiver_id/")
def check_chat_is_exists_by_receiver_id(receiver_id: int, token: HTTPAuthorizationCredentials = Depends(security)):
    current_user_id = get_id_by_token(token.credentials)
    check_auth(current_user_id)
    chat_id = get_chat_by_users(current_user_id, receiver_id)
    if chat_id is None:
        raise HTTPException(status_code=404, detail="Chat not found")
    return {"chat_id": chat_id}


@router.post("/create_chat_if_not_exists/")
async def create_chat_if_not_exists(first_msg_text: str, receiver_id: int,
                                    token: HTTPAuthorizationCredentials = Depends(security)):
    current_user_id = get_id_by_token(token.credentials)
    check_auth(current_user_id)
    chat_id = get_chat_by_users(current_user_id, receiver_id)
    if chat_id is not None:
        HTTPException(status_code=409, detail="Chat already exists")
    chat_id = track_message_and_create_chat(current_user_id, receiver_id, first_msg_text)

    if receiver_id in active_connections:
        try:
            sender_nickname = get_user_by_id(current_user_id)[2]
            await active_connections[receiver_id].send_json({
                "type": "new_chat",
                "chat_id": chat_id,
                "from": current_user_id,
                "message": first_msg_text,
                "message_id": get_first_message(chat_id),
                "sender_nickname": sender_nickname
            })
        except:
            pass

    return {"chat_id": chat_id}


@router.get("/status/{user_id}")
def get_status(user_id: int, token: HTTPAuthorizationCredentials = Depends(security)):
    current_user_id = get_id_by_token(token.credentials)
    check_auth(current_user_id)
    return {
        "online": user_id in active_connections
    }


@router.patch("/set_message_is_read/")
def set_msg_is_read(msg_id: int, token: HTTPAuthorizationCredentials = Depends(security)):
    current_user_id = get_id_by_token(token.credentials)
    check_auth(current_user_id)
    set_message_is_read(msg_id)
    return {"success": True}


@router.patch("/set_all_messages_is_read/")
async def set_all_msgs_is_read(chat_id: int, receiver_id: int, token: HTTPAuthorizationCredentials = Depends(security)):
    current_user_id = get_id_by_token(token.credentials)
    check_auth(current_user_id)
    set_all_messages_is_read(chat_id)
    if receiver_id in active_connections:
        try:
            await active_connections[receiver_id].send_json({
                "type": "messages_is_read",
                "chat_id": chat_id
            })
        except:
            active_connections.pop(receiver_id, None)
    return {"success": True}


async def broadcast(data):
    disconnected = []
    for user_id, ws in active_connections.items():
        try:
            await ws.send_json(data)
        except:
            disconnected.append(user_id)
    for user_id in disconnected:
        active_connections.pop(user_id, None)


def serialize_msg(msg):
    return {
        "sender_id": msg[0],
        "msg_body": msg[1],
        "created_at": msg[2],
        "is_read": msg[3]
    }


def serialize_chat(chat):
    return {
        "chat_id": chat[0],
        "receiver_id": chat[1],
        "receiver_nickname": chat[2],
        "last_msg": chat[3][0],
        "last_msg_timestamp": chat[3][1]
    }