# -*- coding: utf-8 -*-
import re
from urllib.parse import urlparse

from flask import get_flashed_messages, url_for
from flask_login import login_user
import pytest

from app.extensions import mail
from app.user.models import User
from tests.factories import UserFactory


class TestLoggingIn:

    @pytest.mark.parametrize('endpoint', ('public.home', 'auth.login'))
    def test_login_return_200(self, user, testapp, endpoint):
        res = testapp.get(url_for(endpoint))

        form = res.forms['login-form']
        form['username'] = user.username
        form['password'] = 'myprecious'

        res = form.submit().follow()
        assert res.status_code == 200

    def test_alert_on_logout(self, user, testapp):
        res = testapp.get(url_for('public.home'))
        # Fills out login form in navbar
        form = res.forms['login-form']
        form['username'] = user.username
        form['password'] = 'myprecious'
        # Submits
        res = form.submit().follow()
        res = testapp.get(url_for('auth.logout')).follow()
        # sees alert
        assert 'You are logged out.' in res

    @pytest.mark.parametrize('endpoint', ('public.home', 'auth.login'))
    def test_error_message_incorrect_password(self, user, testapp, endpoint):
        res = testapp.get(url_for(endpoint))

        form = res.forms['login-form']
        form['username'] = user.username
        form['password'] = 'wrong'

        res = form.submit()
        assert 'Invalid password' in res

    @pytest.mark.parametrize('endpoint', ('public.home', 'auth.login'))
    def test_error_message_username_doesnt_exist(self, user, testapp, endpoint):
        res = testapp.get(url_for(endpoint))

        form = res.forms['login-form']
        form['username'] = 'unknown'
        form['password'] = 'myprecious'

        res = form.submit()
        assert 'Unknown user' in res


class TestRegistering:

    def test_can_register(self, user, testapp):
        old_count = len(User.query.all())
        # Goes to homepage
        res = testapp.get(url_for('public.home'))
        # Clicks Create Account button
        res = res.click('Create account')
        # Fills out the form
        form = res.forms['registerForm']
        form['username'] = 'foobar'
        form['email'] = 'foo@bar.com'
        form['password'] = 'secret'
        form['confirm'] = 'secret'
        # Submits
        res = form.submit().follow()
        assert res.status_code == 200
        # A new user was created
        assert len(User.query.all()) == old_count + 1

    def test_error_message_passwords_dont_match(self, user, testapp):
        # Goes to registration page
        res = testapp.get(url_for('auth.register'))
        # Fills out form, but passwords don't match
        form = res.forms['registerForm']
        form['username'] = 'foobar'
        form['email'] = 'foo@bar.com'
        form['password'] = 'secret'
        form['confirm'] = 'secrets'
        # Submits
        res = form.submit()
        # sees error message
        assert 'Passwords must match' in res

    def test_error_message_user_already_registered(self, user, testapp):
        user = UserFactory(active=True)  # A registered user
        user.save()
        # Goes to registration page
        res = testapp.get(url_for('auth.register'))
        # Fills out form, but username is already registered
        form = res.forms['registerForm']
        form['username'] = user.username
        form['email'] = 'foo@bar.com'
        form['password'] = 'secret'
        form['confirm'] = 'secret'
        # Submits
        res = form.submit()
        # sees error
        assert 'Username already registered' in res

    def test_confirm_email_sent(self, db, testapp):
        # Goes to registration page
        with mail.record_messages() as outbox:

            res = testapp.get(url_for('auth.register'))

            form = res.forms['registerForm']
            form['username'] = 'pandas'
            form['email'] = 'foo@bar.com'
            form['password'] = 'secret'
            form['confirm'] = 'secret'

            res = form.submit()

            assert len(outbox) == 1
            assert 'Confirm Your Email Address' in outbox[0].subject

    def test_email_confirmation(self, db, testapp):
        with mail.record_messages() as outbox:
            res = testapp.get(url_for('auth.register'))

            form = res.forms['registerForm']
            form['username'] = 'pandas'
            form['email'] = 'foo@bar.com'
            form['password'] = 'secret'
            form['confirm'] = 'secret'

            form.submit()

            body_html = outbox[0].html

        groups = re.search('<a href=\"http://localhost(.*)\">', body_html)
        confirmation_url = groups[1]

        testapp.get(confirmation_url)

        assert User.get_by_id(1).email_confirmed is True

    def test_email_confirmation_no_user_redirect(self, db, testapp):

        with mail.record_messages() as outbox:
            res = testapp.get(url_for('auth.register'))
            form = res.forms['registerForm']
            form['username'] = 'pandas'
            form['email'] = 'foo@bar.com'
            form['password'] = 'secret'
            form['confirm'] = 'secret'
            form.submit()

            body_html = outbox[0].html

        groups = re.search('<a href=\"http://localhost(.*)\">', body_html)
        confirmation_url = groups[1] + 'wrong'

        response = testapp.get(confirmation_url)

        assert response.status_code == 302
        assert urlparse(response.location).path == url_for('public.home')

    @pytest.mark.xfail
    def test_email_already_confirmed_redirect(self, db, testapp):
        with mail.record_messages() as outbox:
            res = testapp.get(url_for('auth.register'))
            form = res.forms['registerForm']
            form['username'] = 'pandas'
            form['email'] = 'foo@bar.com'
            form['password'] = 'secret'
            form['confirm'] = 'secret'
            form.submit()

            body_html = outbox[0].html

        groups = re.search('<a href=\"http://localhost(.*)\">', body_html)
        confirmation_url = groups[1]

        user = User.get_by_id(1)

        login_user(user)
        user.email_confirmed = True
        # FIXME: .get() has a different context. No logged in user
        response = testapp.get(confirmation_url)
        flashed_messages = get_flashed_messages()

        assert 'You have already verified your email address.' in flashed_messages
        assert response.status_code == 302
        assert urlparse(response.location).path == url_for('public.home')
