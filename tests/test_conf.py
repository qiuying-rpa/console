"""
Configuration Tests

By Allen Tao
Created at 2023/03/28 21:19
"""


def test_conf():
    from utils.common import get_conf
    conf = get_conf()
    assert conf.get('auth').get('admin_password') == '123456'
