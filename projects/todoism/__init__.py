import os
from flask import Flask
from todoism.extensions import db, csrf, login_manager, babel
from todoism.setttings import config
from todoism.blueprint.home import home_bp
from todoism.blueprint.auth import auth_bp
from todoism.blueprint.todo import todo_bp
from todoism.apis.v1 import api_v1

def register_extensions(app):
    db.init_app(app)
    csrf.init_app(app)
    csrf.exempt(api_v1)   # 取消 API 蓝图的 CSRF 保护
    login_manager.init_app(app)
    babel.init_app(app)

def register_blueprint(app):
    app.register_blueprint(home_bp, url_prefix='/')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(todo_bp, url_prefix='/todo')
    app.register_blueprint(api_v1, subdomain='api', url_prefix='/v1')


def create_app(config_name):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprint(app)

    return app
