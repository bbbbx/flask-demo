from faker import Faker
from sqlalchemy.exc import IntegrityError
from albumy.extensions import db
from albumy.models import User

fake = Faker('zh-CN')

def fake_admin():
    admin = User(name='Venus Shell',
                 username='venus',
                 email='venus@venusworld.cn',
                 bio=fake.sentence(),
                 website='http://venusworld.cn',
                 confirmed=True)
    admin.set_password('123123')
    db.session.add(admin)
    db.session.commit()


def fake_user(count=10):
    for i in range(count):
        user = User(name=fake.name(),
                    confirmed=True,
                    username=fake.user_name(),
                    bio=fake.sentence(),
                    location=fake.city(),
                    website=fake.url(),
                    member_since=fake.date_this_decade(),
                    email=fake.email())
        user.set_password('123456')
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

