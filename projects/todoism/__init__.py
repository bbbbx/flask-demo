import os
from flask import Flask
from todoism.extensions import db, csrf, login_manager, babel
from todoism.setttings import config
from todoism.blueprint.home import home_bp
from todoism.blueprint.auth import auth_bp
from todoism.blueprint.todo import todo_bp

def register_extensions(app):
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    babel.init_app(app)

def register_blueprint(app):
    app.register_blueprint(home_bp, prefix='/')
    app.register_blueprint(auth_bp, prefix='/auth')
    app.register_blueprint(todo_bp, prefix='/todo')


def create_app(config_name):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprint(app)

    return app
