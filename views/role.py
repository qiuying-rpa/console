"""
Role View

By Allen Tao
Created at 2023/4/10 11:15
"""
from flask import current_app as app
from apiflask.views import MethodView
from apiflask.schemas import EmptySchema

from models.schemas.common import IdsIn
from models.schemas.role import RolePermissionsOut, RolesOut, RoleIn, RolePermissionsIn
import services.role as role_service


class Role(MethodView):

    @app.output(RolePermissionsOut)
    def get(self, role_id: str):
        role = role_service.find_role(role_id)
        if role:
            return {'data': role}
        else:
            return {'message': f'Role {role_id} not found.', 'code': 1}

    @app.input(RoleIn)
    def post(self, role_in: dict):
        code, result = role_service.create_role(role_in['name'], role_in['desc'])
        if code == 0:
            return {'data': result, 'message': 'Created.'}, 201
        else:
            return {'message': result, 'code': code}

    @app.input(RoleIn)
    @app.input(RolePermissionsIn)
    def patch(self, role_id: str, role_in: dict):
        code, res = role_service.update_role(role_id, role_in)
        if code == 0:
            return {'message': 'Updated.'}
        else:
            return {'message': res, 'code': code}


class Roles(MethodView):

    @app.output(RolesOut)
    def get(self):
        roles = role_service.list_all()
        return {'data': {'roles': roles}}

    @app.input(IdsIn)
    @app.output(EmptySchema)
    def delete(self, roles_in):
        role_service.delete_roles(roles_in.get('ids'))


app.add_url_rule('/role/<user_id>', view_func=Role.as_view('role'))
app.add_url_rule('/role', view_func=Role.as_view('create_role'))
app.add_url_rule('/roles', view_func=Roles.as_view('users'))
