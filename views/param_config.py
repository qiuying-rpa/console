"""

By Ziqiu Li
Created at 2023/5/25 14:20
"""
"""
By Ziqiu Li
Created at 2023/5/11 17:07
"""
from flask import current_app as app
from apiflask.views import MethodView
from schemas.param_config import ParamConfigIn, ParamConfigOut
from schemas.common import IdsIn
from apiflask.schemas import EmptySchema
import services.param_config as param_config_service
from utils.response import make_resp


class ParamConfig(MethodView):
    @app.output(ParamConfigOut)
    def get(self, param_config_id):
        code, res = param_config_service.find_param_config(param_config_id)
        return make_resp(code, res)

    @app.input(ParamConfigIn)
    def post(self, param_config_in):
        code, res = param_config_service.create_param_config(
            name=param_config_in["name"],
            params=param_config_in["params"],
            desc=param_config_in.get("desc"),
            process_id=param_config_in["process_id"],
        )
        return make_resp(code, res, msg="Created.")

    @app.input(ParamConfigIn)
    def patch(self, param_config_id, param_config_in):
        code, res = param_config_service.update_param_config(
            param_config_id, param_config_in
        )
        return make_resp(code, res, msg="Updated.")


class ParamConfigs(MethodView):
    @app.output(EmptySchema)
    @app.input(IdsIn)
    def delete(self, ids_in):
        param_config_service.delete_many_param_config(ids_in["ids"])

    @app.input(ParamConfigIn, "query")
    @app.output(ParamConfigOut(many=True))
    def get(self, param_config_in):
        if param_config_in:
            param_configs = param_config_service.find_param_configs_by(param_config_in)
        else:
            param_configs = param_config_service.list_all_param_config()
        return make_resp(res=param_configs)


app.add_url_rule(
    "/console/paramConfig/<param_config_id>",
    view_func=ParamConfig.as_view("paramConfig"),
)
app.add_url_rule(
    "/console/paramConfig", view_func=ParamConfig.as_view("createParamConfig")
)
app.add_url_rule(
    "/console/paramConfigs", view_func=ParamConfigs.as_view("paramConfigs")
)
