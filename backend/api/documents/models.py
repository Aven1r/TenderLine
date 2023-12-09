from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..database import Base
# from datetime import datetime
#
#
# class Document(Base):
#     __tablename__ = 'document'
#
#     id = Column(Integer, primary_key=True, autoincrement=True, index=True)
#     message_id = Column(Integer, ForeignKey('message.id'), nullable=True)
#
#     consumer_id = Column(Integer, ForeignKey('user.id'), nullable=True)
#     consumer = relationship('User', foreign_keys=consumer_id, backref='documents_with_suppliers')
#
#     supplier_id = Column(Integer, ForeignKey('user.id'), nullable=True)
#     supplier = relationship('User', foreign_keys=supplier_id, backref='documents_with_consumers')
#
#     previous_document_id = Column(Integer, ForeignKey('document.id'), nullable=True)
#     previous_document = relationship('Document', lazy=False)
#
#     created_at = Column(DateTime, default=datetime.utcnow)


class Document(Base):
    __tablename__ = 'document'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    status = Column(String)
    reestr_number = Column(String)
    purchase_number = Column(String)
    law_number = Column(String)
    contract_method = Column(String)
    contract_basis = Column(String)
    contract_number = Column(String)
    contract_lifetime = Column(String)
    contract_subject = Column(String)
    contract_place = Column(String)
    IKZ = Column(String)
    budget = Column(String)
    contract_price = Column(String)
    prepayment = Column(String)
    
    message_id = Column(Integer, ForeignKey('message.id'), nullable=True)
    # message = relationship("Message", backref="document", foreign_keys=message_id)


