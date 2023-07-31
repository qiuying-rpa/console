"""

By Ziqiu Li
Created at 2023/5/25 15:15
"""
from flask import current_app as app
from schemas.process import ProcessIn, ProcessOut, ProcessQuery
from apiflask.views import MethodView
import services.process as process_service
from schemas.common import IdsIn
from apiflask.schemas import EmptySchema
from utils.response import make_resp


class Process(MethodView):
    @app.output(ProcessOut)
    def get(self, process_id: str):
        code, res = process_service.find_process(process_id)
        return make_resp(code, res)

    @app.input(ProcessIn)
    def patch(self, process_id, process_in):
        code, res = process_service.update_process(process_id, process_in)
        return make_resp(code, res, msg="Updated.")

    @app.output(EmptySchema)
    def delete(self, process_id):
        process_service.delete_process(process_id)


class Processes(MethodView):
    @app.input(ProcessIn)
    def post(self, process_in: dict):
        code, res = process_service.create_process(
            name=process_in["name"],
            start_params=process_in.get("start_params"),
            nodes=process_in["nodes"],
            desc=process_in.get("desc"),
            template=process_in.get("template"),
            developer_id=process_in.get("developer_id"),
            demander_id=process_in.get("demander_id"),
            group_id=process_in["group_id"],
        )
        return make_resp(code, res, msg="Created.")

    @app.output(EmptySchema)
    @app.input(IdsIn)
    def delete(self, ids_in):
        process_service.delete_processes(ids_in["ids"])

    @app.input(ProcessQuery, "query")
    @app.output(ProcessOut(many=True))
    def get(self, process_in):
        pagination = process_service.find_processes(process_in)
        return make_resp(pagination=pagination)


app.add_url_rule("/console/process/<process_id>", view_func=Process.as_view("process"))
app.add_url_rule("/console/processes", view_func=Processes.as_view("processes"))
