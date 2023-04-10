"""
Role CRUD

By Allen Tao
Created at 2023/4/10 11:39
"""
from models.role import Role
from utils import repository
from utils.common import get_conf


def find_role(role_id):
    role = repository.find_one(Role, role_id)
    return role


def create_role(name: str, desc: str):
    role_exists = repository.find_one_by(Role, 'name', name)
    if role_exists:
        return 1, 'Role with same name exists.'
    else:
        role = repository.create_one(Role, name=name, desc=desc)
        return 0, role.id


def update_role(role_id, role_props):
    return repository.update_one(Role, role_id, **role_props)


def list_all():
    return repository.list_all(Role)


def create_default():
    role_exists = repository.find_one_by(Role, 'is_default', True)
    if role_exists:
        return 1, 'Default role already exists.'
    else:
        conf = get_conf().get('app')
        role = repository.create_one(
            Role, name=conf.get('default_role_name'), desc=conf.get('default_role_desc'), is_default=True)
        return 0, role.id


def delete_roles(ids: list[str]):
    repository.delete_many(Role, ids)
