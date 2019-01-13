import os
from flask import Blueprint, render_template, redirect, url_for, current_app, request, flash, send_from_directory
from flask_login import login_required, current_user
from flask_ckeditor import upload_fail, upload_success
from bluelog.models import Post, Category, Comment
from bluelog.utils import redirect_back, allow_file
from bluelog.extensions import db
from bluelog.forms import PostForm, SettingsForm, CategoryForm

admin_bp = Blueprint('admin', __name__)

# 如果一个蓝图的所有页面都需要
# 登录后才能访问，可以使用钩子小技巧
# @admin_bp.before_request
# @login_required
# def login_protect():
#     pass

@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.blog_title = form.blog_title.data
        current_user.blog_subtitle = form.blog_subtitle.data
        current_user.about = form.about.data
        db.session.commit()
        flash('更新成功。', 'success')
        return redirect(url_for('blog.index'))
    form.name.data = current_user.name
    form.blog_title.data = current_user.blog_title
    form.blog_subtitle.data = current_user.blog_subtitle
    form.about.data = current_user.about
    return render_template('admin/settings.html', form=form)

@admin_bp.route('/post/delete/<post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('删除成功。', 'success')
    return redirect_back()

@admin_bp.route('/post/edit/<post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.category = Category.query.get(form.category.data)
        db.session.commit()
        flash('更新成功。', 'success')
        return redirect(url_for('blog.show_post', post_id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    form.category.data = post.category_id
    return render_template('admin/edit_post.html', form=form)

@admin_bp.route('/post/<post_id>/set_comment', methods=['POST'])
@login_required
def set_comment(post_id):
    post = Post.query.get_or_404(post_id)
    if post.can_comment:
        post.can_comment = False
        flash('关闭成功。', 'success')
    else:
        post.can_comment = True
        flash('开启成功。', 'success')
    db.session.commit()
    return redirect_back()

@admin_bp.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        category = Category.query.get(form.category.data)
        post = Post(title=title, body=body, category=category)
        # 等价于：
        # category_id = form.category.data
        # post = Post(title=title, body=body, category_id=category_id)
        db.session.add(post)
        db.session.commit()
        flash('新建成功。', 'success')
        return redirect(url_for('blog.show_post', post_id=post.id))
    return render_template('admin/new_post.html', form=form)

@admin_bp.route('/manage_post')
@login_required
def manage_post():
    post_page = request.args.get('page', 1, type=int)
    post_per_page = current_app.config['BLUELOG_MANAGE_POST_PER_PAGE']
    pagination = Post.query.paginate(page=post_page, per_page=post_per_page)
    posts = pagination.items
    return render_template('admin/manage_post.html', posts=posts, pagination=pagination, page=post_page)

@admin_bp.route('/category/manage')
@login_required
def manage_category():
    return render_template('admin/manage_category.html')

@admin_bp.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    form = CategoryForm()
    category = Category.query.get_or_404(category_id)
    if category.id == 1:
        flash('不能编辑默认分类。', 'warning')
        return redirect(url_for('blog.index'))
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash('更新成功。', 'success')
        return redirect(url_for('.manage_category'))
    form.name.data = category.name
    return render_template('admin/edit_category.html', form=form)

@admin_bp.route('/category/new', methods=['GET', 'POST'])
@login_required
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        flash('新建成功。', 'success')
        return redirect(url_for('.manage_category'))
    return render_template('admin/new_category.html', form=form)


@admin_bp.route('/category/<int:category_id>/delete', methods=['POST'])
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    if category.id == 1:
        flash('不能删除默认分类。', 'warning')
        return redirect(url_for('blog.index'))
    category.delete()
    flash('删除成功。', 'success')
    return redirect(url_for('.manage_category'))

@admin_bp.route('/comment/manage')
@login_required
def manage_comment():
    filter_rule = request.args.get('filter', 'all')   # 'all', 'reviewed', 'admin'
    comment_page = request.args.get('page', 1, type=int)
    comment_per_page = current_app.config['BLUELOG_MANAGE_POST_PER_PAGE']
    if filter_rule == 'unreviewed':
        filtered_comment = Comment.query.filter_by(reviewed=False)
    elif filter_rule == 'admin':
        filtered_comment = Comment.query.filter_by(from_admin=True)
    else:
        filtered_comment = Comment.query

    pagination = filtered_comment.order_by(Comment.timestamp.asc()).paginate(comment_page, per_page=comment_per_page)
    comments = pagination.items
    return render_template('admin/manage_comment.html', page=comment_page, comments=comments, pagination=pagination)

@admin_bp.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('评论已删除。', 'success')
    return redirect_back()

@admin_bp.route('/comment/<int:comment_id>/approve', methods=['POST'])
@login_required
def approve_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.reviewed = True
    db.session.commit()
    flash('评论已发布。', 'success')
    return redirect_back()

@admin_bp.route('/uploads/<path:filename>')
def get_image(filename):
    return send_from_directory(current_app.config['BLUELOG_UPLOAD_PATH'], filename=filename)

@admin_bp.route('/upload', methods=['POST'])
def upload_image():
    f = request.files.get('upload')
    if not allow_file(f.filename):
        return upload_fail('只允许上传 png、jpg、jpeg、gif 图片！')
    f.save(os.path.join(current_app.config['BLUELOG_UPLOAD_PATH'], f.filename))
    url = url_for('.get_image', filename=f.filename)
    return upload_success(url, f.filename)
