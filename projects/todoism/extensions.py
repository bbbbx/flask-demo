from flask import request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, current_user
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

@babel.localeselector
def get_localee():
    if current_user.is_authenticated and current_user.locale is not None:
        return current_user.locale
    
    locale = request.cookies.get('locale')
    if locale is not None:
        return locale
    # 根据请求头的 Accept-Language 字段来匹配
    # 若返回 None，则返回 BABEL_DEFAULT_LOCALE 配置
    return request.accept_language.best_match(current_app.config['TODOISM_LOCALE'])
