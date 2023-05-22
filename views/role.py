"""
Role View

By Allen Tao
Created at 2023/4/10 11:15
"""
from flask import current_app as app
from apiflask.views import MethodView
from apiflask.schemas import EmptySchema

from schemas.common import IdsIn
from schemas.role import RoleOut, RoleIn, RoleWithPermissionsOut
import services.role as role_service
from utils.response import make_resp


class Role(MethodView):
    @app.output(RoleWithPermissionsOut)
    def get(self, role_id: str):
        code, res = role_service.find_role(role_id)
        return make_resp(code, res)

    @app.input(RoleIn)
    def post(self, role_in: dict):
        code, res = role_service.create_role(role_in["name"], role_in.get("desc"))
        if code == 0:
            return make_resp(res=res, msg="Created"), 201
        else:
            return make_resp(code, res)

    @app.input(RoleIn)
    def patch(self, role_id: str, role_in: dict):
        code, res = role_service.update_role(role_id, role_in)
        return make_resp(code, res, "Updated")


class Roles(MethodView):
    @app.output(RoleOut(many=True))
    def get(self):
        roles = role_service.list_all()
        return make_resp(res=roles)

    @app.input(IdsIn)
    @app.output(EmptySchema)
    def delete(self, roles_in):
        role_service.delete_roles(roles_in.get("ids"))


app.add_url_rule("/sys/role/<role_id>", view_func=Role.as_view("role"))
app.add_url_rule("/sys/role", view_func=Role.as_view("create_role"))
app.add_url_rule("/sys/roles", view_func=Roles.as_view("roles"))
