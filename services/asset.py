"""

By Ziqiu Li
Created at 2023/2/19 21:45
"""
from typing import Tuple, List
from models.asset import Asset
from utils import repository


def create_asset(name: str, asset_type: str, desc: str, value: str) -> Tuple[int, str]:
    asset_exists = repository.find_one_by(Asset, "name", name)
    if asset_exists:
        return 1, "Asset with same name is exists."
    else:
        asset = repository.create_one(Asset, type=asset_type, desc=desc, value=value)
        return 0, asset.id


def delete_asset(asset_id: str) -> None:
    repository.delete_one(Asset, asset_id)


def delete_assets(asset_ids: List[str]) -> None:
    repository.delete_many(Asset, asset_ids)


def update_asset(asset_id: str, name: str, asset_type: str, desc: str, value: str) -> str:
    props = {}
    if name:
        asset_exists = repository.find_one_by(Asset, "name", name)
        if asset_exists:
            return "Asset with same name is exists."
        else:
            props["name"] = props

    if asset_type:
        props["type"] = asset_type

    if desc:
        props["desc"] = desc

    if value:
        props["value"] = value

    result = repository.update_one(Asset, asset_id, props)
    return "" if result else "Fail to update."


def find_one(asset_id: str) -> Asset:
    return repository.find_one(Asset, asset_id)


def find_all():
    return repository.list_all(Asset)



