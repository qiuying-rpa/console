"""

By Ziqiu Li
Created at 2023/3/24 14:43
"""
from flask import current_app as app
from apiflask.views import MethodView
from apiflask.schemas import EmptySchema

from schemas.common import IdsIn
from schemas.user import UserAdminIn, UserOut, UserRolesIn, UserNameOut
import services.user as user_service
from utils.encrypt import rsa_decrypt
from utils.response import make_resp


class User(MethodView):
    @app.output(UserOut)
    def get(self, user_id: str):
        code, res = user_service.find_user(user_id)
        return make_resp(code, res)

    @app.input(UserAdminIn)
    def put(self, user_id: str, user_in: dict):
        code, res = user_service.update_one(user_id, user_in)
        return make_resp(code, res, "Updated")


class Users(MethodView):
    @app.input(UserAdminIn)
    def post(self, user_in: dict):
        code, res = user_service.create_user_by_admin(
            user_in["email"],
            rsa_decrypt(user_in["password"]),
            user_in.get("name"),
            user_in.get("roles"),
        )
        if code == 0:
            return make_resp(code, res, "Created"), 201
        else:
            return make_resp(code, res)

    @app.output(UserOut(many=True))
    def get(self):
        users = user_service.list_all()
        return make_resp(res=users)

    @app.input(IdsIn)
    @app.output(EmptySchema)
    def delete(self, users_in):
        user_service.delete_many(users_in.get("ids"))

    @app.input(UserRolesIn)
    def patch(self, user_in: dict):
        code, res = user_service.update_roles(
            user_in["ids"], user_in["roles"], user_in["action"]
        )
        return make_resp(code, res, "Updated")


class BriefUsers(MethodView):
    # Just output  id and name
    # Can filter by roles and action
    @app.input(UserRolesIn, "query")
    @app.output(UserNameOut(many=True))
    def get(self, user_in):
        if user_in:
            users = user_service.find_users_by(user_in)
        else:
            users = user_service.list_all()
        return make_resp(res=users)


app.add_url_rule("/sys/user/<user_id>", view_func=User.as_view("user"))
app.add_url_rule("/sys/users", view_func=Users.as_view("users"))
app.add_url_rule("/sys/brief-users", view_func=BriefUsers.as_view("briefUsers"))
