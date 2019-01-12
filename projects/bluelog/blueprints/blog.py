from flask import Blueprint, render_template, request, current_app
from bluelog.models import Post, Comment

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
    return render_template('blog/category.html')

@blog_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    comment_page = request.args.get('page', 1, type=int)
    comment_per_page = current_app.config['BLUELOG_COMMENT_PER_PAGE']
    pagination = Comment.query.with_parent(post).filter_by(reviewed=True).order_by(Comment.timestamp.asc()).paginate(
        page=comment_page, per_page=comment_per_page)
    comments = pagination.items
    print(comments)
    return render_template('blog/post.html', post=post, pagination=pagination, comments=comments)

@blog_bp.route('/comment')
def reply_comment():
    return 'hello'
