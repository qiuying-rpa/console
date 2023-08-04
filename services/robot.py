"""

By Ziqiu Li
Created at 2023/5/25 14:06
"""

from utils import repository
from models.robot import Robot
from models.group import Group
from models.user import User
from sqlalchemy import select


def create_robot(
    name: str, ip: str, desc: str, owner_id: str, group_id: str
) -> tuple[int, str]:
    if group_id:
        group = repository.find_one(Group, group_id)
        if group is None:
            return 2, f"Group {group_id} not found."
    if owner_id:
        owner = repository.find_one(User, owner_id)
        if owner is None:
            return 3, f"Owner {owner_id} not found"

    robot = repository.find(select(Robot).filter_by(name=name))
    if robot:
        return 1, "Robot with same name exists."
    else:
        robot = repository.create_one(
            Robot,
            name=name,
            ip=ip,
            desc=desc,
            owner_id=owner_id,
            status="offline",
            group_id=group_id,
        )
        return 0, robot.id


def delete_robot(robot_id: str) -> None:
    repository.delete_one(Robot, robot_id)


def delete_robots(robot_ids: list[str]) -> None:
    repository.delete_many(Robot, robot_ids)


def update_robot(robot_id, props: dict) -> tuple[int, str]:
    if props.get("group_id"):
        group = repository.find_one(Group, props["group_id"])
        if group is None:
            return 2, f'Group {props["group_id"]} not found.'
    if props.get("owner_id"):
        owner = repository.find_one(User, props["owner_id"])
        if owner is None:
            return 3, f'Owner {props["owner_id"]} not found'
    return repository.update_one(Robot, robot_id, **props)


def find_robot(robot_id):
    robot = repository.find_one(Robot, robot_id)
    if robot:
        return 0, robot
    else:
        return 1, f"Robot {robot_id} not found."


def find_robots(props: dict):
    return repository.find(
        select(Robot)
        .join(Group, isouter=True)
        .filter(Group.name.contains(props.get("group_name", "")))
        .filter(Robot.name.contains(props.get("name", ""))),
        page=props["page"],
        size=props["size"],
    )
