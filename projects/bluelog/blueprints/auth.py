from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import login_user, logout_user, current_user, login_required
from bluelog.models import Admin
from bluelog.forms import LoginForm
from bluelog.utils import redirect_back

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remeber = form.remeber.data
        admin = Admin.query.first()
        if admin:
            if username == admin.username and admin.validate_password(password):
                login_user(admin, remeber)
                flash('欢迎回来。', 'info')
                return redirect_back()
            flash('无效的用户名或密码。', 'warning')
        else:
            flash('没有账号', 'warning')
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('退出成功。', 'info')
    return redirect_back()
