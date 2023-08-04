"""

By Ziqiu Li
Created at 2023/5/25 13:51
"""

from utils import repository
from models.group import Group
from sqlalchemy import select


def create_group(name: str, desc: str = "") -> tuple[int, str]:
    group = repository.find(select(Group).filter_by(name=name), first=True)
    if group:
        return 1, "Group with same name exists."
    else:
        group = repository.create_one(Group, name=name, desc=desc)
        return 0, group.id


def delete_group(group_id: str) -> None:
    repository.delete_one(Group, group_id)


def delete_groups(group_ids: list[str]) -> None:
    repository.delete_many(Group, group_ids)


def update_group(group_id: str, props: dict):
    return repository.update_one(Group, group_id, **props)


def find_group(group_id: str) -> tuple[int, str]:
    group = repository.find_one(Group, group_id)
    if group:
        return 0, group
    else:
        return 1, f"Group {group_id} not found."


def find_groups(props: dict) -> list[Group]:
    return repository.find(
        select(Group).filter(Group.name.contains(props.get("name", ""))),
        page=props["page"],
        size=props["size"],
    )
