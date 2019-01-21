import os
from datetime import datetime
from flask_login import UserMixin
from flask_avatars import Identicon
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from albumy.extensions import db

# 每个角色可以拥有多个权限，权限可以被多个角色所拥有
roles_permissions = db.Table(
    'roles_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'))
)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    users = db.relationship('User', back_populates='role')
    permissions = db.relationship('Permission', secondary=roles_permissions, back_populates='roles')

    @staticmethod
    def init_role():
        # 角色与权限的对应关系
        roles_permissions_map = {
            'Locked': ['FOLLOW', 'COLLECT'],
            'User': ['FOLLOW', 'COLLECT', 'COMMENT', 'UPLOAD'],
            'Moderator': ['FOLLOW', 'COLLECT', 'COMMENT', 'UPLOAD', 'MODERATE'],
            'Administrator': ['FOLLOW', 'COLLECT', 'COMMENT', 'UPLOAD', 'MODERATE', 'ADMINISTER']
        }

        for role_name in roles_permissions_map:
            role = Role.query.filter_by(name=role_name).first()
            if role is None:
                role = Role(name=role_name)
                db.session.add(role)
            role.permissions = []
            for permission_name in roles_permissions_map[role_name]:
                permission = Permission.query.filter_by(name=permission_name).first()
                if permission is None:
                    permission = Permission(name=permission_name)
                    db.session.add(permission)
                role.permissions.append(permission)
        db.session.commit()

class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    roles = db.relationship('Role', secondary=roles_permissions, back_populates='permissions')

class Follow(db.Model):
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    follower = db.relationship('User', foreign_keys=[follower_id], back_populates='following', lazy='joined')
    followed = db.relationship('User', foreign_keys=[followed_id], back_populates='followers', lazy='joined')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # 资料
    username = db.Column(db.String(20), unique=True, index=True)
    email = db.Column(db.String(254), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(30))
    website = db.Column(db.String(255))
    bio = db.Column(db.String(120))
    location = db.Column(db.String(50))
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    # 用户状态
    confirmed = db.Column(db.Boolean(), default=False)

    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', back_populates='users')
    comments = db.relationship('Comment', back_populates='author', cascade='all')
    photos = db.relationship('Photo', back_populates='author', cascade='all')

    avatar_s = db.Column(db.String(255))
    avatar_m = db.Column(db.String(255))
    avatar_l = db.Column(db.String(255))

    collections = db.relationship('Collect', back_populates='collector', cascade='all')

    following = db.relationship('Follow', foreign_keys=[Follow.follower_id], back_populates='follower', lazy='dynamic', cascade='all')
    followers = db.relationship('Follow', foreign_keys=[Follow.followed_id], back_populates='followed', lazy='dynamic', cascade='all')

    notifications = db.relationship('Notification', back_populates='receiver', cascade='all')

    avatar_raw = db.Column(db.String(255))  # 用户上传的原始头像文件名

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        # ...
        self.set_role()
        self.generate_avatar()
        self.follow(self)  # 自己关注自己

    def set_role(self):
        if self.role is None:
            if self.email == current_app.config['ALBUMY_ADMIN_EMAIL']:
                self.role = Role.query.filter_by(name='Administrator').first()
            else:
                self.role = Role.query.filter_by(name='User').first()
            db.session.commit()
    
    def generate_avatar(self):
        avatar = Identicon()
        filenames = avatar.generate(text=self.username)
        self.avatar_s = filenames[0]
        self.avatar_m = filenames[1]
        self.avatar_l = filenames[2]
        db.session.commit()

    @property
    def is_admin(self):
        return self.role.name == 'Administrator'

    def can(self, permission_name):
        permission = Permission.query.filter_by(name=permission_name).first()
        return permission is not None and self.role is not None \
            and permission in self.role.permissions

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_collecting(self, photo):
        # return self.collected.filter_by(collected_id=photo.id).first() is not None  # 错误的逻辑，User 没有 collected 属性
        return Collect.query.with_parent(self).filter_by(collector_id=self.id, collected_id=photo.id).first() is not None

    def collect(self, photo):
        if not self.is_collecting(photo):
            collect = Collect(collector=self, collected=photo)
            db.session.add(collect)
            db.session.commit()

    def uncollect(self, photo):
        # collect = self.collected.filter_by(collected_id=photo.id).first()  # 错误的逻辑
        collect = Collect.query.with_parent(self).filter_by(collector_id=self.id, collected_id=photo.id).first()
        if collect:
            db.session.delete(collect)
            db.session.commit()

    def is_following(self, user):
        if user.id is None:
            return False
        return self.following.filter_by(followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        return self.followers.filter_by(follower_id=user.id).first() is not None

    def follow(self, user):
        if not self.is_following(user):
            follow = Follow(follower=self, followed=user)
            db.session.add(follow)
            db.session.commit()

    def unfollow(self, user):
        follow = self.following.filter_by(follower_id=self.id, followed_id=user.id).first()
        if follow:
            db.session.delete(follow)
            db.session.commit()

# 标签与图片的多对多关系使用关联表 tagging 存储
tagging = db.Table('tagging',
    db.Column('photo_id', db.Integer, db.ForeignKey('photo.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500))
    filename = db.Column(db.String(255))    # 原始尺寸的文件名
    filename_s = db.Column(db.String(255))  # 小型尺寸的文件名
    filename_m = db.Column(db.String(255))  # 中型尺寸的文件名
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    can_comment = db.Column(db.Boolean, default=True)
    flag = db.Column(db.Integer, default=0)  # 图片被举报次数

    author = db.relationship('User', back_populates='photos')
    tags = db.relationship('Tag', secondary=tagging, back_populates='photos')
    comments = db.relationship('Comment', back_populates='photo', cascade='all')

    collectors = db.relationship('Collect', back_populates='collected', cascade='all')


class Collect(db.Model):
    '''关联表只能用来表示关系，不能用来存储数据，例如 tagging。
    使用关联模型建立多对多关系可以用来存储数据。
    '''
    collector_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    collected_id = db.Column(db.Integer, db.ForeignKey('photo.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # 收藏的时间

    collector = db.relationship('User', back_populates='collections', lazy='joined')
    collected = db.relationship('Photo', back_populates='collectors', lazy='joined')


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), index=True)

    photos = db.relationship('Photo', secondary=tagging, back_populates='tags')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    flag = db.Column(db.Integer, default=0)

    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    photo_id = db.Column(db.Integer, db.ForeignKey('photo.id'))

    photo = db.relationship('Photo', back_populates='comments')
    author = db.relationship('User', back_populates='comments')
    replies = db.relationship('Comment', back_populates='replied', cascade='all')
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    is_read = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver = db.relationship('User', back_populates='notifications')

@db.event.listens_for(Photo, 'after_delete', named=True)
def delete_photos(**kwargs):
    ''''监听 Photo 记录删除后，自动删除对应文件。
    SQLAlchemy 文档：https://docs.sqlalchemy.org/en/latest/core/event.html#sqlalchemy.event.listens_for
    '''
    target = kwargs['target']
    for filename in [target.filename, target.filename_s, target.filename_m]:
        if filename is not None:
            path = os.path.join(current_app.config['ALBUMY_UPLOAD_PATH'], filename)
            if os.path.exists(path):
                os.remove(path)

