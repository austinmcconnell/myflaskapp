"""Model unit tests."""
import datetime as dt

import pytest

from app.user.models import User
from tests.factories import UserFactory


@pytest.mark.usefixtures('db')
class TestUser:
    """User tests."""

    def test_get_by_id(self):
        """Get user by ID."""
        user = User('foo', 'foo@bar.com')
        user.save()

        retrieved = User.get_by_id(user.id)
        assert retrieved == user

    def test_created_at_defaults_to_datetime(self):
        """Test creation date."""
        user = User(username='foo', email='foo@bar.com')
        user.save()
        assert bool(user.created_at)
        assert isinstance(user.created_at, dt.datetime)

    def test_password_is_nullable(self):
        """Test null password."""
        user = User(username='foo', email='foo@bar.com')
        user.save()
        assert user.password is None

    def test_factory(self, db):
        """Test user factory."""
        user = UserFactory(password='myprecious')
        db.session.commit()
        assert bool(user.username)
        assert bool(user.email)
        assert bool(user.created_at)
        assert user.is_admin is False
        assert user.active is True
        assert user.check_password('myprecious')

    def test_check_password(self):
        """Check password."""
        user = User.create(username='foo', email='foo@bar.com', password='foobarbaz123')
        assert user.check_password('foobarbaz123') is True
        assert user.check_password('barfoobaz') is False

    def test_full_name(self):
        """User full name."""
        user = UserFactory(first_name='Foo', last_name='Bar')
        assert user.full_name == 'Foo Bar'

    def test_add_notification(self):
        """User full name."""
        user = UserFactory(first_name='Foo', last_name='Bar')

        user_notifications = list(user.notifications)
        assert len(user_notifications) == 0

        user.add_notification(name='panda', data='bear')

        user_notifications = list(user.notifications)
        assert len(user_notifications) == 1

    def test_verify_reset_password(self):
        user1 = UserFactory(first_name='Foo', last_name='Bar')
        user1.save()

        token = user1.get_reset_password_token()

        user2 = User.verify_reset_password_token(token)
        assert user1 == user2

    def test_add_message(self):
        user = UserFactory(first_name='Foo', last_name='Bar')
        assert user.new_messages() == 0

        user.add_message(contents=f'Bigger on the inside')
        assert user.new_messages() == 1
