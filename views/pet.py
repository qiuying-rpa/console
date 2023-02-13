"""

By Allen Tao
Created at 2023/02/10 15:49
"""
from flask import current_app as app
from apiflask.views import MethodView
from apiflask.schemas import EmptySchema

from models.schemas.pet import PetOut, PetIn, PetsOut, PetsIn
import services.pet as pet_service


class Pet(MethodView):

    @app.output(PetOut)
    def get(self, pet_id: str):
        pet = pet_service.find_pet(pet_id)
        if pet:
            return {'data': pet}

    @app.input(PetIn(partial=True))
    def post(self, pet_in: dict):
        code, result = pet_service.create_pet(pet_in['name'], pet_in['gender'])
        if code == 0:
            return {'data': result, 'message': 'Created.'}, 201
        else:
            return {'message': result}, 409

    @app.output(EmptySchema, status_code=204)
    def delete(self, pet_id: str):
        pet_service.delete_pet(pet_id)

    @app.input(PetIn)
    def put(self, pet_id: str, pet_in: dict):
        result = pet_service.update_pet(pet_id, **pet_in)
        if result:
            return {'message': result}, 409
        return {'message': 'Updated.'}

    @app.input(PetIn(partial=True))
    def patch(self, pet_id: str, pet_in: dict):
        result = pet_service.update_pet(pet_id, **pet_in)
        if result:
            return {'message': result}, 409
        return {'message': 'Updated.'}


class Pets(MethodView):

    @app.output(PetsOut)
    def get(self):
        pets = pet_service.find_all()
        return {'data': {'pets': pets}}

    @app.input(PetsIn)
    @app.output(EmptySchema, status_code=204)
    def delete(self, pets_in: dict):
        pet_service.delete_pets(pets_in.get('ids'))


app.add_url_rule('/pet/<pet_id>', view_func=Pet.as_view('pet'))
app.add_url_rule('/pet', view_func=Pet.as_view('create_pet'))
app.add_url_rule('/pets', view_func=Pets.as_view('pets'))
