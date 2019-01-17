from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import AnonymousUserMixin, LoginManager
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from flask_dropzone import Dropzone

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
bootstrap = Bootstrap()
moment = Moment()
csrf = CSRFProtect()
dropzone = Dropzone()

@login_manager.user_loader
def load_user(user_id):
    from albumy.models import User
    user = User.query.get(int(user_id))
    return user

login_manager.login_view = 'auth.login'
# login_manager.login_manager = 'Your custom message'
login_manager.login_message_category = 'warning'

class Guest(AnonymousUserMixin):
    @property
    def is_admin(self):
        return False

    def can(self, permission_name):
        return False

login_manager.anonymous_user = Guest
