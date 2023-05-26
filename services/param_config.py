"""

By Ziqiu Li
Created at 2023/5/25 14:17
"""
from utils import repository
from models.param_config import ParamConfig
import json


def create_param_config(
    name: str, params: str, desc: str, process_id: str
) -> tuple[int, str]:
    # todo 同用户下name不重复
    param_config = repository.create_one(
        ParamConfig,
        name=name,
        params=json.dumps(params),
        desc=desc,
        process_id=process_id,
    )
    return 0, param_config.id


def delete_many_param_config(ids: list[str]) -> None:
    repository.delete_many(ParamConfig, ids)


def update_param_config(param_config_id: str, props: dict):
    if props.get("params"):
        props["params"] = json.dumps(props["params"])
    return repository.update_one(ParamConfig, param_config_id, **props)


def find_param_config(param_config_id):
    param_config = repository.find_one(ParamConfig, param_config_id)
    if param_config:
        return 0, param_config
    else:
        return 1, f"Param config {param_config_id} not found."


def find_param_configs_by(props: dict):
    return repository.find_many_by(ParamConfig, **props)


def list_all_param_config():
    return repository.list_all(ParamConfig)
