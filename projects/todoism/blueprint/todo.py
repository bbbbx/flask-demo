from flask import Blueprint

todo_bp = Blueprint('todo', __name__)

@todo_bp.route('/')
def index():
    pass


@todo_bp.route('/item')
def new_item():
    pass


@todo_bp.route('/items/clear')
def clear_items():
    pass