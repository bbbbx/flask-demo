import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, send_from_directory, abort
from flask_login import login_required, current_user
from flask_dropzone import random_filename
from albumy.decorators import confirm_required, permission_required
from albumy.models import Photo, Tag
from albumy.extensions import db
from albumy.utils import resize_image, flash_errors
from albumy.forms.main import DescriptionForm, TagForm

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('main/index.html')


@main_bp.route('/explore')
def explore():
    return render_template('main/explore.html')

@main_bp.route('/upload', methods=['GET', 'POST'])
@login_required    # 验证登录状态
@confirm_required  # 验证确认邮箱状态
@permission_required('UPLOAD')  # 验证权限
def upload():
    if request.method == 'POST' and 'file' in request.files:
        f = request.files.get('file')  # 获取文件对象

        # Dropzone.js 是通过 Ajax 发送请求的，
        # 每个文件一个请求。为此，无法返回重定向响应，
        # 使用 flash() 函数或是操作 session。
        # 假设我们使用一个 check_image() 函数来检查文件的有效性：
        # if not check_image(f):
        #     return '无效的图片', 400
        # 客户端会把接收到的错误响应显示出来。

        filename = random_filename(f.filename)  # 生成随机文件名
        f.save(os.path.join(current_app.config['ALBUMY_UPLOAD_PATH'], filename)) # 保存文件
        filename_s = resize_image(f, filename, 400)
        filename_m = resize_image(f, filename, 800)

        photo = Photo(  # 创建图片记录
            filename=filename,
            filename_s=filename_s,
            filename_m=filename_m,
            author=current_user._get_current_object()  # 获取真实的用户对象，而不是代理的用户对象
        )
        db.session.add(photo)
        db.session.commit()
    return render_template('main/upload.html')

@main_bp.route('/avatar/<path:filename>')
def get_avatar(filename):
    return send_from_directory(current_app.config['AVATARS_SAVE_PATH'], filename)

@main_bp.route('/uploads/<path:filename>')
def get_image(filename):
    return send_from_directory(current_app.config['ALBUMY_UPLOAD_PATH'], filename)

@main_bp.route('/photo/<photo_id>')
def show_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    description_form = DescriptionForm()
    description_form.description.data = photo.description
    tag_form = TagForm()
    
    return render_template('main/photo.html', photo=photo, description_form=description_form, tag_form=tag_form)

@main_bp.route('/photo/<int:photo_id>/description', methods=['POST'])
@confirm_required
@login_required
def edit_description(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    if current_user != photo.author:
        abort(403)
    
    form = DescriptionForm()
    if form.validate_on_submit():
        photo.description = form.description.data
        db.session.commit()
        flash('修改成功。', 'success')
    
    flash_errors(form)
    return redirect(url_for('.show_photo', photo_id=photo_id))


@main_bp.route('/photo/<int:photo_id>/tag/new', methods=['POST'])
@confirm_required
@login_required
def new_tag(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    if current_user != photo.author:
        abort(403)
    
    form = TagForm()
    if form.validate_on_submit():
        for name in form.tag.data.split():
            tag = Tag.query.filter_by(name=name).first()
            if tag is None:  # 如果没有该标签则新建一个
                tag = Tag(name=name)
                db.session.add(tag)
                db.session.commit()
            if tag not in photo.tags:  # 如果还没有建立联系，则新建联系
                photo.tags.append(tag)
                db.session.commit()
        flash('添加标签成功。', 'success')
    
    flash_errors(form)
    return redirect(url_for('.show_photo', photo_id=photo_id))

@main_bp.route('/photo/<int:photo_id>/tag/<int:tag_id>', methods=['POST'])
@login_required
def delete_tag(photo_id, tag_id):
    tag = Tag.query.get_or_404(tag_id)
    photo = Photo.query.get_or_404(photo_id)
    if current_user != photo.author:
        abort(403)
    photo.tags.remove(tag)
    db.session.commit()

    if not tag.photos:  # 如果已经没有图片与该标签有联系，则删除该标签
        db.session.delete(tag)
        db.session.commit()
    
    flash('删除成功。', 'success')
    return redirect(url_for('.show_photo', photo_id=photo_id))

@main_bp.route('/tag/<int:tag_id>', defaults={ 'order': 'by_time' })
@main_bp.route('/tag/<int:tag_id>/<order>')
def show_tag(tag_id, order):
    '''这个视图函数注册了两个路由，第一个用来决定排序方式的 order 变量设默认值。'''
    tag = Tag.query.get_or_404(tag_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ALBUMY_PHOTO_PER_PAGE']
    order_rule = '时间'
    pagination = Photo.query.with_parent(tag).order_by(Photo.timestamp.desc()).paginate(page, per_page)
    photos = pagination.items

    # if order == 'by_collects':
    #     photos.sort(key=lambda photo: len(photo.collectors), reverse=True)
    #     order_rule = '收藏数'
    return render_template('main/tag.html', tag=tag, pagination=pagination, photos=photos, order_rule=order_rule)


@main_bp.route('/photo/n/<int:photo_id>')
def photo_next(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    photo_n = Photo.query.with_parent(photo.author).filter(Photo.id < photo_id).order_by(Photo.timestamp.desc()).first()

    if photo_n is None:
        flash('已经是最后的一张照片了。', 'info')
        return redirect(url_for('.show_photo', photo_id=photo_id))
    return redirect(url_for('.show_photo', photo_id=photo_n.id))    # 注意这里和上一行是不一样的

@main_bp.route('/photo/p/<int:photo_id>')
def photo_previous(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    photo_p = Photo.query.with_parent(photo.author).filter(Photo.id > photo_id).order_by(Photo.timestamp.asc()).first()

    if photo_p is None:
        flash('已经是最后的一张照片了。', 'info')
        return redirect(url_for('.show_photo', photo_id=photo_id))
    return redirect(url_for('.show_photo', photo_id=photo_p.id))    # 注意这里和上一行是不一样的

@main_bp.route('/photo/<int:photo_id>/delete', methods=['POST'])
@confirm_required
@login_required
def delete_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    if current_user != photo.author:
        abort(403)

    db.session.delete(photo)
    db.session.commit()
    flash('删除成功', 'info')

    photo_n = Photo.query.with_parent(photo.author).filter(Photo.id < photo_id).order_by(Photo.id.desc()).first()
    if photo_n is None:  # 没有下一张照片时获取上一张
        photo_p = Photo.query.with_parent(photo.author).filter(Photo.id > photo_id).order_by(Photo.id.asc()).first()
        if photo_p is None:  # 上一张也没有时则返回主页
            return redirect(url_for('main.index', username=photo.author.username))
        return redirect(url_for('.show_photo', photo_id=photo_p.id))
    return redirect(url_for('.show_photo', photo_id=photo_n.id))

@main_bp.route('/photo/<int:photo_id>/report', methods=['POST'])
@confirm_required
@login_required
def report_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    photo.flag += 1
    db.session.commit()
    flash('举报成功', 'success')
    return redirect(url_for('.show_photo', photo_id=photo_id))
