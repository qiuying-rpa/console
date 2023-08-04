"""

By Ziqiu Li
Created at 2023/5/25 14:23
"""
from models.group import Group
from models.process import Process
from models.user import User
from utils import repository
from datetime import datetime
from flask import g
from sqlalchemy import select


def create_process(
    name: str,
    start_params: str,
    nodes: str,
    desc: str,
    template: str,
    developer_id: str,
    demander_id: str,
    group_id: str,
) -> tuple[int, str]:
    process_exists = repository.find(select(Process).filter_by(name=name))
    if process_exists:
        return 1, "Process is already exists."
    else:
        group = repository.find_one(Group, group_id)
        if group is None:
            return 2, f"Group {group_id} not found."
        developer = repository.find_one(User, developer_id)
        if developer is None:
            return 3, f"Developer {developer_id} not found."
        demander = repository.find_one(User, demander_id)
        if demander is None:
            return 4, f"Demander {demander_id} not found."
        process = repository.create_one(
            Process,
            name=name,
            start_params=start_params,
            nodes=nodes,
            desc=desc,
            template=template,
            updater_id=g.current_user["id"],
            developer_id=developer_id,
            demander_id=demander_id,
            group_id=group_id,
        )
        return 0, process.id


def delete_process(process_id: str) -> None:
    repository.delete_one(Process, process_id)


def delete_processes(process_ids: list[str]) -> None:
    repository.delete_many(Process, process_ids)


def update_process(process_id: str, props):
    if props.get("group_id"):
        group = repository.find_one(Group, props["group_id"])
        if group is None:
            return 2, f'Group {props["group_id"]} not found.'
    if props.get("developer_id"):
        developer = repository.find_one(User, props.get("developer_id"))
        if developer is None:
            return 2, f'Developer {props.get("developer_id")} not found.'
    if props.get("demander_id"):
        demander = repository.find_one(User, props.get("demander_id"))
        if demander is None:
            return 3, f'Demander {props.get("demander_id")} not found.'
    props["updater_id"] = g.current_user["id"]
    props["update_time"] = datetime.now()
    return repository.update_one(Process, process_id, **props)


def find_process(process_id: str):
    process = repository.find_one(Process, process_id)
    if process:
        return 0, process
    else:
        return 1, f"Process {process_id} not found."


def find_processes(props: dict) -> list[Process]:
    # developer_name = props.get('developer_name', '')
    # if props.get('developer_name'):
    #     del props['developer_name']
    # group_name = props.get('group_name', '')
    # if props.get('group_name'):
    #     del props['group_name']
    # page = props['page']
    # del props['page']
    # size = props['size']
    # del props['size']
    return repository.find(
        select(Process)
        .join(User, Process.developer_id == User.id)
        .join(Group, isouter=True)
        .filter(User.name.contains(props.get("developer_name", "")))
        .filter(Group.name.contains(props.get("group_name", "")))
        .filter(Process.name.contains(props.get("name", ""))),
        page=props["page"],
        size=props["size"],
    )
