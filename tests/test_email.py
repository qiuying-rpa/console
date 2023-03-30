"""

By Allen Tao
Created at 2023/03/30 22:06
"""
from utils.common import get_conf
from utils.email import send_mail


def test_email():
    if get_conf().get('email').get('password') != '':
        res = send_mail('Test Email', ['allen@tkzt.cn', 'taoqingqiu@gmail.com'], 'This is content.')
        assert res
