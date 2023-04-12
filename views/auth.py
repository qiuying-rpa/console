"""
Auth View

By Allen Tao
Created at 2023/4/10 11:00
"""
import datetime

from flask import current_app as app
from apiflask.views import MethodView
from models.schemas.auth import TokenIn, RefreshTokenIn
from models.schemas.verification import VerificationIn
import services.auth as auth_services
from utils.common import get_conf


class Token(MethodView):

    @app.input(TokenIn)
    def post(self, token_in):
        code, res = auth_services.login(token_in['email'], token_in['password'])
        if code:
            return {'message': res, 'code': code}
        else:
            return {'data': {
                'access_token': res[0],
                'refresh_token': res[1]
            }}, 201

    @app.input(RefreshTokenIn)
    def put(self, refresh_token_in):
        code, res = auth_services.refresh(refresh_token_in['user_id'], refresh_token_in['refresh_token'])
        if code:
            return {'message': res, 'code': code}
        else:
            return {'data': {
                'access_token': res[0],
                'refresh_token': res[1]
            }}, 200


class Verification(MethodView):
    @app.input(VerificationIn)
    def post(self, verification_in):
        auth_services.send_verification_code(verification_in['email'])
        return {'message': 'done.'}, 201


app.add_url_rule('/auth/token', view_func=Token.as_view('token'))
app.add_url_rule('/auth/verify-code', view_func=Verification.as_view('verification'))
app.add_url_rule('/auth/pub-key', view_func=lambda: (
    {'data': get_conf().get('auth').get('rsa_public_key'), 'code': 0, 'message': 'Success',
     'time': datetime.datetime.now()}, 201))
