import maya

from app.extensions import db
from app.database import Column, Model, SurrogatePK, relationship


class Message(SurrogatePK, Model):
    __tablename__ = 'messages'
    user_id = Column(db.Integer, db.ForeignKey('users.id'))
    body = Column(db.String(140))
    timestamp = Column(db.DateTime(timezone=True), index=True, default=maya.now().datetime)

    user = relationship('User', back_populates='messages', lazy='joined')

    def __repr__(self):
        return '<Message {}>'.format(self.body)
