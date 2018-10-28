from flask import current_app, render_template
from flask_babel import _

from app.email import send_email
from app.user.models import User


def send_password_reset_email(user: User):
    token = user.get_reset_password_token()
    send_email(subject=_('[My Flask App] Reset Your Password'),
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt', user=user, token=token),
               html_body=render_template('email/reset_password.html', user=user, token=token))


def send_confirm_email(user: User):
    token = user.get_confirmation_token()
    send_email(subject=_('[My Flask App] Confirm Your Email Address'),
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/confirm_email.txt', user=user, token=token),
               html_body=render_template('email/confirm_email.html', user=user, token=token))
