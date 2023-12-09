from fastapi import APIRouter, Depends, status
from fastapi.staticfiles import StaticFiles
from .schemas import Document, DocumentCreate
from ..dependencies import get_db
from . import crud

# from ..chat.crud import get_chat

router = APIRouter(
    prefix='/documents',
    tags=['Documents']
)


@router.post('/create', response_model=Document)
async def create_document(document: DocumentCreate, db=Depends(get_db)):
    return await crud.create_document(db, document)


@router.post('/getdiff', status_code=status.HTTP_200_OK)
async def get_gifference(document: Document, document2: Document):
    return await crud.get_difference(document, document2)


@router.post('/generatepdf', status_code=status.HTTP_200_OK)
async def generate_pdf(document: Document, db = Depends(get_db)):
    return await crud.generate_pdf(document)