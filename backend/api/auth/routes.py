from fastapi import APIRouter

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.post('/register/customer')
async def register_customer():
    pass


@router.post('/register/customer')
async def register_supplier():
    pass


