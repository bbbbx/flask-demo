from faker import Faker
from flask import Blueprint, jsonify, render_template
from todoism.models import User, Item

auth_bp = Blueprint('auth', __name__)
fake = Faker()

@auth_bp.route('/login')
def login():
    return render_template('_login.html')

@auth_bp.route('/register')
def register():
    username = fake.user_name()

    # 确保生成的随机用户名不重复
    while User.query.filter_by(username=username).first() is not None:
        username = fake.user_name()

    password = fake.word()
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    # 添加几条 todo item
    item1 = Item(body='学习 Flask', author=user)
    item2 = Item(body='学习 Python', author=user)
    item3 = Item(body='学习 Redis、RabbitMQ', author=user)
    db.session.add_all([item1, item2, item3])
    db.session.commit()

    return jsonify(username=username, password=password, message='成功。')


@auth_bp.route('/logout')
def logout():
    pass
