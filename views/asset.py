"""

By Ziqiu Li
Created at 2023/5/25 11:26
"""

import services.asset as asset_service
from apiflask.views import MethodView
from schemas.asset import AssetIn, AssetOut, AssetQuery
from schemas.common import IdsIn
from apiflask.schemas import EmptySchema
from utils.response import make_resp
from flask import current_app as app


class Asset(MethodView):
    @app.output(AssetOut)
    def get(self, asset_id):
        code, res = asset_service.find_asset(asset_id)
        return make_resp(code=code, res=res)

    @app.input(AssetIn)
    def patch(self, asset_id, asset_in):
        code, res = asset_service.update_asset(asset_id, asset_in)
        return make_resp(code=code, res=res, msg="Updated.")

    @app.output(EmptySchema)
    def delete(self, asset_id):
        asset_service.delete_asset(asset_id)


class Assets(MethodView):
    @app.input(AssetIn)
    def post(self, asset_in):
        code, res = asset_service.create_asset(
            name=asset_in["name"],
            asset_type=asset_in["type"],
            desc=asset_in.get("desc"),
            value=asset_in.get("value"),
        )
        return make_resp(code=code, res=res, msg="Created.")

    @app.input(AssetQuery, "query")
    @app.output(AssetOut(many=True))
    def get(self, asset_in):
        print(asset_in)
        pagination = asset_service.find_assets(asset_in)
        return make_resp(pagination=pagination)

    @app.input(IdsIn)
    @app.output(EmptySchema)
    def delete(self, ids_in):
        asset_service.delete_assets(ids_in)


app.add_url_rule("/console/asset/<asset_id>", view_func=Asset.as_view("asset"))
app.add_url_rule("/console/assets", view_func=Assets.as_view("assets"))
