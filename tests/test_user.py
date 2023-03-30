"""

By Ziqiu Li
Created at 2023/3/24 17:55
"""
import pytest

from . import client, BASE_URL
from utils.repository import use_redis

_global = {}


@pytest.fixture
def set_global():
    def _set_global(key, value):
        _global[key] = value
    return _set_global


@pytest.fixture
def get_global():
    def _get_global(key):
        return _global.get(key)
    return _get_global


@pytest.mark.run(order=0)
def test_create_user_admin(set_global):
    res = client.post(BASE_URL + '/user', json={
        'mail': 'admin@qiuying.com',
        'password': '123456',
        'is_admin': True
    })
    admin_user_id = res.get_json().get('data')

    assert res.status_code == 201
    assert type(admin_user_id) == str and len(admin_user_id) > 0

    set_global('admin_id', admin_user_id)


@pytest.mark.run(order=1)
def test_verification():
    res = client.post(BASE_URL + '/verification', json={"mail": "lcmail1001@163.com"})
    assert res.status_code == 204


@pytest.mark.run(order=2)
def test_create_user(set_global):
    redis_conn = use_redis()
    verification_code = redis_conn.get('lcmail1001@163.com')
    res = client.post(BASE_URL + '/user', json={
        'name': '李子秋',
        'mail': 'lcmail1001@163.com',
        'password': '654321',
        'is_admin': False,
        'verification_code': verification_code
    })
    other_user_id = res.get_json().get('data')

    assert res.status_code == 201
    assert type(other_user_id) == str and len(other_user_id) > 0

    set_global('other_id', other_user_id)


@pytest.mark.run(order=3)
def test_create_user_again():
    res = client.post(BASE_URL + '/user', json={
        'name': '李子秋',
        'mail': 'lcmail1001@163.com',
        'password': '1',
    })

    assert res.status_code == 409


@pytest.mark.run(order=4)
def test_login_admin():
    res = client.post(BASE_URL + '/token', json={
        'mail': 'admin@qiuying.com',
        'password': '123456'
    })
    token = res.get_json().get('data').get('token')

    assert res.status_code == 200
    assert type(token) == str and len(token) > 0


@pytest.mark.run(order=5)
def test_get_user_info(get_global):
    admin_user_id = get_global('admin_id')
    other_user_id = get_global('other_id')
    # admin
    res = client.get(BASE_URL + '/user/' + admin_user_id)
    admin_user_info = res.get_json().get('data')

    assert 'admin' == admin_user_info['name']
    assert 'admin@qiuying.com' == admin_user_info['mail']
    assert admin_user_info['is_admin']
    # assert '123456' == admin_user_info['password']
    # other
    res = client.get(BASE_URL + '/user/' + other_user_id)
    other_user_info = res.get_json().get('data')
    assert '李子秋' == other_user_info['name']
    assert not other_user_info['is_admin']


@pytest.mark.run(order=6)
def test_update_user(get_global):
    other_user_id = get_global('other_id')

    res = client.put(BASE_URL + '/user/' + other_user_id, json={
        'tel': '12345678901'
    })
    assert res.status_code == 200
    res = client.get(BASE_URL + '/user/' + other_user_id)
    assert '12345678901' == res.get_json().get('data')['tel']


@pytest.mark.run(order=7)
def test_get_all_users():
    res = client.get(BASE_URL + '/users')
    users = res.get_json().get('data')['users']
    assert 1 == len(users)


@pytest.mark.run(order=8)
def test_delete_users():
    res = client.get(BASE_URL + '/users')
    user_ids = [i["id"] for i in res.get_json().get('data')['users']]
    client.delete(BASE_URL + '/users', json={
        'ids': user_ids
    })
    res = client.get(BASE_URL + '/users')
    users = res.get_json().get('data')["users"]
    assert 0 == len(users)


def test_verification_code():
    res = client.get(BASE_URL + '/verification')

    assert res.status_code == 201
