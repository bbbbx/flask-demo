from flask import Blueprint, flash, redirect, render_template, url_for
from albumy.decorators import permission_required
from albumy.models import User
from albumy.utils import redirect_back

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/lock/user/<int:user_id>', methods=['POST'])
@permission_required('MODERATE')
def lock_user(user_id):
    user = User.query.get_or_404(user_id)
    user.lock()
    flash('已锁住账号。', 'success')
    return redirect_back()

@admin_bp.route('/unlock/user/<int:user_id>', methods=['POST'])
@permission_required('MODERATE')
def unlock_user(user_id):
    user = User.query.get_or_404(user_id)
    user.unlock()
    flash('已对账号解锁。', 'success')
    return redirect_back()
