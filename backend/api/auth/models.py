from sqlalchemy import Column, Integer, Boolean, String, ForeignKey
from sqlalchemy.orm import relationship

# from ..chat.models import Chat
from ..database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String)
    address = Column(String)
    email = Column(String, unique=True)
    status = Column(String)
    password = Column(String)
    use_email_notification = Column(Boolean, default=True)
    telegram_id = Column(String, unique=True)
    # chats = relationship(Chat)


class UserContractInfo(Base):
    __tablename__ = 'user_contract_info'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, unique=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    company_name = Column(String, default='ООО "Новая компания"')
    address = Column(String, default='г. Москва, ул. Пушкина, д. 1, кв. 1')
    phone = Column(String, default='+7 (999) 999-99-99')
    checking_account = Column(String, default='00000000000000000000')
    BIC = Column(String, default='000000000')
    INN = Column(String, default='0000000000')
    KPP = Column(String, default='000000000')
    OGRN = Column(String, default='0000000000000')
    OKPO = Column(String, default='00000000')
    ОКТМО = Column(String, default='00000000000')
    email = Column(String, default='eeeeeeeee')
    user = relationship(User, backref='contract_info')
