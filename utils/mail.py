"""

By Ziqiu Li
Created at 2023/3/30 9:01
"""
from typing import Union
from flask_mail import Mail, Message

_mail: Union[Mail, None] = None


def use_mail(app=None):
    global _mail
    if app is not None:
        _mail = Mail(app)
    return _mail


def send_mail(subject, recipient, body, sender: Union[str, None] = None, attachments: Union[list, None] = None):
    msg = Message(subject,
                  recipients=[recipient],
                  body=body,
                  sender=sender,
                  attachments=attachments)
    _mail.send(msg)

