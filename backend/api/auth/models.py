from sqlalchemy import Column, Integer, Boolean, String
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
    # chats = relationship(Chat)

