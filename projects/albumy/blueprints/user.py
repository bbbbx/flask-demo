from flask import Blueprint, request, render_template, current_app, flash, redirect, url_for
from flask_login import login_required, current_user, fresh_login_required
from albumy.models import User, Photo, Collect
from albumy.decorators import confirm_required, permission_required
from albumy.utils import redirect_back, flash_errors
from albumy.notifications import push_follow_notification
from albumy.forms.user import UploadAvatarForm, CropAvatarForm, ChangePasswordForm, EditProfileForm
from albumy.extensions import db, avatars

user_bp = Blueprint('user', __name__)

@user_bp.route('/<username>')
def index(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ALBUMY_PHOTO_PER_PAGE']
    pagination = Photo.query.with_parent(user).order_by(Photo.timestamp.desc()).paginate(page, per_page)
    photos = pagination.items
    return render_template('user/index.html', photos=photos, pagination=pagination, user=user)
    
@user_bp.route('/<username>/collections')
def show_collections(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ALBUMY_COMMENT_PER_PAGE']
    pagination = Collect.query.with_parent(user).order_by(Collect.timestamp.desc()).paginate(page, per_page)
    collects = pagination.items
    return render_template('user/collections.html', user=user, pagination=pagination, collects=collects)

@user_bp.route('/follow/<username>', methods=['POST'])
@login_required
@confirm_required
@permission_required('FOLLOW')
def follow(username):
    user = User.query.filter_by(username=username).first_or_404()
    if current_user.is_following(user):
        flash('已经关注过了。', 'info')
        return redirect(url_for('.index', username=username))
    
    current_user.follow(user)
    flash('关注成功。', 'success')
    push_follow_notification(follower=current_user, receiver=user)
    return redirect_back()

@user_bp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first_or_404()
    if not current_user.is_following(user):
        flash('还没有关注。', 'info')
        return redirect(url_for('.index', username=username))
    
    current_user.unfollow(user)
    flash('取消关注成功。', 'success')
    return redirect_back()

@user_bp.route('/<username>/followers')
def show_followers(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ALBUMY_COMMENT_PER_PAGE']
    pagination = user.followers.paginate(page, per_page)
    follows = pagination.items
    return render_template('user/followers.html', user=user, pagination=pagination, follows=follows)

@user_bp.route('/<username>/following')
def show_following(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ALBUMY_COMMENT_PER_PAGE']
    pagination = user.following.paginate(page, per_page)
    follows = pagination.items
    return render_template('user/following.html', user=user, pagination=pagination, follows=follows)

@user_bp.route('/settings/profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.username = form.username.data
        current_user.website = form.website.data
        current_user.location = form.location.data
        current_user.bio = form.bio.data
        db.session.commit()
        flash('修改成功。', 'success')
        return redirect(url_for('user.edit_profile'))

    form.name.data = current_user.name
    form.username.data = current_user.username
    form.bio.data = current_user.bio
    form.website.data = current_user.website
    form.location.data = current_user.location
    return render_template('user/settings/edit_profile.html', form=form)

@user_bp.route('/settings/avatar')
@login_required
@confirm_required
def change_avatar():
    upload_form = UploadAvatarForm()
    crop_form = CropAvatarForm()
    return render_template('user/settings/change_avatar.html', upload_form=upload_form, crop_form=crop_form)

@user_bp.route('/settings/avatar/upload', methods=['POST'])
@login_required
@confirm_required
def upload_avatar():
    form = UploadAvatarForm()
    if form.validate_on_submit():
        image = form.image.data
        filename = avatars.save_avatar(image)   # 保存头像，并取得文件名
        current_user.avatar_raw = filename
        db.session.commit()
        flash('文件已上传。', 'info')
    flash_errors(form)
    return redirect(url_for('.change_avatar'))
    

@user_bp.route('/settings/avatar/crop', methods=['POST'])
@login_required
@confirm_required
def crop_avatar():
    form = CropAvatarForm()
    if form.validate_on_submit():
        x = form.x.data
        y = form.y.data
        h = form.h.data
        w = form.w.data
        # 裁剪头像并保存，返回三个尺寸头像的文件名
        filename = avatars.crop_avatar(current_user.avatar_raw, x, y, w, h)
        current_user.avatar_s = filename[0]
        current_user.avatar_m = filename[1]
        current_user.avatar_l = filename[2]
        db.session.commit()
        flash('头像已更新。', 'success')
    flash_errors(form)
    return redirect(url_for('.change_avatar'))


@user_bp.route('/settings/password', methods=['GET', 'POST'])
@fresh_login_required     # 确保用户处于 “活跃” 的认证状态
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.validate_password(form.old_password.data):
            current_user.set_password(form.new_password.data)   # 重设密码
            db.session.commit()
            flash('密码修改成功。', 'success')
            return redirect(url_for('.index', username=current_user.username))
        else:
            flash('密码不正确！', 'warning')
    return render_template('user/settings/change_password.html', form=form)


@user_bp.route('/settings/email')
def change_email_request():
    pass

@user_bp.route('/settings/notification-setting')
def notification_setting():
    return render_template('user/settings/edit_notification.html')

@user_bp.route('/settings/account')
def delete_account():
    return render_template('user/settings/delete_account.html')
