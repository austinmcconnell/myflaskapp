# from threading import Thread
from typing import List

from flask import current_app, render_template
from flask_mail import Message

from app.extensions import mail
from app.user.models import User


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject: str, sender: str, recipients: List[str], text_body: str, html_body: str) -> None:
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)
    # Thread(target=send_async_email,
    #        args=(current_app._get_current_object(), msg)).start()


def send_password_reset_email(user: User):
    token = user.get_reset_password_token()
    send_email(subject='[My Flask App] Reset Your Password',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))


def send_confirm_email(user: User):
    token = user.get_confirmation_token()
    send_email(subject='[My Flask App] Confirm Your Email Address',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/confirm_email.txt',
                                         user=user, token=token),
               html_body=render_template('email/confirm_email.html',
                                         user=user, token=token))
