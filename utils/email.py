"""

By Ziqiu Li
Created at 2023/3/30 9:01
"""
import smtplib
from smtplib import SMTP_SSL
from email.utils import formataddr
from email.utils import parseaddr
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from typing import Union

from utils.common import get_conf


def send_mail(subject: str, recipients: list[str], content: str,
              attachments: Union[None, list[tuple[bytes, str]]] = None):
    if attachments is None:
        attachments = []
    host = get_conf().get('email').get('host')
    port = get_conf().get('email').get('port')
    username = get_conf().get('email').get('username')
    password = get_conf().get('email').get('password')
    sender = get_conf().get('email').get('sender_name')
    recipients = recipients
    mime = MIMEMultipart()

    mime['Subject'] = Header(subject, 'utf-8')
    mime['From'] = formataddr((sender, username))
    mime['To'] = ';'.join([formataddr(parseaddr(r)) for r in recipients])
    mime.attach(MIMEText(content, 'plain', 'utf-8'))

    for file_bytes, file_name in attachments:
        attachment = MIMEApplication(file_bytes)
        attachment.add_header('Content-Disposition', 'attachment', filename=file_name)
        mime.attach(attachment)

    try:
        smtp = SMTP_SSL(host, port)
        smtp.login(username, password)
        smtp.sendmail(username, recipients, mime.as_string())
        smtp.quit()
        return True
    except smtplib.SMTPException as e:
        print(e)
        return False
