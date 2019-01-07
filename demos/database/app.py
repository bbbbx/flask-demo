import os
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
migrate = Migrate(app, db)

class Role(db.Model):
    __tablename__ = 'roles'

    # 其余的类变量都是该模型的属性，
    # 定义为 db.Column 类的实例。
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    # 一个角色可属于多个用户。
    # backrest 数向 User 模型中
    # 添加一个 role 属性，从而定义反向关系。
    # 通过 User 实例的这个属性可以获取对应的
    # Role 模型对象，而不用再通过 role_id 外键获取。
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)

    # 每个用户只能有一个角色
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

class NameForm(FlaskForm):
    name = StringField('你的名字？', validators=[DataRequired()])
    submit = SubmitField('提交')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    users = User.query.all()
    print(users)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:   # 如果用户不存在，则新建记录
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))

    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known'), users=users)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)
