from threading import Thread
from typing import List, Optional

from flask import current_app
from flask_mail import Message

from app.extensions import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject: str,
               sender: str,
               recipients: List[str],
               text_body: str,
               html_body: str,
               attachments: Optional[List] = None,
               sync: bool = False) -> None:
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body

    if attachments:
        for attachment in attachments:
            msg.attach(*attachment)
    if sync:
        mail.send(msg)
    else:
        Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()
