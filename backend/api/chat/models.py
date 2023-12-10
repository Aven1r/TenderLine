from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    author_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    recipient_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    text = Column(String)
    document = relationship('Document', uselist=False, lazy="immediate")
    created_at = Column(DateTime, default=datetime.utcnow)

   


