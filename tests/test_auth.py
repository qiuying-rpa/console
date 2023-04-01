"""

By Allen Tao
Created at 2023/04/01 16:59
"""
import pytest
from . import client, BASE_URL

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


@pytest.mark.run(order=1)
def test_auth_login(set_global):
    res = client.post(BASE_URL+'/token', json={
        'mail': 'admin@qiuying.com',
        'password': '123456',
    })
    data = res.get_json().get('data')
    assert res.status_code == 201
    assert len(data.get('access_token')) > 0
    assert len(data.get('refresh_token')) > 0

    set_global('refresh_token', data.get('refresh_token'))


@pytest.mark.run(order=2)
def test_auth_refresh_token(get_global):
    res = client.put(BASE_URL + '/token', json={
        'refresh_token': get_global('refresh_token'),
        'user_id': '5d658069-fbb1-467c-aab4-54555eaab683',
    })
    data = res.get_json().get('data')

    assert res.status_code == 200
    assert len(data.get('access_token')) > 0
    assert len(data.get('refresh_token')) > 0
