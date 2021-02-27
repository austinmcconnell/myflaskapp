from typing import Dict, TYPE_CHECKING

import maya

from app.database import Column, db, Model, SurrogatePK

if TYPE_CHECKING:
    from app.user.models import User


class Notification(SurrogatePK, Model):
    __tablename__ = 'notifications'
    name = Column(db.String(128), index=True)
    user_id = Column(db.Integer, db.ForeignKey('users.id'))
    payload = Column(db.JSON)
    timestamp = Column(db.DateTime(timezone=True), index=True, default=maya.now().datetime)

    def __init__(self, name: str, user: 'User', payload: Dict) -> None:
        db.Model.__init__(self, name=name, user_id=user.id, payload=payload)

    def update(self, commit=True, **kwargs):
        kwargs['timestamp'] = maya.now().datetime()
        super().update(commit, **kwargs)
