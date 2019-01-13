import os
import click
from flask import Flask, render_template
from bluelog.blueprints import auth, blog, admin
from bluelog.settings import config
from bluelog.extensions import bootstrap, db, mail, moment, ckeditor, login_manager
from bluelog.models import Admin, Category

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('bluelog')
    app.config.from_object(config[config_name])

    register_logging(app)
    register_extensions(app)
    register_blueprints(app)
    register_shell_context(app)
    register_template_context(app)
    register_errors(app)
    register_commands(app)

    return app

def register_logging(app):
    pass

def register_extensions(app):
    bootstrap.init_app(app)    
    db.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    ckeditor.init_app(app)
    login_manager.init_app(app)

def register_blueprints(app):
    app.register_blueprint(blog.blog_bp)
    app.register_blueprint(auth.auth_bp, url_prefix='/auth')
    app.register_blueprint(admin.admin_bp, url_prefix='/admin')

def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)

def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()
        return dict(admin=admin, categories=categories)


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('errors/500.html'), 500

def register_commands(app):
    @app.cli.command()
    @click.option('--category', default=10, help='Quantity of categories, default is 10.')
    @click.option('--post', default=50, help='Quantity of posts, default is 50.')
    @click.option('--comment', default=500, help='Quantity of comments, default is 500.')
    def forge(category, post, comment):
        """Generate fake data."""
        from bluelog.fakes import fake_admin, fake_categories, fake_posts, fake_comments

        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator...')
        fake_admin()

        click.echo('Generating %d categories...' % category)
        fake_categories(category)

        click.echo('Generating %d posts...' % post)
        fake_posts(post)

        click.echo('Generating %d comment...' % comment)
        fake_comments(comment)

        click.echo('Done.')

    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--password', prompt=True, help='The password used to login.', hide_input=True, confirmation_prompt=True)
    def init(username, password):
        """Building Bluelog, just for you."""

        click.echo('Initializing the database...')
        db.create_all()

        admin = Admin.query.first()
        if admin:
            click.echo('The administrator already exists, updating...')
            admin.username = username
            admin.set_password(password)
        else:
            click.echo('Creating the temporary administrator account...')
            admin = Admin(
                username=username,
                blog_title='Bluelog',
                blog_subtitle='Subtitle here...',
                name='Admin',
                about='Anything about you.'
            )
            admin.set_password(password)
            db.session.add(admin)

        category = Category.query.first()
        if category is None:
            click.echo('Creating the default category...')
            category = Category(name='Default')
            db.session.add(category)

        db.session.commit()
        click.echo('Done.')
    
