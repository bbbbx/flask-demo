import os
from datetime import datetime
from flask import Flask, request, redirect, url_for, abort, make_response, jsonify, session, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/hello')
def hello():
    # name = request.args.get('name', 'Flask')
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name', 'Human')  # 从 Cookie 中获取 name 的值
    response = '<h1>Hello %s!</h1>' % name

    # 根据用户的认证状态返回不同的内容
    if 'logged_in' not in session:
        abort(403)
    else:
        response += '[Authenticated]'
    return response

@app.route('/', methods=['get', 'post'])
def index():
    name = request.args.get('name', 'Venus')
    return render_template('user_bootstrap.html', name=name, comments=['awesome', 'nice', 'excellent!'], current_time=datetime.utcnow())

@app.route('/goback/<int:year>')
def goback(year):
    return '<p>Welcome to %d!</p>' % (2019 - year)

# @app.route('/colors/<any(blue, white, red):color>')
# def colors(color):
#     return '<p>Your color is %s!' % color

colors = ['blue', 'white', 'red']
@app.route('/colors/<any(%s):color>' % str(colors)[1:-1])
def colors(color):
    return '<p>Your color is %s!' % color

@app.before_request
def do_something():
    print('before request:', request.url)

@app.route('/res')
def res():
    return '<h1>Response</h1>', 201

@app.route('/302')
def redirect302():
    return '', 302, {'Location': 'https://venusworld.cn'}

@app.route('/red')
def red():
    return redirect('https://venusworld.cn')

@app.route('/hi')
def hi():
    return redirect(url_for('hello'))   # 重定向到视图函数 'hello' 对应的 URl，即 /hello

@app.route('/brew/coffee')
def not_found():
    abort(418)

@app.route('/404')
def teapot():
    abort(404)

@app.route('/foo')
def foo():
    response = make_response('Hello, World!')
    response.mimetype = 'text/plain'
    return response

@app.route('/note/<content_type>')
def note(content_type):
    content_type = content_type.lower()
    response = make_response('Unsupported content type!')
    if content_type == 'text':
        response = make_response('''
        Note\n
        to: Peter\n
        from: Jane\n
        heading: Reminder\n
        body: Don't forget the party!
        ''')
        response.mimetype = 'text/plain'
    if content_type == 'html':
        response = make_response('''
        <!DOCTYPE html>
        <html>
        <head></head>
        <body>
            <h1>Note</h1>
            <p>to: Peter</p>
            <p>from: Jane</p>
            <p>heading: Reminder</p>
            <p>body: <strong>Don't forget the party!</strong></p>
        </body>
        </html>
        ''')
        response.mimetype = 'text/html'
    if content_type == 'xml':
        response = make_response('''<?xml version="1.0" encoding="UTF-8"?>
        <note>
            <to>Peter</to>
            <from>Jane</from>
            <heading>Reminder</heading>
            <body>Don't forget the party!</body>
        </note>
        ''')
        response.mimetype = 'application/xml'
    if content_type == 'json':
        response = make_response('''
        {
            "note": {
                "to": "Peter",
                "from": "Jane",
                "heading": "Reminder",
                "body": "Don't forget the party!"
            }
        }
        ''')
        response.mimetype = 'application/json'
    return response

@app.route('/bar')
def bar():
    return jsonify(name='Venus', gender='male')

@app.route('/set/<name>')
def set_cookie(name):
    response = make_response(redirect(url_for('hello')))
    response.set_cookie('name', name)
    return response

app.secret_key = os.getenv('SECRET_KEY', 'secret string')  # 第二个参数为默认值
@app.route('/login')
def login():
    # session 对象可以像字典那样操作，
    # 我们向 session 中添加一个 logged-in 的 cookie，
    # 把它的值设为 True。
    session['logged_in'] = True

    # 当我们使用 session 对象添加 cookie 时，
    # 数据会使用秘钥进行加密，
    # 加密后的数据会存储在浏览器中名为
    # session 的 cookie 中。
    return redirect(url_for('hello'))

@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('hello'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', error=e), 404
