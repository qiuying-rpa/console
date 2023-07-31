"""

By Ziqiu Li
Created at 2023/5/25 14:17
"""
from utils import repository
from models.param_config import ParamConfig
import json
from flask import g
from sqlalchemy import select


def create_param_config(
    name: str, params: str, desc: str, process_id: str
) -> tuple[int, str]:
    # 同用户同process下name不重复
    param_config = repository.find(
        select(ParamConfig).filter_by(
            name=name, user_id=g.current_user["id"], process_id=process_id
        ),
        first=True,
    )
    if param_config:
        return 1, f"Param config with same name exists."
    param_config = repository.create_one(
        ParamConfig,
        name=name,
        params=json.dumps(params),
        desc=desc,
        process_id=process_id,
        user_id=g.current_user["id"],
    )
    return 0, param_config.id


def delete_param_config(param_config_id: str) -> None:
    repository.delete_one(ParamConfig, param_config_id)


def delete_param_configs(ids: list[str]) -> None:
    repository.delete_many(ParamConfig, ids)


def update_param_config(param_config_id: str, props: dict):
    if props.get("name"):
        param_config = repository.find(
            select(ParamConfig)
            .filter_by(
                name=props.get("name"),
                user_id=g.current_user["id"],
                process_id=props["process_id"],
            )
            .filter(ParamConfig.id.isnot(param_config_id)),
            first=True,
        )
        if param_config:
            return 1, f"Param config with same name exists."
    if props.get("params"):
        props["params"] = json.dumps(props["params"])
    return repository.update_one(ParamConfig, param_config_id, **props)


def find_param_config(param_config_id):
    param_config = repository.find_one(ParamConfig, param_config_id)
    if param_config:
        return 0, param_config
    else:
        return 1, f"Param config {param_config_id} not found."


def find_param_configs(props):
    return repository.find(
        select(ParamConfig).filter_by(
            user_id=g.current_user["id"], process_id=props["process_id"]
        )
    )
