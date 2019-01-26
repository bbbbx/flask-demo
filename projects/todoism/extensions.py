from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_babel import Babel

db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
babel = Babel()

@login_manager.user_loader
def load_user(user_id):
    from todoism.models import User

    user = User.query.get(int(user_id))
    return user
