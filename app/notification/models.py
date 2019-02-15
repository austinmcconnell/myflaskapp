from typing import Dict

import maya

from app.database import Column, Model, SurrogatePK, db


class Notification(SurrogatePK, Model):
    __tablename__ = 'notifications'
    name = Column(db.String(128), index=True)
    user_id = Column(db.Integer, db.ForeignKey('users.id'))
    payload = Column(db.JSON)
    timestamp = Column(db.DateTime(timezone=True), index=True, default=maya.now().datetime)

    def __init__(self, name: str, user, payload: Dict) -> None:
        db.Model.__init__(self, name=name, user_id=user.id, payload=payload)
