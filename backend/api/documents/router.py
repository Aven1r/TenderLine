from fastapi import APIRouter, Depends, status
from fastapi.staticfiles import StaticFiles
from .schemas import Document, DocumentCreate, UserContractInfo
from ..dependencies import get_db
from . import crud
from fastapi.responses import FileResponse
from ..profile.api.crud import get_user_full_info

# from ..chat.crud import get_chat

router = APIRouter(
    prefix='/documents',
    tags=['Documents']
)


@router.post('/create', response_model=Document)
async def create_document(document: DocumentCreate, db=Depends(get_db)):
    return await crud.create_document(db, document)


@router.post('/getdiff', status_code=status.HTTP_200_OK)
async def get_gifference(doc_id: int, db=Depends(get_db)):
    document = await crud.get_document(db, doc_id)
    document_pre = await crud.get_document(db, document.previous_document_id)
    print(document, document_pre)
    return await crud.get_difference(document.as_dict(), document_pre.as_dict())


@router.get('/downloadpdf', status_code=status.HTTP_200_OK)
async def generate_pdf(db = Depends(get_db), user1_id=id, user2_id=id, doc_id=id):

    user1 = await get_user_full_info(db, user1_id)
    user2 = await get_user_full_info(db, user2_id)

    document = await crud.get_document(db, doc_id)
    
    path_to_contract = await crud.generate_pdf(document, user1=user1, user2=user2)
    return FileResponse(path=path_to_contract, filename='diff.pdf',media_type='multipart/form-data')