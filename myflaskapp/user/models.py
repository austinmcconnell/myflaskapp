# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt
from time import time
from typing import TypeVar, Union

from flask import current_app
from flask_login import UserMixin
import jwt
from jwt import InvalidTokenError

from myflaskapp.database import Column, Model, SurrogatePK, db, reference_col, relationship
from myflaskapp.extensions import bcrypt


class Role(SurrogatePK, Model):
    """A role for a user."""

    __tablename__ = 'roles'
    name = Column(db.String(80), unique=True, nullable=False)
    user_id = reference_col('users', nullable=True)
    user = relationship('User', backref='roles')

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Role({name})>'.format(name=self.name)


User_Type = TypeVar('User_Type', bound='User')


class User(UserMixin, SurrogatePK, Model):
    """A user of the app."""

    __tablename__ = 'users'
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(db.Binary(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)
    email_confirmed = Column(db.Boolean(), nullable=True, default=False)
    email_confirmed_at = Column(db.DateTime, nullable=True)

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
        return bcrypt.check_password_hash(self.password, value)

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
    def verify_reset_password_token(token) -> Union[User_Type, None]:
        try:
            user_id = jwt.decode(token, current_app.config['SECRET_KEY'],
                                 algorithms=['HS256'])['reset_password']
        except InvalidTokenError:
            return None
        return User.query.get(user_id)

    def confirm_email(self) -> None:
        self.email_confirmed = True
        self.email_confirmed_at = dt.datetime.utcnow()

    def get_confirmation_token(self) -> str:
        return jwt.encode(
            {'confirm_email': self.id},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_confirmation_token(token: str) -> Union[User_Type, None]:
        try:
            user_id = jwt.decode(token, current_app.config['SECRET_KEY'],
                                 algorithms=['HS256'])['confirm_email']
        except:
            return None
        return User.query.get(user_id)
