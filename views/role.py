"""
Role View

By Allen Tao
Created at 2023/4/10 11:15
"""
from flask import current_app as app
from apiflask.views import MethodView
from apiflask.schemas import EmptySchema

from schemas.common import IdsIn
from schemas.role import RolePermissionsOut, RoleOut, RoleIn
import services.role as role_service
from utils.response import make_resp, make_resp_concise


class Role(MethodView):
    @app.output(RolePermissionsOut)
    def get(self, role_id: str):
        code, res = role_service.find_role(role_id)
        return make_resp_concise(code, res)

    @app.input(RoleIn(partial=True))
    def post(self, role_in: dict):
        code, res = role_service.create_role(role_in["name"], role_in.get("desc"))
        if code == 0:
            return make_resp(data=res, message="Created"), 201
        else:
            return make_resp_concise(code, res)

    @app.input(RoleIn(partial=True))
    def patch(self, role_id: str, role_in: dict):
        code, res = role_service.update_role(role_id, role_in)
        return make_resp(code, res, "Updated.")


class Roles(MethodView):
    @app.output(RoleOut(many=True))
    def get(self):
        roles = role_service.list_all()
        return make_resp(data=roles)

    @app.input(IdsIn)
    @app.output(EmptySchema)
    def delete(self, roles_in):
        role_service.delete_roles(roles_in.get("ids"))


app.add_url_rule("/role/<user_id>", view_func=Role.as_view("role"))
app.add_url_rule("/role", view_func=Role.as_view("create_role"))
app.add_url_rule("/roles", view_func=Roles.as_view("roles"))
