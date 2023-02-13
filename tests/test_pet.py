"""

By Allen Tao
Created at 2023/02/11 20:30
"""
from . import client, BASE_URL


created_pet_id = None


def test_create_pet():
    global created_pet_id
    res = client.post(BASE_URL + '/pet', json={'name': 'foo', 'gender': 0})
    created_pet_id = res.get_json().get('data')

    assert res.status_code == 201
    assert created_pet_id


def test_create_pet_repeat():
    global created_pet_id
    res = client.post(BASE_URL + '/pet', json={'name': 'foo', 'gender': 1})

    assert res.status_code == 409


def test_get_pet():
    res = client.get(BASE_URL + '/pet/' + created_pet_id)
    data = res.get_json().get('data')

    assert res.status_code == 200
    assert data.get('name') == 'foo'
    assert data.get('id') == created_pet_id


def test_get_pets():
    res = client.get(BASE_URL + '/pets')
    pets = res.get_json().get('data').get('pets')

    assert res.status_code == 200
    assert any(map(lambda x: x.get('name') == 'foo', pets))


def test_update_pet():
    client.put(BASE_URL + '/pet/' + created_pet_id, json={'name': 'bar', 'gender': 1})
    res = client.get(BASE_URL + '/pet/' + created_pet_id)
    data = res.get_json().get('data')

    assert res.status_code == 200
    assert data.get('name') == 'bar'


def test_update_pet_partial():
    client.patch(BASE_URL + '/pet/' + created_pet_id, json={'name': 'quz'})
    res = client.get(BASE_URL + '/pet/' + created_pet_id)
    data = res.get_json().get('data')

    assert res.status_code == 200
    assert data.get('name') == 'quz'


def test_update_pet_repeat():
    client.post(BASE_URL + '/pet', json={'name': 'bar', 'gender': 0})
    res = client.patch(BASE_URL + '/pet/' + created_pet_id, json={'name': 'bar'})

    assert res.status_code == 409


def test_delete():
    res = client.delete(BASE_URL + '/pet/' + created_pet_id)

    assert res.status_code == 204

    res = client.get(BASE_URL + '/pet/' + created_pet_id)
    data = res.get_json().get('data')

    assert data is None


def test_delete_many():
    client.post(BASE_URL + '/pet', json={'name': 'foo', 'gender': 0})
    pets = client.get(BASE_URL + '/pets').get_json().get('data').get('pets')

    assert len(pets) > 0

    client.delete(BASE_URL + '/pets', json={'ids': list(map(lambda x: x.get('id'), pets))})

    pets = client.get(BASE_URL + '/pets').get_json().get('data').get('pets')

    assert len(pets) == 0



