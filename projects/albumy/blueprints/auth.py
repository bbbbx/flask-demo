from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required, login_user, logout_user
from albumy.forms.auth import RegisterForm, LoginForm, ForgetPasswordForm, ResetPasswordForm
from albumy.models import User
from albumy.extensions import db
from albumy.utils import generate_token, validate_token
from albumy.settings import Operations
from albumy.emails import send_confirm_account_email, send_reset_password_email

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        user = User(name=name, email=email, username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        token = generate_token(user=user, operation=Operations.CONFIRM)
        send_confirm_account_email(user=user, token=token)
        flash('确认邮件已发送，请查收收件箱。', 'info')
        return redirect(url_for('.login'))
    return render_template('auth/register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.validate_password(form.password.data):
            if login_user(user, form.remember_me.data):
                flash('登录成功。', 'info')
                return redirect_back()
            else:
                flash('你的账号被封了。', 'warning')
                return redirect(url_for('main.index'))
        flash('无效的邮箱或密码', 'warning')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('退出成功', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/forget-password', methods=['GET', 'POST'])
def forget_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = ForgetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            token = generate_token(user=user, operation=Operations.RESET_PASSWORD)
            send_reset_password_email(user=user, token=token)
            flash('重置密码邮件已发送，请查看收信箱。', 'info')
            return redirect(url_for('.login'))
        flash('无效的邮箱', 'warning')
        return redirect(url_for('.forget_password'))
    return render_template('auth/reset_password.html', form=form)

@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is None:
            flash('用户不存在！', 'warning')
            return redirect(url_for('main.index'))
        if validate_token(user=user, token=token, operation=Operations.RESET_PASSWORD,
                            new_password=form.password.data):  # 传入新密码
            flash('重置密码成功。', 'success')
            return redirect(url_for('.login'))
            
    return render_template('auth/reset_password.html', form=form)

@auth_bp.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))

    if validate_token(user=current_user, token=token, operation=Operations.CONFIRM):
        flash('账号已确认。', 'success')
        return redirect(url_for('main.index'))
    else:
        flash('无效或超时。', 'danger')
        return redirect(url_for('.resend_confirm_email'))

@auth_bp.route('/resend-confirm-email')
@login_required
def resend_confirm_email():
    if current_user.confirmed:
        return redirect(url_for('main.index'))

    token = generate_token(user=current_user, operation=Operations.CONFIRM)
    send_confirm_account_email(user=current_user, token=token)
    flash('新的确认邮件已发送，请查收你的收信箱。', 'info')
    return redirect(url_for('main.index'))
