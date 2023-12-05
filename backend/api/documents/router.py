from fastapi import APIRouter, Depends
from .schemas import DocumentCreate, Document
from ..dependencies import get_db
from . import crud

router = APIRouter(
    prefix='/documents'
)


@router.post('/create', response_model=Document)
async def create_document(document: DocumentCreate, db = Depends(get_db)):
    return await crud.create_document(db, document)

