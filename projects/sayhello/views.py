from flask import flash, redirect, url_for, render_template, request

from sayhello import app, db
from sayhello.models import Message
from sayhello.forms import HelloForm

# @app.route('/', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'], defaults={'page': 1})
@app.route('/<int:page>')
def index(page):
    # page = request.args.get('page', 1, type=int)
    form = HelloForm()
    # http://flask-sqlalchemy.pocoo.org/2.3/api/#flask_sqlalchemy.BaseQuery.paginate
    pagination = Message.query.order_by(Message.timestamp.desc()).paginate(page=page, per_page=50)
    if form.validate_on_submit():
        name = form.name.data
        body = form.body.data
        message = Message(body=body, name=name)
        db.session.add(message)
        db.session.commit()
        flash('发送成功!')
        return redirect(url_for('index'))
    return render_template('index.html', form=form, messages=pagination.items, pagination=pagination)


@app.route('/xlsxdemo')
def xlsxdemo():
    return render_template('xlsxdemo.html')
