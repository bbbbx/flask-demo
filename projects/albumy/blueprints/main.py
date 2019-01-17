import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from flask_dropzone import random_filename
from albumy.decorators import confirm_required, permission_required
from albumy.models import Photo
from albumy.extensions import db
from albumy.utils import resize_image

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
@permission_required('UOLOAD')  # 验证权限
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
