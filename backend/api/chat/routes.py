from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends

# from .managers import ConnectionManager, UserConnection
from .managers import ConnectionManager, UserConnection
from .schemas import MessageCreate, Message
from . import crud
from ..dependencies import get_db, get_user


router = APIRouter(
    prefix='/chats',
    tags=['Messages / Chats']
)


# @router.get('/', response_model=list[Chat], dependencies=[Depends(get_user)])
# async def get_chats(user=Depends(get_user), db=Depends(get_db)):
#     return await crud.get_user_chats(db,  user.id)
#
#
# @router.post('/create', response_model=Chat, dependencies=[Depends(get_user)])
# async def create_chat(chat: ChatCreate, db=Depends(get_db)):
#     chat_db = await crud.create_chat(db, chat)
#     return chat_db
#
#
# @router.get('/{chat_id}', response_model=Chat | None, dependencies=[Depends(get_user)])
# async def get_chat(chat_id: int, db=Depends(get_db)):
#     return await crud.get_chat(db, chat_id)


@router.get('/messages', response_model=list[Message], dependencies=[Depends(get_user)])
async def get_messages(recipient_id: int, limit: int = 10, skip: int = 0, user=Depends(get_user), db=Depends(get_db)):
    rez = await crud.get_messages(db, user.id, recipient_id)
    return rez
    # return await crud.get_messages(db, chat_id, None, skip=skip, limit=limit)


# @router.get('/{chat_id}/messages/{message_id}', response_model=Message | None, dependencies=[Depends(get_user)])
# async def get_message(chat_id: int, message_id: int,  db=Depends(get_db)):
#     return await crud.get_message(db, chat_id, message_id)


@router.post('/messages/create', response_model=Message, dependencies=[Depends(get_user)])
async def create_message(message: MessageCreate, user=Depends(get_user),  db=Depends(get_db)):
    return await crud.create_message(db, user.id, message)
    # return await crud.create_message(db, message, chat_id)

manager = ConnectionManager()


# @router.websocket('/ws/chat/{chat_id}')
# async def websocket_chat_endpoint(websocket: WebSocket, chat_id: int, user=Depends(get_user), db=Depends(get_db)):
#     chat = await crud.get_chat(db, chat_id)
#     recipient = chat.vendor if user != chat.vendor else chat.consumer
#     user_connection = UserConnection(chat, user, websocket)
#     await manager.connect(user_connection)
#     try:
#         while True:
#             data = await websocket.receive_json()
#
#             message = await crud.create_message(db, MessageCreate(**data), user.id)
#             await manager.send_message(recipient, message)
#             # await manager.broadcast(f"Client #{client_id} says: {data}")
#     except WebSocketDisconnect:
#         manager.disconnect(user_connection)
#         # await manager.broadcast(f"Client #{client_id} left the chat")


@router.websocket('/ws/{recipient_id}')
async def websocket_chat_endpoint(websocket: WebSocket, recipient_id: int, user=Depends(get_user), db=Depends(get_db)):
    print(user.id, recipient_id)
    user_connection = UserConnection(user.id, websocket)
    await manager.connect(user_connection)
    try:
        while True:
            data = await websocket.receive_json()
            print(data)
            message = await crud.create_message(db, user.id, MessageCreate(**data, recipient_id=recipient_id))

            await manager.send_message(recipient_id, message)
            # await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(user_connection)





