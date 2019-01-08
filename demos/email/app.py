'''
不过要注意，应用要发送大量电子邮件时，
使用专门发送电子邮件的作业要比
给每封邮件都新建个线程更合适。
例如，我们可以把执行 send_async_email() 函数
的操作发给 Celery 任务队列。
'''
import os
import random
import time
from threading import Thread
from flask import Flask, render_template, redirect, url_for, session, flash, request, jsonify
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

@celery.task(bind=True)
def long_task(self):
    '''
    添加 bind=True 参数到 Celery 修饰器中，
    可以让 Celery 发送 self 参数到自定义的函数中，
    之后可以用这个参数来记录 state 的更新。
    '''
    # verb = ['启动', '加速', '修复', '加载', '检查']
    # adjective = ['精通的', '金闪闪的', '安静的', '和善的', '迅速的']
    # noun = ['太阳军团', '再生者', '宇宙射线', '轨道飞行器', '位']
    poetries = [
        '黑发不知勤学早，白首方悔读书迟。',
        '最是繁丝摇落后，转教人忆春山。',
        '天生我材必有用，千金散尽还复来。',
        '大鹏一日同风起，扶摇直上九万里。',
        '百战沙场碎铁衣，城南已合数重围。',
        '器乏雕梁器，材非构厦材。',
        '百岁落半途，前期浩漫漫。',
        '沉舟侧畔千帆过，病树前头万木春。'
    ]
    message = ''  # 发送一些滑稽的 message 给 client
    total = random.randint(10, 50)
    for i in range(total):
        if not message or random.random() < 0.25:
            # message = '{0}{1}{2}...'.format(random.choice(verb),
            #                                   random.choice(adjective),
            #                                   random.choice(noun))
            message = '{0}'.format(random.choice(poetries))

        # Celery 运行跟踪 task 当前的 state，
        # 有几个内置的 state，也可以自定义 state。
        # http://docs.celeryproject.org/en/latest/userguide/tasks.html#states
        self.update_state(state='PROGRESS', meta={'current': i, 'total': total, 'status': message})
        time.sleep(1)
    return {'current': 100, 'total': 100, 'status': 'Task completed!', 'result': 42}

@app.route('/longtask', methods=['POST'])
def longtask():
    task = long_task.apply_async()
    return jsonify({}), 202, {'Location': url_for('taskstatus', task_id=task.id)}

@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = long_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        # job did not start yet
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info)  # this is the exception raised
        }
    return jsonify(response)
