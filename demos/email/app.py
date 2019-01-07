'''
不过要注意，应用要发送大量电子邮件时，
使用专门发送电子邮件的作业要比
给每封邮件都新建个线程更合适。
例如，我们可以把执行 send_async_email() 函数
的操作发给 Celery 任务队列。
'''
import os
from threading import Thread
from flask import Flask, render_template, redirect, url_for, session, flash, request
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from celery import Celery

class NameForm(FlaskForm):
    name = StringField('你的名字？', validators=[DataRequired()])
    submit = SubmitField('提交')

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MAIL_SERVER'] = 'smtp.venusworld.cn'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

app.config['MAIL_SUBJECT_PREFIX'] = '[flask-mail demo]'
app.config['MAIL_SENDER'] = 'venus@venusworld.cn'
app.config['MAIL_ADMIN'] = 'venus@venusworld.cn'

mail = Mail(app)

BROKER_URL = 'amqp://'
RESULT_BACKEND = 'amqp'
celery = Celery(app.name, backend=RESULT_BACKEND, broker=BROKER_URL)
celery.conf.update(app.config)

# def send_async_email(app, msg):
#     with app.app_context():
#         mail.send(msg)

# def send_email(to, subject, template, **kwargs):
#     msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + subject, sender=app.config['MAIL_SENDER'], recipients=[to])
#     msg.body = render_template(template + '.txt', **kwargs)
#     msg.html = render_template(template + '.html', **kwargs)
#     thr = Thread(target=send_async_email, args=[app, msg])
#     thr.start()
#     return thr

@celery.task
def send_async_email(to, subject, content):
    msg = Message(subject=subject, sender=app.config['MAIL_SENDER'], recipients=[to])
    msg.body = content
    with app.app_context():
        mail.send(msg)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if request.method == 'GET':
        return render_template('index.html', form=form, name=session.get('name'), email=session.get('email', ''))
    email = request.form['email']
    session['email'] = email

    if request.method == 'POST':
        # send right away
        send_async_email.delay(email, 'Hello from Flask', 'This is a test email sent from a background Celery task.')
        flash('邮件已发至 {0}，请注意查收。'.format(email))
    return redirect(url_for('index'))

    # if form.validate_on_submit():
    #     result = send_email.delay(app.config['MAIL_ADMIN'], '新用户注册', 'new_user', name=form.name.data)
    #     session['name'] = form.name.data
    #     form.name.data = ''
    #     if result.ready() is not True:
    #         flash('发送邮件失败！')
    #     return redirect(url_for('index'))
    # return render_template('index.html', form=form, name=session.get('name'))
