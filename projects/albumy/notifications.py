from flask import url_for
from albumy.models import Notification
from albumy.extensions import db

def push_follow_notification(follower, receiver):
    '''推送关注提醒'''
    message = '用户 <a href="%s">%s</a> 关注了你。' % \
              (url_for('user.index', username=follower.username), follower.username)
    notification = Notification(message=message, receiver=receiver)
    db.session.add(notification)
    db.session.commit()

def push_commit_notification(photo_id, receiver, page=1):
    '''推送评论提醒'''
    message = '<a href="%s">这个照片</a>有一个新的评论或回复。' % \
              (url_for('main.show_photo', photo_id=photo_id), page=page)
    notification = Notification(message=message, receiver=receiver)
    db.session.add(notification)
    db.session.commit()

def push_collect_notification(collector, photo_id, receiver):
    '''推送收藏提醒'''
    message = '用户 <a href="%s">%s</a> 收藏了你的 <a href="%s">照片</a>' % \
              (url_for('user.index', username=collector.username), collector.username, url_for('main.show_photo', photo_id=photo_id))
    notification = Notification(message=message, receiver=receiver)
    db.session.add(notification)
    db.session.commit()
