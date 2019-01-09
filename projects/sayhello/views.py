from flask import flash, redirect, url_for, render_template, request

from sayhello import app, db
from sayhello.models import Message
from sayhello.forms import HelloForm

@app.route('/', methods=['GET', 'POST'])
def index():
    form = HelloForm()
    if request.method == 'POST':
        if form.validate_on_submit() is False:
            flash('参数错误！', category='error')
        else:
            name = form.name.data
            body = form.body.data
            message = Message(body=body, name=name)  # 实例化模型类，创建数据库中的记录
            db.session.add(message)
            db.session.commit()
            flash('Your message have been sent to the world!')
        return redirect(url_for('index'))
    messages = Message.query.order_by(Message.timestamp.desc()).all()
    return render_template('index.html', messages=messages, form=form)
