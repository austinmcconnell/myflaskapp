"""Defines fixtures available to all tests."""

import logging
from unittest.mock import patch

import pytest
from alembic import command
from flask import g, url_for
from pytest_postgresql import factories
from webtest import TestApp

from app.app import create_app
from app.database import db as _db
from app.settings import TestingConfig

from .factories import UserFactory


def template_database(**kwargs):
    connection_str = f"postgresql+psycopg://{kwargs['user']}:@{kwargs['host']}:\
        {kwargs['port']}/{kwargs['dbname']}"

    testing_config = TestingConfig()
    testing_config.SQLALCHEMY_DATABASE_URI = connection_str

    with patch.dict('app.app.CONFIG', {'testing': testing_config}):
        app = create_app('testing')
        with app.app_context():
            config = app.extensions['migrate'].migrate.get_config('migrations')
            command.upgrade(config, 'head')


postgresql_proc = factories.postgresql_proc(load=[template_database], )
postgresql = factories.postgresql('postgresql_proc')


@pytest.fixture
def app(postgresql):
    connection_str = f'postgresql+psycopg://{postgresql.info.user}:@{postgresql.info.host}:\
        {postgresql.info.port}/{postgresql.info.dbname}'

    testing_config = TestingConfig()
    testing_config.SQLALCHEMY_DATABASE_URI = connection_str

    with patch.dict('app.app.CONFIG', {'testing': testing_config}):
        _app = create_app('testing')
        _app.logger.setLevel(logging.CRITICAL)

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

    yield _db

    _db.session.close()


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
