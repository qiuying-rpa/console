"""

By Ziqiu Li
Created at 2023/3/24 14:43
"""
from flask import current_app as app
from apiflask.views import MethodView
from apiflask.schemas import EmptySchema

from models.schemas.auth import TokenIn, RefreshTokenIn
from models.schemas.user import UserOut, UserIn, UsersOut, UsersIn
from models.schemas.verification import VerificationIn
import services.user as user_services
import services.auth as auth_services


class User(MethodView):

    @app.output(UserOut)
    def get(self, user_id: str):
        user = user_services.find_user(user_id)
        if user:
            return {"data": user}

    @app.input(UserIn)
    def post(self, user_in: dict):
        code, result = user_services.create_one(user_in['mail'],
                                                user_in['password'],
                                                user_in.get('name'),
                                                user_in.get('tel'),
                                                user_in.get('is_admin', False),
                                                user_in.get('verification_code'))
        if code == 0:
            return {"data": result, "message": "Created."}, 201
        else:
            return {"message": result}, 409

    @app.input(UserIn)
    def put(self, user_id: str, user_in: dict):
        result = user_services.update_one(user_id, user_in)
        if result:
            return {"message": result}, 409
        return {"message": "Updated."}


class Users(MethodView):

    @app.output(UsersOut)
    def get(self):
        users = user_services.list_all()
        return {'data': {'users': users}}

    @app.input(UsersIn)
    @app.output(EmptySchema, status_code=204)
    def delete(self, users_in):
        user_services.delete_many(users_in.get('ids'))


class Token(MethodView):

    @app.input(TokenIn)
    def post(self, token_in):
        code, res = auth_services.login(token_in['mail'], token_in['password'])
        if code:
            return {"message": res}, 400
        else:
            return {"data": {
                'access_token': res[0],
                'refresh_token': res[1]
            }}, 201

    @app.input(RefreshTokenIn)
    def put(self, refresh_token_in):
        code, res = auth_services.refresh(refresh_token_in['user_id'], refresh_token_in['refresh_token'])
        if code:
            return {"message": res}, 400
        else:
            return {"data": {
                'access_token': res[0],
                'refresh_token': res[1]
            }}, 200


class Verification(MethodView):
    @app.input(VerificationIn)
    @app.output(EmptySchema, status_code=201)
    def post(self, verification_in):
        user_services.send_verification_code(verification_in['mail'])
        return {'message': 'done.'}, 201


app.add_url_rule('/user/<user_id>', view_func=User.as_view('user'))
app.add_url_rule('/user', view_func=User.as_view('createUser'))
app.add_url_rule('/users', view_func=Users.as_view('users'))
app.add_url_rule('/token', view_func=Token.as_view('login'))
app.add_url_rule('/verification', view_func=Verification.as_view('verification'))
