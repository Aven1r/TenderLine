from fastapi import APIRouter, Depends
from .schemas import DocumentCreate, Document
from ..dependencies import get_db
from . import crud
from ..chat.crud import get_chat

router = APIRouter(
    prefix='/documents'
)


@router.post('/create', response_model=Document)
async def create_document(document: DocumentCreate, db = Depends(get_db)):
    return await crud.create_document(db, document)


@router.get('/history', response_model=list[Document])
async def get_document_history(chat_id: int, db = Depends(get_db)):
    chat = await get_chat(db, chat_id)
    return await crud.get_document_history(db, chat.consumer_id, chat.vendor_id)
