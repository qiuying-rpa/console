"""
Role CRUD

By Allen Tao
Created at 2023/4/10 11:39
"""

from models.role import Role
from utils import repository
from utils.common import get_conf
from sqlalchemy import select


def find_role(role_id):
    role = repository.find_one(Role, role_id)
    if role:
        return 0, role
    else:
        return 1, f"Role {role_id} not found."


def create_role(name: str, desc: str):
    role_exists = repository.find(select(Role).filter_by(name=name))
    if role_exists:
        return 1, "Role with same name exists."
    else:
        role = repository.create_one(Role, name=name, desc=desc)
        return 0, role.id


def update_role(role_id, role_props):
    role = repository.find_one(Role, role_id)
    if role:
        if role.is_default:
            return 2, "Default role cannot be modified :/"
        else:
            if new_name := role_props.get("name"):
                exists_role = repository.find(
                    select(Role).filter_by(name=new_name).filter(Role.id.isnot(role_id))
                )
                # exists_role = repository.find_other_with_same(
                #     Role, role_id, "name", new_name
                # )
                if exists_role:
                    return 3, "Role with same name already exists."
            return repository.update_one(Role, role_id, **role_props)
    else:
        return 4, "Target role not found."


def list_all():
    return repository.find(select(Role))


def create_default():
    role_exists = repository.find(select(Role).filter_by(is_default=True), first=True)
    if not role_exists:
        conf = get_conf().get("app")
        repository.create_one(
            Role,
            name=conf.get("default_role_name"),
            desc=conf.get("default_role_desc"),
            is_default=True,
        )


def delete_roles(ids: list[str]):
    default_role = repository.find(select(Role).filter_by(is_default=True), first=True)
    repository.delete_many(Role, list(filter(lambda x: x != default_role.id, ids)))
