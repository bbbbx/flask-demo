import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('Todoism', MAIL_USERNAME)

    SQLALCHEMY_TRACK_MODIFICATIONS = True

    TODOISM_LOCALES = ['en_US', 'zh_Hans_CN']
    BABEL_DEFAULT_LOCALE = TODOISM_LOCALES[0]

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'todoism-data-dev.sqlite3')
    # 使用 MySQL，需要 `pipenv install cymysql`
    # SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://username:password@localhost:3306/albumy'

    SERVER_NAME = 'todoism.com:5000'  # 坑点：Chrome 会强制将 *.dev 的域名改为 HTTPS 访问


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = prefix + ':memory:'


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix + os.path.join(basedir, 'todoism-data.sqlite3'))

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
