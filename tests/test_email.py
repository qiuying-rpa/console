"""

By Allen Tao
Created at 2023/03/30 22:06
"""
import pytest

from utils.common import get_conf
from utils.email import send_mail


@pytest.mark.skipif(
    not get_conf().get("email").get("sender_password"),
    reason="no password found in conf.toml",
)
def test_email():
    res = send_mail(
        "Test Email",
        ["yoghurtoreo@163.com", "taoqingqiu@gmail.com"],
        "This is content.",
    )
    assert res


@pytest.mark.skipif(
    not get_conf().get("email").get("sender_password"),
    reason="no password found in conf.toml",
)
def test_email_send_attachment():
    res = send_mail(
        "Test Attachment Email",
        ["taoqingqiu@gmail.com"],
        "This is content.",
        [(open("README.md", "rb").read(), "README.md")],
    )
    assert res
