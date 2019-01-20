from flask import Blueprint, render_template, jsonify
from flask_login import current_user
from albumy.models import User
from albumy.decorators import permission_required, confirm_required

ajax_bp = Blueprint('ajax', __name__)

@ajax_bp.route('/profile/<int:user_id>')
def get_profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('main/profile_popup.html', user=user)

@ajax_bp.route('/followers-count/<int:user_id>')
def followers_count(user_id):
    user = User.query.get_or_404(user_id)
    count = user.followers.count() - 1   # 减去自己
    return jsonify(count=count)

@ajax_bp.route('/follow/<username>', methods=['POST'])
def follow(username):
    if not current_user.is_authenticated:
        return jsonify(message='请先登录！'), 403
    if not current_user.confirmed:
        return jsonify(message='请先确认邮箱！'), 400
    if not current_user.can('FOLLOW'):
        return jsonify(message='没有权限！'), 403
    user = User.query.filter_by(username=username).first_or_404()
    if current_user.is_following(user):
        return jsonify(message='已经关注了。'), 400
    
    current_user.follow(user)
    return jsonify(message='关注成功。')

@ajax_bp.route('/unfollow/<username>', methods=['POST'])
def unfollow(username):
    if not current_user.is_authenticated:
        return jsonify(message='请先登录！'), 403

    user = User.query.filter_by(username=username).first_or_404()
    if not current_user.is_following(user):
        return jsonify(message='还没有关注。'), 400
    
    current_user.unfollow(user)
    return jsonify(message='取消关注成功。')
