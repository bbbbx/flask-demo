from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required
from bluelog.models import Post

admin_bp = Blueprint('admin', __name__)

# 如果一个蓝图的所有页面都需要
# 登录后才能访问，可以使用钩子小技巧
# @admin_bp.before_request
# @login_required
# def login_protect():
#     pass

@admin_bp.route('/post/', methods=['POST'])
def new_post():
    pass

@admin_bp.route('/settings')
@login_required
def settings():
    return render_template('admin/settings.html')

@admin_bp.route('/post/delete/<id>', methods=['POST'])
def delete_post(id):
    post = Post.query.get(id)
    post.delete()
    return redirect(url_for('index'))
