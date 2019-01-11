from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_debugtoolbar import DebugToolbarExtension

app = Flask('sayhello')
app.config.from_pyfile('settings.py')

# 模板环境对象
# http://jinja.pocoo.org/docs/latest/api/#jinja2.Environment
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
toolbar = DebugToolbarExtension(app)

# 因为需要将各个模块和程序实例关联起来，
# 所以需要在构造文件中导入这些模块。
# 因为这些模块也需要从构造文件中导入程序实例，
# 所以为了避免循环依赖，这些导入语句在构造文件的末尾定义。
from sayhello import views, errors, commands
