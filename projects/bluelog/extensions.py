'''使用工厂函数创建程序实例时，
并没有一个创建好的程序实例可以传入。
如果我们把实例化 flask 扩展的操作放到工厂函数中，
那么我们就没有一个全局的 flask 扩展对象可以使用，
比如表示数据库的 db 对象。为了解决这个问题，
大多数扩展都提供了一个 init_app() 方法来支持分离
flask 扩展的实例化和初始化操作。
'''
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_ckeditor import CKEditor
from flask_moment import Moment
from flask_login import LoginManager

# 实例化
bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
moment = Moment()
ckeditor = CKEditor()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    from bluelog.models import Admin
    user = Admin.query.get(user_id)
    return user
