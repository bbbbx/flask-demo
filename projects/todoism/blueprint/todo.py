from flask import Blueprint, request, jsonify, render_template
from flask_login import current_user
from todoism.models import Item
from todoism.extensions import db

todo_bp = Blueprint('todo', __name__)

@todo_bp.route('/')
def index():
    pass


@todo_bp.route('/item/new', methods=['POST'])
def new_item():
    data = request.get_json()     # 获取并解析客户端发送的 JSON 数据
    if data is None or data['body'].strip() == '':
        jsonify(message='无效的 todo 正文。'), 400
    item = Item(body=data['body'], author=current_user._get_current_object())
    db.session.add(item)
    db.session.commit()
    return jsonify(html=render_template('_item.html', item=item), message='+1')


@todo_bp.route('/items/clear')
def clear_items():
    pass