"""Defines fixtures available to all tests."""

import pytest
from flask import g, url_for
from sqlalchemy import create_engine
from testing.postgresql import Postgresql
from webtest import TestApp

from app.app import create_app
from app.database import db as _db

from .factories import UserFactory


@pytest.fixture
def app():
    _app = create_app('testing')
    ctx = _app.test_request_context()
    ctx.push()

    @_app.before_request
    def set_locale():
        g.locale = 'en'

    yield _app

    ctx.pop()


@pytest.fixture
def testapp(app):
    return TestApp(app)


@pytest.fixture(scope='session')
def postgres_db():
    with Postgresql() as postgresql:
        yield create_engine(postgresql.url())


@pytest.fixture
def db(app, postgres_db):
    _db.app = app

    if app.config['SQLALCHEMY_DATABASE_URI'] is None:
        app.config['SQLALCHEMY_DATABASE_URI'] = postgres_db.url

    with app.app_context():
        _db.create_all()

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()


@pytest.fixture
def user(db):
    user = UserFactory(password='myprecious')
    db.session.commit()
    return user


@pytest.fixture
def authenticated_user(user, testapp):
    res = testapp.get(url_for('auth.login'))

    form = res.forms['login-form']
    form['username'] = user.username
    form['password'] = 'myprecious'

    _ = form.submit().follow()
    return user
