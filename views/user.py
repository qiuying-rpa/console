"""

By Ziqiu Li
Created at 2023/3/24 14:43
"""
from flask import current_app as app
from apiflask.views import MethodView
from apiflask.schemas import EmptySchema

from models.schemas.common import IdsIn
from models.schemas.user import UserOut, UserIn, UsersOut
import services.user as user_service
from utils.encrypt import rsa_decrypt


class User(MethodView):
    @app.output(UserOut)
    def get(self, user_id: str):
        user = user_service.find_user(user_id)
        if user:
            return {"data": user}
        else:
            return {"message": f"User {user_id} not found.", "code": 1}

    @app.input(UserIn)
    def post(self, user_in: dict):
        code, result = user_service.create_one(
            user_in["email"],
            rsa_decrypt(user_in["password"]),
            user_in.get("name"),
            False,
            user_in.get("verification_code"),
        )
        if code == 0:
            return {"data": result, "message": "Created."}, 201
        else:
            return {"message": result, "code": code}

    @app.input(UserIn)
    def patch(self, user_id: str, user_in: dict):
        code, res = user_service.update_one(user_id, user_in)
        if code != 0:
            return {"message": res, "code": code}
        else:
            return {"message": "Updated."}


class Users(MethodView):
    @app.output(UsersOut)
    def get(self):
        users = user_service.list_all()
        return {"data": {"users": users}}

    @app.input(IdsIn)
    @app.output(EmptySchema)
    def delete(self, users_in):
        user_service.delete_many(users_in.get("ids"))


app.add_url_rule("/user/<user_id>", view_func=User.as_view("user"))
app.add_url_rule("/user", view_func=User.as_view("createUser"))
app.add_url_rule("/users", view_func=Users.as_view("users"))
