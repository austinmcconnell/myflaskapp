# -*- coding: utf-8 -*-
"""User models."""
from hashlib import md5
from time import time
from typing import Union

from flask import current_app
from flask_login import UserMixin
import jwt
from jwt import InvalidTokenError
import maya

from app.notification.models import Notification
from app.messages.models import Message
from app.database import Column, Model, SurrogatePK, db
from app.extensions import bcrypt
from app.task.models import Task


class User(UserMixin, SurrogatePK, Model):
    """A user of the app."""

    __tablename__ = 'users'
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(db.Binary(128), nullable=True)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)
    email_confirmed = Column(db.Boolean(), nullable=True, default=False)
    email_confirmed_at = Column(db.DateTime(timezone=True), nullable=True)
    locale = db.Column(db.String(length=2), default='en')
    created_at = Column(db.DateTime(timezone=True), nullable=False, default=maya.now().datetime)
    last_seen = db.Column(db.DateTime(timezone=True))
    last_message_read_time = db.Column(db.DateTime(timezone=True))

    notifications = db.relationship('Notification', backref='user', lazy='dynamic')
    tasks = db.relationship('Task', backref='user', lazy='dynamic')
    messages = db.relationship('Message', back_populates='user', lazy='dynamic')

    def __init__(self, username: str, email: str, password: str=None, **kwargs) -> None:
        """Create instance."""
        db.Model.__init__(self, username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password: str) -> None:
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value: str) -> bool:
        """Check password."""
        is_good_password: bool = bcrypt.check_password_hash(self.password, value)
        return is_good_password

    @property
    def full_name(self) -> str:
        """Full user name."""
        return '{0} {1}'.format(self.first_name, self.last_name)

    def __repr__(self) -> str:
        """Represent instance as a unique string."""
        return '<User({username!r})>'.format(username=self.username)

    def get_reset_password_token(self, expires_in: int=600) -> str:
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token) -> Union['User', None]:
        try:
            user_id = jwt.decode(token, current_app.config['SECRET_KEY'],
                                 algorithms=['HS256'])['reset_password']
        except InvalidTokenError:
            return None
        user: User = User.query.get(user_id)
        return user

    def confirm_email(self) -> None:
        self.email_confirmed = True
        self.email_confirmed_at = maya.now().datetime()

    def get_confirmation_token(self) -> str:
        return jwt.encode(
            {'confirm_email': self.id},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_confirmation_token(token: str) -> Union['User', None]:
        try:
            user_id = jwt.decode(token, current_app.config['SECRET_KEY'],
                                 algorithms=['HS256'])['confirm_email']
        except:
            return None
        user: User = User.query.get(user_id)
        return user

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def add_notification(self, name, data):
        notification = self.notifications.filter_by(user=self, name=name).first()

        if notification:
            notification.update(payload=data)
        else:
            notification = Notification.create(name=name, payload=data, user=self)
        return notification

    def launch_task(self, name, description, *args, **kwargs):
        rq_job = current_app.task_queue.enqueue('app.task.tasks.' + name, *args, **kwargs)
        task = Task(id=rq_job.get_id(), name=name, description=description, user=self)
        db.session.add(task)
        return task

    def get_tasks_in_progress(self):
        return Task.query.filter_by(user=self, complete=False).all()

    def get_task_in_progress(self, name):
        return Task.query.filter_by(name=name, user=self, complete=False).first()

    def add_message(self, contents):
        message = Message.create(user_id=self.id, body=contents)
        return message

    def new_messages(self):
        last_read_time = self.last_message_read_time or maya.when('1900-1-1').datetime()
        return Message.query.filter_by(user_id=self.id).filter(Message.timestamp > last_read_time).count()
