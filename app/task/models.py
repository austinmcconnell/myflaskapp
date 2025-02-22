from typing import TYPE_CHECKING

import rq
from flask import current_app
from redis.exceptions import RedisError
from rq.exceptions import NoSuchJobError

from app.database import Column, Model, db

if TYPE_CHECKING:
    from app.user.models import User


class Task(Model):
    __tablename__ = 'tasks'

    id = db.Column(db.String(36), primary_key=True)  # pylint: disable=invalid-name
    name = Column(db.String(128), index=True)
    description = Column(db.String(128))
    user_id = Column(db.Integer, db.ForeignKey('users.id'))
    complete = Column(db.Boolean, default=False)

    def __init__(self, id_: str, name: str, description: str, user: 'User') -> None:
        db.Model.__init__(self, id=id_, name=name, description=description, user=user)

    def get_rq_job(self):
        try:
            rq_job = rq.job.Job.fetch(self.id, connection=current_app.redis)
        except (RedisError, NoSuchJobError):
            return None
        return rq_job

    def get_progress(self):
        job = self.get_rq_job()
        return job.meta.get('progress', 0) if job is not None else 100
