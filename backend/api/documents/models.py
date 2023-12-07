from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..database import Base


class Document(Base):
    __tablename__ = 'document'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    message_id = Column(Integer, ForeignKey('message.id'), nullable=True)

    previous_document_id = Column(Integer, ForeignKey('document.id'), nullable=True)
    previous_document = relationship('Document', lazy=False)

