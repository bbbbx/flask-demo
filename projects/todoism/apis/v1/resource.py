from flask import jsonify, g, request
from flask.views import MethodView
from todoism.apis.v1 import api_v1
from todoism.models import Item, User
from todoism.apis.v1.errors import api_abort
from todoism.apis.v1.auth import generate_token

class IndexAPI(MethodView):
    def get(self):
        return jsonify({
            "api_version": "1.0",
            "api_base_url": "http://example.com/api/v1",
            "current_user_url": "http://example.com/api/v1/user",
            "authentication_url": "http://example.com/api/v1/token",
            "item_url": "http://example.com/api/v1/items/{item_id}",
            "current_user_items_url": "http://example.com/api/v1/user/items{?page,per_page}",
            "current_user_active_items_url": "http://example.com/api/v1/user/items/active{?page,per_page}",
            "current_user_completed_items_url": "http://example.com/api/v1/user/items/completed{?page,per_page}",
        })


class ItemAPI(MethodView):
    # decorators = [auth_required]

    def get(self, item_id):
        return jsonify(item_id=item_id)


    def put(self, item_id):
        pass


    def patch(self, item_id):
        pass


    def delete(self, item_id):
        pass


class AuthTokenAPI(MethodView):

    def post(self):
        grant_type = request.form.get('grant_type')
        username = request.form.get('username')
        password = request.form.get('password')

        if grant_type is None or grant_type.lower() != 'password':
            return api_abort(code=400, message='The grant type must be password.')
        user = User.query.filter_by(username=username).first()
        if user is None or not user.validate_password(password):
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


api_v1.add_url_rule('/', view_func=IndexAPI.as_view('index'), methods=['GET'])
api_v1.add_url_rule('/items/<int:item_id>', view_func=ItemAPI.as_view('item'), methods=['GET', 'PUT', 'PATCH', 'DELETE'])
api_v1.add_url_rule('/oauth/token', view_func=AuthTokenAPI.as_view('token'), methods=['POST'])
