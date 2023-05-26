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
        return 1, "Asset with same name exists."
    else:
        asset = repository.create_one(Asset, type=asset_type, desc=desc, value=value)
        return 0, asset.id


def delete_asset(asset_id: str) -> None:
    repository.delete_one(Asset, asset_id)


def delete_assets(asset_ids: List[str]) -> None:
    repository.delete_many(Asset, asset_ids)


def update_asset(asset_id: str, props: dict):
    if props.get("name"):
        asset_exists = repository.find_one_by(Asset, "name", props.get("name"))
        if asset_exists:
            return 2, "Asset with same name exists."
    result = repository.update_one(Asset, asset_id, **props)
    return result


def find_one(asset_id: str):
    asset = repository.find_one(Asset, asset_id)
    if asset:
        return 0, asset
    else:
        return 1, f"Asset {asset_id} is not found."


def list_all():
    return repository.list_all(Asset)
