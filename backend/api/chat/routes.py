from fastapi import APIRouter, WebSocket
from .schemas import MessageCreate, ChatCreate, Message, Chat


router = APIRouter(
    prefix='/chats',
    tags=['Messages / Chats']
)


@router.get('/')
async def get_chats(user_id: int = None):
    pass


@router.post('/create', response_model=Chat)
async def create_chat(chat: ChatCreate):
    pass


@router.get('/{chat_id}', response_model=Chat)
async def get_chat(chat_id: int):
    pass


@router.get('/{chat_id}/messages', response_model=list[Message])
async def get_messages(chat_id: int, limit: int = 10, skip: int = 0):
    pass


@router.post('/{chat_id}/messages/create', response_model=Message)
async def create_message(chat_id: int, message: MessageCreate):
    pass


@router.websocket('/ws/{chat_id}')
async def websocket_chat_endpoint(websocket: WebSocket, chat_id: int):
    pass


