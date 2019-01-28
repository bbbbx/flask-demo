from flask import request, jsonify
from flask.views import MethodView
from todoism.apis.v1 import api_v1
from todoism.models import User
from todoism.apis.v1.errors import api_abort

class AuthTokenAPI(MethodView):

    def post(self):
        grant_type = request.form.get('grant_type')
        username = request.form.get('username')
        password = request.form.get('password')

        if grant_type is None or grant_type.lower() != 'password':
            return api_abort(code=400, message='The grant type must be password.')
        user = User.query.filter_by(username=username).first()
        if user is None or not user.valiedate_password(password):
            return api_abort(code=400, message='用户名或密码不正确。')
        
        token, expiration = generate_token(user)

        response = jsonify({
            'access_token': token,
            'token_type': 'Bearer',
            'expires_in': expiration
        })
        response.headers['Cache-Control'] = 'no-cache'
        response.headers['Pragma'] = 'no-cache'
        return response


api_v1.add_url_rule('/oauth/token', view_func=AuthTokenAPI.as_view('token'), methods=['POST'])
