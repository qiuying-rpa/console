"""

By Ziqiu Li
Created at 2023/5/25 13:57
"""

import services.group as group_service
from flask import current_app as app
from apiflask.views import MethodView
from apiflask.schemas import EmptySchema
from schemas.group import GroupIn, GroupOut
from schemas.common import IdsIn
from utils.response import make_resp


class Group(MethodView):
    @app.output(GroupOut)
    def get(self, group_id):
        code, res = group_service.find_group(group_id)
        return make_resp(code, res)

    @app.input(GroupIn)
    def post(self, group_in):
        code, res = group_service.create_group(group_in["name"], group_in.get("desc"))
        return make_resp(code, res, msg="Created.")

    @app.input(GroupIn)
    def patch(self, group_id, group_in):
        code, res = group_service.update_group(group_id, group_in)
        return make_resp(code, res, msg="Updated.")


class Groups(MethodView):
    @app.input(IdsIn)
    @app.output(EmptySchema)
    def delete(self, ids_in):
        group_service.delete_many_group(ids_in["ids"])

    @app.output(GroupOut(many=True))
    def get(self):
        groups = group_service.list_all_group()
        return make_resp(res=groups)


app.add_url_rule("/console/group/<group_id>", view_func=Group.as_view("group"))
app.add_url_rule("/console/group", view_func=Group.as_view("createGroup"))
app.add_url_rule("/console/groups", view_func=Groups.as_view("groups"))
