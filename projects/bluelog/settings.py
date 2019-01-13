import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret key')

    DEBUG_TB_INTERCEPT_REDIRECTS = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    CKEDITOR_ENABLE_CSRF = True
    CKEDITOR_FILE_UPLOADER = 'admin.upload_image'

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 25
    MAIL_USR_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('Bluelog Admin', MAIL_USERNAME)

    BLUELOG_EMAIL = os.getenv('BLUELOG_EMAIL')
    BLUELOG_POST_PER_PAGE = 10
    BLUELOG_MANAGE_POST_PER_PAGE = 15
    BLUELOG_COMMENT_PER_PAGE = 15
    # ('theme name', 'display name')
    BLUELOG_THEMES = {'perfect_blue': '忧郁蓝', 'black_swan': '夜间模式'}

    BLUELOG_UPLOAD_PATH = os.path.join(basedir, 'uploads')
    BLUELOG_ALLOWED_IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data-dev.sqlite3')

class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = prefix + ':memory:'

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix + os.path.join(basedir, 'data.sqlite3'))

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
