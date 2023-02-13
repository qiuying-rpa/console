"""

By Allen Tao
Created at 2023/02/10 18:18
"""
from typing import Tuple, List

from models.pet import Pet
from utils import repository


def create_pet(name: str, gender: int) -> Tuple[int, str]:
    pet_exists = repository.find_one_by(Pet, 'name', name)
    if pet_exists:
        return 1, 'Pet with same name already exists.'
    else:
        pet = repository.create_one(Pet, name=name, gender=gender)
        return 0, pet.id


def delete_pet(pet_id: str) -> None:
    repository.delete_one(Pet, pet_id)


def delete_pets(pet_ids: List[str]) -> None:
    repository.delete_many(Pet, pet_ids)


def update_pet(pet_id: str, name: str = None, gender: int = None) -> str:
    props = {}
    if name:
        pet_exists = repository.find_other_with_same(Pet, pet_id, 'name', name)
        if pet_exists:
            return 'Pet with same name already exists.'
        else:
            props['name'] = name

    if gender:
        props['gender'] = gender

    result = repository.update_one(Pet, pet_id, **props)
    return '' if result else 'Fail to update.'


def find_pet(pet_id: str) -> Pet:
    pet = repository.find_one(Pet, pet_id)
    return pet


def find_all():
    return repository.list_all(Pet)
