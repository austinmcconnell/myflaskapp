# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""

from flask import g, url_for
import pytest
import pytest_pgsql
from webtest import TestApp

from app.app import create_app
from app.database import db as _db

from .factories import UserFactory


@pytest.fixture(scope='session')
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


@pytest.fixture
def db(app):
    _db.app = app
    if app.config['SQLALCHEMY_DATABASE_URI'] is None:
        pytest_pgsql.create_engine_fixture('my_engine')
        postgres_db = pytest_pgsql.PostgreSQLTestDB.create_fixture('postgres_db', 'my_engine')

        app.config['SQLALCHEMY_DATABASE_URI'] = postgres_db.engine.url
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
