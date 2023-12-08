from fastapi import APIRouter, Depends, status, HTTPException, Response, Cookie
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..auth.secure import create_access_token, verify_jwt_token, verify_password, get_password_hash
from sqlalchemy.orm import Session
from ..dependencies import get_db, get_user
from ..auth.schemas import User

from .api import email_logic
from .api import crud

router = APIRouter(tags=["email"], prefix='/email')


@router.post('/sendpdf', status_code=status.HTTP_200_OK)
def send_pdf(current_user=Depends(get_user), db=Depends(get_db)):
    # TODO GET DOCUMENT AND ATTACH IT TO FUNCTION
    email_info = {}
    email_info['from_user'] = "Кадомцев Андрей"
    email_info['message'] = (f"Пользователь {email_info['from_user']} отправил вам новое сообщение!")
    email_info['to'] = "m2204942@edu.misis.ru"
    email_info['contract'] = "Закупка кроссовок"
    email_info['subject'] = f"Обновление в контракте {email_info['contract']}"

    email_logic.send_pdf(email_info=email_info, attachment=None)

    return {"Email sent successfully!"}

def email_notify(current_user, contract_number):
    email_logic.notify_user(current_user.email, contract_number)
