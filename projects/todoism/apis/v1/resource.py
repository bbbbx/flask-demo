from flask import jsonify
from flask.views import MethodView
from todoism.apis.v1 import api_v1

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
        pass


    def put(self, item_id):
        pass


    def patch(self, item_id):
        pass


    def delete(self, item_id):
        pass


api_v1.add_url_rule('/', view_func=IndexAPI.as_view('index'), methods=['GET'])
