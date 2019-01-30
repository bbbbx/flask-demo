import os
import logging
from logging.handlers import RotatingFileHandler
import click
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

def register_command(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')


def register_logger(app):
    app.logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler('logs/todoism.log', maxBytes=10*1024*1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    if not app.debug:
        app.logger.addHandler(file_handler)


def create_app(config_name):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    register_logger(app)
    register_extensions(app)
    register_blueprint(app)
    register_command(app)

    return app
