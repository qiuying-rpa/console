"""

By Allen Tao
Created at 2023/02/11 20:30
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


@pytest.mark.run(order=0)
def test_create_pet(set_global):
    res = client.post(BASE_URL + '/pet', json={'name': 'foo', 'gender': 0})
    created_pet_id = res.get_json().get('data')

    assert res.status_code == 201
    assert created_pet_id

    set_global('pet_id', created_pet_id)


@pytest.mark.run(order=1)
def test_create_pet_repeat():
    res = client.post(BASE_URL + '/pet', json={'name': 'foo', 'gender': 1})

    assert res.status_code == 409


@pytest.mark.run(order=2)
def test_get_pet(get_global):
    created_pet_id = get_global('pet_id')
    res = client.get(BASE_URL + '/pet/' + created_pet_id)
    data = res.get_json().get('data')

    assert res.status_code == 200
    assert data.get('name') == 'foo'
    assert data.get('id') == created_pet_id


@pytest.mark.run(order=3)
def test_get_pets():
    res = client.get(BASE_URL + '/pets')
    pets = res.get_json().get('data').get('pets')

    assert res.status_code == 200
    assert any(map(lambda x: x.get('name') == 'foo', pets))


@pytest.mark.run(order=4)
def test_update_pet(get_global):
    created_pet_id = get_global('pet_id')
    client.put(BASE_URL + '/pet/' + created_pet_id, json={'name': 'bar', 'gender': 1})
    res = client.get(BASE_URL + '/pet/' + created_pet_id)
    data = res.get_json().get('data')

    assert res.status_code == 200
    assert data.get('name') == 'bar'


@pytest.mark.run(order=5)
def test_update_pet_partial(get_global):
    created_pet_id = get_global('pet_id')
    client.patch(BASE_URL + '/pet/' + created_pet_id, json={'name': 'quz'})
    res = client.get(BASE_URL + '/pet/' + created_pet_id)
    data = res.get_json().get('data')

    assert res.status_code == 200
    assert data.get('name') == 'quz'


@pytest.mark.run(order=6)
def test_update_pet_repeat(get_global):
    created_pet_id = get_global('pet_id')
    client.post(BASE_URL + '/pet', json={'name': 'bar', 'gender': 0})
    res = client.patch(BASE_URL + '/pet/' + created_pet_id, json={'name': 'bar'})

    assert res.status_code == 409


@pytest.mark.run(order=7)
def test_delete(get_global):
    created_pet_id = get_global('pet_id')
    res = client.delete(BASE_URL + '/pet/' + created_pet_id)

    assert res.status_code == 204

    res = client.get(BASE_URL + '/pet/' + created_pet_id)
    data = res.get_json().get('data')

    assert data is None


@pytest.mark.run(order=8)
def test_delete_many():
    client.post(BASE_URL + '/pet', json={'name': 'foo', 'gender': 0})
    pets = client.get(BASE_URL + '/pets').get_json().get('data').get('pets')

    assert len(pets) > 0

    client.delete(BASE_URL + '/pets', json={'ids': list(map(lambda x: x.get('id'), pets))})

    pets = client.get(BASE_URL + '/pets').get_json().get('data').get('pets')

    assert len(pets) == 0



