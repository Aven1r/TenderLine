from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


# class Chat(Base):
#     __tablename__ = 'chat'
#
#     id = Column(Integer, primary_key=True, autoincrement=True, index=True)
#     created_at = Column(DateTime)
#     # messages = relationship('Message', backref='chat', passive_deletes=True, lazy="immediate")
#     vendor_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
#     vendor = relationship('User', backref='chats_with_consumers', foreign_keys=vendor_id, lazy="immediate")
#     consumer_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
#     consumer = relationship('User', backref='chats_with_vendors', foreign_keys=consumer_id, lazy="immediate")


# class Message(Base):
#     __tablename__ = 'message'
#
#     id = Column(Integer, primary_key=True, autoincrement=True, index=True)
#     chat_id = Column(Integer, ForeignKey('chat.id', ondelete='CASCADE'))
#     chat = relationship('Chat', backref='messages', lazy="immediate")
#     user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
#     user = relationship('User', backref='messages', lazy="immediate")
#     text = Column(String)
#     created_at = Column(DateTime)
#     document = relationship('Document', uselist=False, backref='message', lazy="immediate")


class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    author_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    recipient_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    text = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


