"""Factories to help in tests."""
from factory import PostGenerationMethodCall, Sequence
from factory.alchemy import SQLAlchemyModelFactory

from app.database import db
from app.user.models import User


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = db.session


class UserFactory(BaseFactory):
    """User factory."""

    username = Sequence(lambda n: 'user{}'.format(n))
    email = Sequence(lambda n: 'user{}@example.com'.format(n))
    password = PostGenerationMethodCall('set_password', 'example')
    active = True
    is_admin = False
    email_confirmed = False

    class Meta:
        """Factory configuration."""

        model = User
