from flask import Blueprint, render_template, request, current_app, url_for, redirect, make_response, flash
from flask_login import current_user
from bluelog.models import Post, Comment, Category
from bluelog.forms import AdminCommentForm, CommentForm
from bluelog.emails import send_new_comment_email, send_new_reply_email
from bluelog.utils import redirect_back
from bluelog.extensions import db

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)  # 从 query string 中获取当前页数
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)  # 分页对象
    posts = pagination.items    # 当前页面的 record 列表
    return render_template('blog/index.html', pagination=pagination, posts=posts)

@blog_bp.route('/about')
def about():
    return render_template('blog/about.html')

@blog_bp.route('/category/<int:category_id>')
def show_category(category_id):
    category = Category.query.get_or_404(category_id)
    category_page = request.args.get('page', 1, type=int)
    categoryt_per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    pagination = Post.query.with_parent(category).order_by(Post.timestamp.desc()).paginate(
        page=category_page, per_page=categoryt_per_page)
    posts = pagination.items
    return render_template('blog/category.html', posts=posts, category=category, pagination=pagination)

@blog_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    comment_page = request.args.get('page', 1, type=int)
    comment_per_page = current_app.config['BLUELOG_COMMENT_PER_PAGE']
    pagination = Comment.query.with_parent(post).filter_by(reviewed=True).order_by(Comment.timestamp.desc()).paginate(
        page=comment_page, per_page=comment_per_page)
    comments = pagination.items

    if current_user.is_authenticated:  # 已登录则使用管理员表单
        form = AdminCommentForm() 
        form.author.data = current_user.name
        form.email.data = current_app.config['BLUELOG_EMAIL']
        form.site.data = url_for('.index')
        from_admin = True
        reviewed = True
    else:   # 未登录则使用普通表单
        form = CommentForm()
        from_admin = False
        reviewed = False

    if form.validate_on_submit():
        author = form.author.data
        email = form.email.data
        site = form.site.data
        body = form.body.data
        comment = Comment(
            author=author, email=email, site=site, body=body,
            from_admin=from_admin, post=post, reviewed=reviewed
        )
        db.session.add(comment)
        db.session.commit()
        if current_user.is_authenticated:  # 根据登录状态显示不同的提示信息
            flash('评论已发布。', 'success')
        else:
            flash('感谢你的评论，审核通过后将会显示。', 'info')
            send_new_comment_email(post)

        replied_id = request.args.get('reply')
        if replied_id:
            replied_comment = Comment.query.get_or_404(replied_id)
            comment.replied = reply_comment
            send_new_reply_email(reply_comment)   # 发送邮件给被恢复的用户
        return redirect(url_for('.show_post', post_id=post_id))
    return render_template('blog/post.html', post=post, pagination=pagination, comments=comments, form=form)

@blog_bp.route('/reply/comment/<int:comment_id>')
def reply_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    return redirect(url_for('.show_post', post_id=comment.post_id, reply=comment_id, author=comment.author) + '#comment-form')

@blog_bp.route('/change-theme/<theme_name>')
def change_theme(theme_name):
    if theme_name not in current_app.config['BLUELOG_THEMES'].keys():
        about(404)

    response = make_response(redirect_back())
    response.set_cookie('theme', theme_name, max_age=30*24*60*60)
    return response
