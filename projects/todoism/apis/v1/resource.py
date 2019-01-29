from flask import jsonify, g, request
from flask.views import MethodView
from todoism.apis.v1 import api_v1
from todoism.models import Item, User
from todoism.apis.v1.errors import api_abort
from todoism.apis.v1.auth import generate_token, auth_required

class IndexAPI(MethodView):
    def get(self):
        base_url = "http://api.todoism.com:5000/v1"
        return jsonify({
            "api_version": "1.0",
            "api_base_url": base_url,
            "current_user_url": base_url + "/user",
            "authentication_url": base_url + "/oauth/token",
            "item_url": base_url + "/items/{item_id}",
            "current_user_items_url": base_url + "/user/items{?page,per_page}",
            "current_user_active_items_url": base_url + "/user/items/active{?page,per_page}",
            "current_user_completed_items_url": base_url + "/user/items/completed{?page,per_page}",
        })


class UserApi(MethodView):

    def get(self, user_id):
        return jsonify(user_id=user_id)


class ItemAPI(MethodView):
    # Flask 在 MethodView 类中提供了 decorators 属性，
    # 使用它可以为整个资源类的所有视图方法附加装饰器。
    decorators = [auth_required]

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
api_v1.add_url_rule('/user/<int:user_id>', view_func=UserApi.as_view('user'), methods=['GET', 'PUT', 'PATCH', 'DELETE'])
api_v1.add_url_rule('/items/<int:item_id>', view_func=ItemAPI.as_view('item'), methods=['GET', 'PUT', 'PATCH', 'DELETE'])
api_v1.add_url_rule('/oauth/token', view_func=AuthTokenAPI.as_view('token'), methods=['POST'])
