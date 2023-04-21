"""
Auth View

By Allen Tao
Created at 2023/4/10 11:00
"""
from functools import reduce
from flask import current_app as app, g
from apiflask.views import MethodView
from models.schemas.auth import TokenIn, RefreshTokenIn, TokenOut, PermissionsOut
from models.schemas.common import NoneDataOut
from models.schemas.verification import VerificationIn
import services.auth as auth_service
import services.user as user_service


class Token(MethodView):
    @app.input(TokenIn)
    @app.output(TokenOut(partial=True))
    def post(self, token_in):
        code, res = auth_service.login(token_in["email"], token_in["password"])
        if code:
            return {"message": res, "code": code, "data": None}
        else:
            return {"data": {"access_token": res[0], "refresh_token": res[1]}}, 201

    @app.input(RefreshTokenIn)
    @app.output(TokenOut(partial=True))
    def put(self, refresh_token_in):
        code, res = auth_service.refresh(refresh_token_in["refresh_token"])
        if code:
            return {"message": res, "code": code, "data": None}
        else:
            return {"data": {"access_token": res[0], "refresh_token": res[1]}}, 200


class Verification(MethodView):
    @app.input(VerificationIn)
    @app.output(NoneDataOut)
    def post(self, verification_in):
        auth_service.send_verification_code(verification_in["email"])
        return {"message": "done."}, 201


class Permissions(MethodView):
    @app.output(PermissionsOut)
    def get(self):
        user_id = g.current_user["id"]
        user = user_service.find_user(user_id)

        data = {"menus": [], "actions": []}
        if user.is_admin:
            data["menus"] = "*"
            data["actions"] = "*"
        else:
            data = reduce(
                lambda pre, curr: not pre["menus"].append(curr["menus"])
                and not pre["actions"].append(curr["actions"])
                and pre,
                user.roles,
                data,
            )
        return {"data": data}


app.add_url_rule("/auth/token", view_func=Token.as_view("token"))
app.add_url_rule("/auth/verify-code", view_func=Verification.as_view("verify_code"))
app.add_url_rule("/auth/permissions", view_func=Permissions.as_view("permissions"))
