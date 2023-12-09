from fastapi import APIRouter, Depends, status, HTTPException, Response, Cookie
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..auth.secure import create_access_token, verify_jwt_token, verify_password, get_password_hash
from sqlalchemy.orm import Session
from ..dependencies import get_db, get_user
from ..auth.schemas import User
from .api import schemas

from .api import email_logic
from .api import crud

router = APIRouter(tags=["email"], prefix='/email')


@router.post('/sendpdf', status_code=status.HTTP_200_OK)
def send_pdf(send_to: schemas.EmailInfo, current_user: User=Depends(get_user)):
    
    # TODO - add logic to send the latest version of the contract
    user_email = current_user.email
    email_logic.send_pdf(user_email, attachment=None)

    return {"Email sent successfully!"}

def email_notify(current_user, contract_number):
    print(current_user)
    email_logic.notify_user(current_user.email, contract_number)
