"""

By Ziqiu Li
Created at 2023/5/25 13:51
"""

from utils import repository
from models.group import Group


def create_group(name: str, desc: str = "") -> tuple[int, str]:
    group = repository.find_one_by(Group, "name", name)
    if group:
        return 1, "Group with same name exists."
    else:
        group = repository.create_one(Group, name=name, desc=desc)
        return 0, group.id


def delete_many_group(group_ids: list[str]) -> None:
    repository.delete_many(Group, group_ids)


def update_group(group_id: str, props: dict):
    return repository.update_one(Group, group_id, **props)


def find_group(group_id: str) -> tuple[int, str]:
    group = repository.find_one(Group, group_id)
    if group:
        return 0, group
    else:
        return 1, f"Group {group_id} not found."


def list_all_group():
    return repository.list_all(Group)
