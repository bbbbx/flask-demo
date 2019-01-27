from flask import Blueprint
from flask_cors import CORS

api_v1 = Blueprint('api_v1', __name__)
CORS(api_v1)   # 使 API 支持跨域请求

# 为了避免产生循环导入，我们在脚本末尾导入 resource 模块，
# 以便让蓝本和对应的视图函数关联起来。
from todoism.apis.v1 import resource
