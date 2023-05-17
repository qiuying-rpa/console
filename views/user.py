"""

By Ziqiu Li
Created at 2023/3/24 14:43
"""
from flask import current_app as app
from apiflask.views import MethodView
from apiflask.schemas import EmptySchema

from schemas.common import IdsIn
from schemas.user import UserIn, UserOut
import services.user as user_service
from utils.encrypt import rsa_decrypt
from utils.response import make_resp, make_resp_concise


class User(MethodView):
    @app.output(UserOut)
    def get(self, user_id: str):
        code, res = user_service.find_user(user_id)
        return make_resp_concise(code, res)

    @app.input(UserIn)
    def post(self, user_in: dict):
        code, res = user_service.create_one(
            user_in["email"],
            rsa_decrypt(user_in["password"]),
            user_in.get("name"),
            False,
            user_in.get("verification_code"),
        )
        if code == 0:
            return make_resp(data=res, message="Created."), 201
        else:
            return make_resp_concise(code, res)

    @app.input(UserIn)
    def patch(self, user_id: str, user_in: dict):
        code, res = user_service.update_one(user_id, user_in)
        return make_resp_concise(code, res)


class Users(MethodView):
    @app.output(UserOut(many=True))
    def get(self):
        users = user_service.list_all()
        return make_resp(data=users)

    @app.input(IdsIn)
    @app.output(EmptySchema)
    def delete(self, users_in):
        user_service.delete_many(users_in.get("ids"))


app.add_url_rule("/sys/user/<user_id>", view_func=User.as_view("user"))
app.add_url_rule("/sys/user", view_func=User.as_view("createUser"))
app.add_url_rule("/sys/users", view_func=Users.as_view("users"))
