<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Flask 工作原理与机制解析](#flask-%E5%B7%A5%E4%BD%9C%E5%8E%9F%E7%90%86%E4%B8%8E%E6%9C%BA%E5%88%B6%E8%A7%A3%E6%9E%90)
  - [Flask 源码](#flask-%E6%BA%90%E7%A0%81)
    - [Flask 版本对比](#flask-%E7%89%88%E6%9C%AC%E5%AF%B9%E6%AF%94)
  - [Flask 的设计理念](#flask-%E7%9A%84%E8%AE%BE%E8%AE%A1%E7%90%86%E5%BF%B5)
    - [两个核心依赖](#%E4%B8%A4%E4%B8%AA%E6%A0%B8%E5%BF%83%E4%BE%9D%E8%B5%96)
    - [显式程序对象](#%E6%98%BE%E5%BC%8F%E7%A8%8B%E5%BA%8F%E5%AF%B9%E8%B1%A1)
    - [本地上下文](#%E6%9C%AC%E5%9C%B0%E4%B8%8A%E4%B8%8B%E6%96%87)
    - [程序的三种状态](#%E7%A8%8B%E5%BA%8F%E7%9A%84%E4%B8%89%E7%A7%8D%E7%8A%B6%E6%80%81)
      - [程序设置状态](#%E7%A8%8B%E5%BA%8F%E8%AE%BE%E7%BD%AE%E7%8A%B6%E6%80%81)
      - [程序运行状态](#%E7%A8%8B%E5%BA%8F%E8%BF%90%E8%A1%8C%E7%8A%B6%E6%80%81)
      - [请求运行状态](#%E8%AF%B7%E6%B1%82%E8%BF%90%E8%A1%8C%E7%8A%B6%E6%80%81)
  - [Flask 与 WSGI](#flask-%E4%B8%8E-wsgi)
    - [WSGI 程序](#wsgi-%E7%A8%8B%E5%BA%8F)
    - [WSGI 服务器](#wsgi-%E6%9C%8D%E5%8A%A1%E5%99%A8)
    - [中间件](#%E4%B8%AD%E9%97%B4%E4%BB%B6)
  - [Flask 的工作流程与机制](#flask-%E7%9A%84%E5%B7%A5%E4%BD%9C%E6%B5%81%E7%A8%8B%E4%B8%8E%E6%9C%BA%E5%88%B6)
    - [Flask 中的请求响应循环](#flask-%E4%B8%AD%E7%9A%84%E8%AF%B7%E6%B1%82%E5%93%8D%E5%BA%94%E5%BE%AA%E7%8E%AF)
      - [程序启动](#%E7%A8%8B%E5%BA%8F%E5%90%AF%E5%8A%A8)
      - [请求 In](#%E8%AF%B7%E6%B1%82-in)
      - [响应 Out](#%E5%93%8D%E5%BA%94-out)
    - [路由系统](#%E8%B7%AF%E7%94%B1%E7%B3%BB%E7%BB%9F)
      - [路由注册](#%E8%B7%AF%E7%94%B1%E6%B3%A8%E5%86%8C)
      - [URL 匹配](#url-%E5%8C%B9%E9%85%8D)
    - [本地上下文](#%E6%9C%AC%E5%9C%B0%E4%B8%8A%E4%B8%8B%E6%96%87-1)
      - [`Local` 实现本地线程](#local-%E5%AE%9E%E7%8E%B0%E6%9C%AC%E5%9C%B0%E7%BA%BF%E7%A8%8B)
      - [`LocalStack` 实现上下文对象](#localstack-%E5%AE%9E%E7%8E%B0%E4%B8%8A%E4%B8%8B%E6%96%87%E5%AF%B9%E8%B1%A1)
      - [`LocalProxy` 实现代理](#localproxy-%E5%AE%9E%E7%8E%B0%E4%BB%A3%E7%90%86)
      - [请求上下文](#%E8%AF%B7%E6%B1%82%E4%B8%8A%E4%B8%8B%E6%96%87)
      - [程序上下文](#%E7%A8%8B%E5%BA%8F%E4%B8%8A%E4%B8%8B%E6%96%87)
      - [总结](#%E6%80%BB%E7%BB%93)
    - [请求和响应对象](#%E8%AF%B7%E6%B1%82%E5%92%8C%E5%93%8D%E5%BA%94%E5%AF%B9%E8%B1%A1)
      - [请求对象](#%E8%AF%B7%E6%B1%82%E5%AF%B9%E8%B1%A1)
      - [响应对象](#%E5%93%8D%E5%BA%94%E5%AF%B9%E8%B1%A1)
    - [session](#session)
      - [操作 session](#%E6%93%8D%E4%BD%9C-session)
      - [session 起源](#session-%E8%B5%B7%E6%BA%90)
    - [蓝图](#%E8%93%9D%E5%9B%BE)
    - [模板渲染](#%E6%A8%A1%E6%9D%BF%E6%B8%B2%E6%9F%93)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Flask 工作原理与机制解析

## Flask 源码

Flask 仓库中 `flask` 包各个模块及其说明：

|模块/包       |说明              |
|:----------- |:----------------|
|`json/`      |提供 JSON 支持|
|`__init__.py`|构造文件，导入了所有其他模块中开放的类和函数|
|`__main__.py`|用来启动 flask 命令|
|`_compat.py` |定义 Python 2 和 Python 3 版本兼容代码|
|`app.py`     |主模块，实现了 WSGI 程序对象，包含 `Flask` 类|
|`blueprints.py`|蓝图支持，包含 `Blueprint` 类的定义|
|`cli.py`     |提供命令行支持，包含内置的几个命令|
|`config.py`  |实现配置相关的对象|
|`ctx.py`     |实现上下文对象，比如请求上下文 `RequestContext`|
|`debughelpers.py`|一些辅助开发的函数/类|
|`globals.py`     |定义全局对象，比如 `request`、`session` 等|
|`helpers.py`     |包含一些常用的辅助函数，比如 `flask()`、`url_for()`|
|`logging.py`     |提供日志支持|
|`sessions.py`    |实现 session 功能|
|`signals.py`     |实现信号支持，定义了内置的信号|
|`templating.py`  |模板渲染功能|
|`testing.py`     |提供用于测试的辅助函数|
|`views.py`       |提供了类似 Django 中的视图类，用于编写 Web API 的 `MethodView` 就在这里定义|
|`wrappers.py`    |实现 WSGI 封装对象，比如代表请求和响应的 `Request` 和 `Response`|

对于一些某些不重要的模块，我们只需要知道大概的实现方法即可，例如 `cli.py`、`debughelpers.py`。我们关注的是实现 Flask 核心功能的模块，例如 WSGI 交互、蓝图、上下文等。

在读源码时我们需要带着两个问题去阅读：

- 这段代码实现了什么功能？
- 它是如何实现的？

例如 `flash()` 函数：

```python
def flash(message, category='message'):
    """给下一次 request 闪现一条消息。"""
    flashes = session.get('_flashes', [])
    flashes.append((category, message))
    session['_flashes'] = flashes
    message_flashed.send(current_app._get_current_object(),
                         message=message, category=category)
```

其中出现了一个不熟悉的 `message_flashed` 对象，我们可以先把它当作一个黑盒。通过查看对应的定义，可以大概知道这个对象的功能：一个信号对象（类似 Unix 系统的 signal 机制？），即更新 `session` 的 flashes 之后，给当前的 Flask 对象发送一个 `'message-flashed'` 信号。

在模板中，我们可以用 `get_flashed_message()` 函数获得消息：

```python
def get_flashed_messages(with_categories=False, category_filter=[]):
    """从 session 中获得所有已经闪现的消息，并返回它们。"""
    flashes = _request_ctx_stack.top.flashes
    if flashes is None:
        _request_ctx_stack.top.flashes = flashes = session.pop('_flashes') \
            if '_flashes' in session else []
    if category_filter:   # 类别过滤
        flashes = list(filter(lambda f: f[0] in category_filter, flashes))
    if not with_categories:    # 判断是否返回消息类别
        return [x[1] for x in flashes]
    return flashes
```

可以看到，先是从 `_request_ctx_stack.top.flashes` 中获取闪现消息，如果没有获取到，再从 `session` 中获取。同样，先把 `_request_ctx_stack.top` 当做一个黑盒，不过从变量名上可以推断出这是请求上下文的栈顶。

许多介绍 Linux 的书籍都会建议读者先阅读 Linux 0.x 版本（即初期版本）的代码，因为早期的代码仅保留了核心特性，而且代码量较少，容易阅读和理解。Flask 源码也是如此。Flask 最早发布的 0.1版本只包含一个核心文件：`flask.py`，不算空行大概只有 400+ 行代码，使用下面的命令迁出 0.1 版本的代码：

```sh
$ cd flask
$ git checkout 0.1
```

在 Flask 0.1 中，`flash()` 方法只有一行代码：

```python
def flash(message):
    session['_flashes'] = (session.get('_flashes', [])) + [message]
```

在 PyCharm 中，可以在窗口下方的 Version Control 工具栏中查看所有的代码提交记录，还可以在任意一个提交上单击右键选择 Checkout Revision 迁出这一版本的仓库，还可以单击 Show Diff 按钮，查看该变动与当前版本的对比。

### Flask 版本对比

Flask 当前最新的版本是 1.0.2，带 * 的版本为比较值得阅读的版本，其他版本大部分的变动都是在重构、优化代码以及修复错误。

|版本号（Tag）|发布日期|主要变化说明|
|:----------|:------|:---------|
|0.1*       |2010/4/16|第一个公开发布的版本，最精简的 Flask 版本|
|0.2        |2010/5/12|添加 `send_file()`；集成 JSON 支持|
|0.3        |2010/5/28|支持配置；集成日志（Logging）；`flash()` 消息支持分类|
|0.4*       |2010/6/18|新增 TESTING 标志|
|0.5*       |2010/7/6 |项目模块化重组（单模块拆分为多模块）|
|0.6        |2010/7/27|自动处理 OPTION 请求（返回该 URL 允许的 HTTP 方法，放在 `Allow` 头部中）；增加 `make_response*()` 函数；增加了基于 Blinker 的信号支持|
|0.7*       |2011/6/28|添加蓝图（Blueprint）支持；增加 `teardown_request` 钩子；支持基于类的视图|
|0.8        |2011/9/29|引入新的 session 交互系统；添加 `before_first_request` 钩子；添加扩展导入系统 `flask.ext`|
|0.9        |2012/7/1 |添加程序上下文 `flask.Flask.app_context()`；添加 `after_this_request` 钩子|
|0.10       |2013/6/13|cookie 序列化格式换为 JSON；添加 `template_test` 和 `template_global` 方法；`g` 存储到程序上下文中，而非请求上下文中|
|0.11       |2016/5/29|扩展导入系统 `flask.ext` 被弃用；添加 `flask.cli` 模块，内置命令行支持，并推荐使用 `flask run` 命令代替 `Flask.run()` 方法|
|0.12       |2016/9/21|完善 `cli` 模块|
|1.0*       |2018/4/27|引入 `FLASK_ENV` 环境变量，完善自动发现程序实例等 CLI 相关功能；支持从 `.env` 或 `.flaskenv` 文件中导入环境变量（基于 `python-dotenv`）；移除了多个弃用功能的代码；简化了日志系统|

完整的发布版本 Changelog 可以在 [http://flask.pocoo.org/docs/latest/changelog/](http://flask.pocoo.org/docs/latest/changelog/) 中查看。

## Flask 的设计理念

### 两个核心依赖

虽然 Flask 保持简单的核心，但它主要依赖两个库 —— Werkzeug 和 Jinja。Python Web 框架都需要处理 WSGI 交互，而 Werkzeug 本身就是一个非常优秀的 WSGI 工具库，没有理由不使用它。

Flask 与 Werkzeug 的联系非常紧密。从路由处理，到请求解析，再到响应的封装，以及上下文和各种数据结构都离不开 Werkzeug，有些函数（例如 `redirect`、`abort`）都是直接都 Werkzeug 引入的。想要深入了解 Flask，不然躲不开 Werkzeug。

引入 Jinja2 主要是因为大多数 Web 程序都需要渲染模板，不过 Flask 并不限制模板引擎的选择。

### 显式程序对象

在一些 Python Web 框架中，一个视图函数可能类似这样：

```python
from example_framework import route

@route('/')
def index():
    return 'Hello World!'
```

而在 Flask 中，则需要这样：

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'
```

主要区别在于：Flask 中存在一个显式的程序对象。这样设计的原因是：

1. 隐式程序对象在同一时间内只能由一个实例存在，而显式程序对象运行多个程序实例同时存在。
2. 允许通过子类化 `Flask` 类来修改程序行为。
3. Flask 需要通过传入的包名来定位资源（模板 templates 和静态资源 static）
4. 允许通过工厂模式来创建程序实例，可以在不同的地方传入不同的配置来创建不同的程序实例。
5. 允许通过蓝图来模块化程序。

这也是 Zen of Python 里的一条：“Explicit is better than implicit.”

### 本地上下文

如果直接将请求对象设为全局变量，那必然会在不同的线程中导致混乱（非线程安全）。本地线程（thread locals）的出现解决了这个问题。

本地线程就是一个全局对象，你可以使用一种特定线程却线程安全的方法来存储和获取数据。也就是说，同一个变量在不同的线程内拥有各自的变量，互不干扰。实现原理其实很简单，就是根据线程的 ID 来存储数据。Flask 没有使用标准库的 `threading.local()`，而是使用了 Werkzeug 实现的本地线程对象 `werkzeug.local.Local()`。

**Flask 使用本地线程来让上下文代理对象可以全局访问，比如 `request`、`session`、`current_app`、`g`，这些对象被称为本地上下文对象（context locals）。因此，在不基于线程、Greenlet 或进程实现并发的服务器上，这些代理对象将无法正常工作，但好在只有少部分服务器不被支持。Flask 的设计初衷是为了让传统 Web 程序的开发更加简单和迅速，而不是用来开发大型程序或异步服务的。但 Flask 的可扩展性却提供了无线的可能，除了使用扩展，我们还可以子类化 `Flask` 类，或是为程序添加中间件。**

注：[Greenlet](https://github.com/python-greenlet/greenlet) 是以 C 扩展形式接入 Python 的轻量级协程（协程：比线程更轻量，协程的暂停由程序控制（运行于用户态），线程的阻塞状态由操作系统内核来进行切换，协程的开销远小于线程）。

### 程序的三种状态

Flask 提供的 4 个本地上下文对象分别会在程序的特定状态下去绑定实际的对象。如果我们在访问它们的时候还没有绑定，就会出现 `RuntimeError` 异常。

Flask 程序有三种状态，分别是程序设置状态（application setup state）、程序运行状态（application runtime state）和请求运行状态（request runtime state）。

#### 程序设置状态

当 `Flask` 类被实例化后就进入了程序设置状态，这时，所有的全局对象都没有被绑定：

```python
>>> from flask import Flask, current_app, g, request, session
>>> app = Flask(__name__)
>>> current_app, g, request, session
(<LocalProxy unbound>, <LocalProxy unbound>, <LocalProxy unbound>, <LocalProxy unbound>)
```

#### 程序运行状态

当 Flask 程序启动，但还没有请求进入时，Flask 就进入了程序运行状态。这时，`current_app` 和 `g` 都绑定了各自的对象，使用 `flask shell` 命令打开的 Python shell 默认就是这种状态。我们可以通过手动 push 程序上下文来模拟：

```python
>>> ctx = app.app_context()
>>> ctx.push()
>>> current_app, g, request, session
(<Flask '__main__'>, <flask.g of '__main__'>, <LocalProxy unbound>, <LocalProxy unbound>)
```

默认情况下，当请求进入时，程序上下文会随着请求上下文一起被自动激活。

#### 请求运行状态

当请求进入时，或是使用 `test_request_context()` 方法、`test_client()` 方法时，Flask 就会进入请求运行状态。因为当请求上下文被 push 时，程序上下文也会被自动地 push，所以此时 4 个全局对象都会被绑定。可以通过手动 push 请求上下文模拟：

```python
>>> ctx = app.test_request_context()
>>> ctx.push()
>>> current_app, g, request, session
(<Flask '__main__'>, <flask.g of '__main__'>, <Request 'http://localhost/' [GET]>, <NullSession {}>)
>>> ctx.pop()
```

这也就是为什么可以直接在视图函数和对应的回调函数里直接使用这些上下文对象，而不用手动 push 上下文，因为 Flask 在处理请求时会自动帮你 push 请求上下文和程序上下文。

## Flask 与 WSGI

Werkzeug 是一个 WSGI 工具库。WSGI 是为了让 Web 服务器与 Python 程序能够进行数据交流而定义的一套接口标准/规范。

客户端和服务器端进行沟通需要遵循 HTTP 协议，而 HTTP 请求到 Web 程序之间还有另一个转换过程，即从 HTTP 报文格式到 WSGI 规定的数据格式。WSGI 可以认为是 WSGI 服务器和我们的 Web 程序进行沟通的语言。[PEP 3333](https://www.python.org/dev/peps/pep-3333/) 定义了新版的 WSGI。

### WSGI 程序

按照 WSGI 规定，Web 程序（WSGI 程序）必须是一个可调用对象（callable object)，该对象接收两个参数：

1. `environ`：包含请求的所有信息的字典
2. `start_response`：需要在可调用对象中调用的函数，用来发起响应，参数是状态码、响应头部等。

这个可调用对象可以是函数、方法、类或是实现了 `__call__` 方法的实例。用函数实现的 WSGI 程序：

```python
def hello(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-Type', 'text/html')]
    start_response(status, response_headers)
    return [b'<h1>Hello World</h1>']   # 返回列表
```

根据 WSGI 的定义，请求和响应的 body 应该为字符串（bytestrings），即 Python 2 中的 `str` 类型。在 Python 3 中字符串默认为 unicode 类型（unicode 不是编码方式？），因此需要在字符串前添加 `b`前缀，将字符串声明为 `bytes` 类型。

用 **类** 来实现可调用对象：

```python
class AppClass:
    
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response
    
    def __iter__(self):
        status = '200 OK'
        response_headers = [('Content-Type', 'text/html')]
        self.start(status, response_headers)
        yield b'<h1>Hello World</h1>'  # 这里要用 yield
```

如果想以 **类的实例**（不是类）作为 WSGI 程序，那么这个类必须实现 `__call__` 方法。

在 Flask 中，这个可调用对象就是 `Flask` 类的实例 `app`，所以 `Flask` 类实现了 `__call__` 方法：

```python
class Flask(_):

    def wsgi_app(self, environ, start_response):
        # ...

    def __call__(self, environ, start_response):
        """The WSGI server calls the Flask application object as the
        WSGI application. This calls :meth:`wsgi_app` which can be
        wrapped to applying middleware."""
        return self.wsgi_app(environ, start_response)
```

`__call__` 方法内部调用了 `wsgi_app` 方法，请求进入和响应的返回就发生在这里，WSGI 服务器通过调用这个方法来传入请求数据，获取返回的响应。

### WSGI 服务器

写好 WSGI 程序后，我们需要一个 WSGI 服务器来运行它。Python 提供了一个 `wsgiref` 库，可以在开发时使用：

```python
from wsgiref.simple_server import make_server

def hello(environ, start_response):
    # 定义 WSGI 程序 ...

server = make_server('localhost', 5000, hello)
server.serve_forever()
```

**WSGI 服务器** 启动后，它会监听 `5000` 端口。当接收到 HTTP 请求后，它会把 HTTP 报文解析为一个 `environ` 字典，然后 **调用WSGI 程序** 提供的可调用对象，并将这个字典和 `start_response` 函数作为参数传给 WSGI 程序。

在浏览器访问 `http://localhost:5000` 时，这个 WSGI 服务器会将接收到的 HTTP 请求报文解析为 `environ` 字典，然后调用 `hello()` 函数，并将 `environ` 和 `start_response` 作为参数传递进去，最后把 `hello()` 函数的返回值处理为 HTTP 响应报文返回给浏览器。

无论是 Werkzeug 内置的用于开发使用的服务器，还是 Gunicorn、uWSGI 等都是实现了这类规范的 WSGI 服务器，正因为遵循了统一的 WSGI 规范，所以这些 WSGI 服务器都可以用来运行我们的 Flask 程序。

### 中间件

WSGI 允许使用中间件包装 WSGI 程序，为程序在被调用之前添加额外的功能。中间件可以被用来解耦程序的功能，达到分层的目的。

```python
from wsgiref.simple_server import make_server

def hello(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-Type', 'text/html')]
    start_response(status, response_headers)
    return [b'<h1>Hello World</h1>']

class MyMiddleware(object):
    def __init__(self, app):
        self.app = app
    
    def __call__(self, environ, start_response):
        def custom_start_response(status, headers, exc_info=None):
            headers.append(('A-Costom-Header', 'Nothing'))
            return start_response(status, headers)

        return self.app(environ, custom_start_response)

wrapped_app = MyMiddleware(hello)
server = make_server('localhost', 5000, wrapped_app)
server.serve_forever()
```

中间件接收可调用对象作为参数。这个可调用对象也可以是其他中间件包装的可调用对象。

使用类定义的中间件必须实现 `__call__` 方法，接收 `environ` 和 `start_response` 作为参数，最后传入这两个参数调用实例化时传入的可调用对象。上面的中间件自定义了一个 `custom_start_response` 方法，并将该方法代替 `start_response` 方法，最后向 HTTP 响应添加一个自定义的头部。

在 Flask 中，实际的 WSGI 可调用对象是 `Flask.wsgi_app()` 方法，因此，如果我们自己实现了中间件，那么最佳的方式是嵌套在这个 `wsgi_app` 对象上：

```python
class MyMiddleware(object):
    pass

app = Flask(__name__)
app.wsgi_app = MyMiddleware(app.wsgi_app)
```

## Flask 的工作流程与机制

### Flask 中的请求响应循环

#### 程序启动

无论是使用 `flask run` 命令（会调用 `flask.cli.run_command()` 函数）还是使用被弃用的 `flask.Flask.run()` 方法来启动开发服务器，它们都在最后调用了 `werkzeug.serving` 模块中的 `run_simple()` 函数。

```python
def run_simple(hostname, port, application, use_reloader=False,
               use_debugger=False, use_evalex=True,
               extra_files=None, reloader_interval=1,
               reloader_type='auto', threaded=False,
               processes=1, request_handler=None, static_files=None,
               passthrough_errors=False, ssl_context=None):

    if not isinstance(port, int):
        raise TypeError('port must be an integer')
    if use_debugger:   # 判断是否使用了调试器
        from werkzeug.debug import DebuggedApplication
        application = DebuggedApplication(application, use_evalex)
    if static_files:
        from werkzeug.wsgi import SharedDataMiddleware
        application = SharedDataMiddleware(application, static_files)

    def inner():
        try:
            fd = int(os.environ['WERKZEUG_SERVER_FD'])
        except (LookupError, ValueError):
            fd = None
        srv = make_server(hostname, port, application, threaded,
                          processes, request_handler,
                          passthrough_errors, ssl_context,
                          fd=fd)
        if fd is None:
            log_startup(srv.socket)
        srv.serve_forever()

    # ...

    if use_reloader:   # 判断是否使用重载器
        # ...
        from werkzeug._reloader import run_with_reloader
        run_with_reloader(inner, extra_files, reloader_interval,
                          reloader_type)
    else:
        inner()
```

这里使用到了两个 Werkzeug 提供的中间件，如果 `use_debugger` 为 `True`，即开启了调试模式，那就使用 `DebuggedApplication` 中间件为程序添加调试功能。如果 `static_file` 为 `True`，那就使用 `SharedDataMiddleware` 中间为程序提供静态文件的功能。

这个方法最终会调用 `inner()` 函数，它使用 `make_server()` 方法创建 WSGI 服务器，然后调用 `serve_forever()` 方法运行服务器。当接收到 HTTP 请求报文后，WSGI 服务器就会调用 Web 程序中提供的可调用对象，这个对象就是我们的程序实例 `app`，然后请求进入了。

#### 请求 In

`Flask` 类实现了 `__call__()` 方法，当程序实例被调用时会执行这个方法，而这个方法内部调用了 `Flask.wsgi_app()` 方法：

```python
class Flask(_PackageBoundObject):
    # ...
    def wsgi_app(self, environ, start_response):
        ctx = self.request_context(environ)
        error = None
        try:
            try:
                ctx.push()
                response = self.full_dispatch_request()
            except Exception as e:
                error = e
                response = self.handle_exception(e)
            except:
                error = sys.exc_info()[1]
                raise
            return response(environ, start_response)
        finally:
            if self.should_ignore_error(error):
                error = None
            ctx.auto_pop(error)
```

从 `wsgi_app()` 方法接收的参数可以看出，这个 `wsgi_app()` 方法就是隐藏在 Flask 中的那个 WSGI 程序。这个将 WSGI 程序实现在单独的方法里，主要是为了方便在附加中间件的同时，又保留对程序实例的引用。

其中终点在 `try...except...`，它尝试从 `Flask.full_dispatch_request()` 方法获取响应，如果出错就根据错误类型来生成错误的响应。

```python
class Flask(_PackageBoundObject):
    # ...
    def full_dispatch_request(self):
        """将请求分发出去并对请求进行预处理和后处理，
        同时捕获 HTTP 异常和处理错误。
        """
        self.try_trigger_before_first_request_functions()
        try:
            request_started.send(self)       # 发送请求进入信号
            rv = self.preprocess_request()   # 预处理请求
            if rv is None:
                rv = self.dispatch_request() # 分发请求给匹配的视图函数，并获取视图函数的返回值
        except Exception as e:
            rv = self.handle_user_exception(e)  # 获取处理异常的视图函数的返回值
        return self.finalize_request(rv)     # 最终处理，将视图函数的返回值转为 HTTP 响应，并进行后处理
```

这个函数首先会调用 `preprocess_request()` 分发对请求进行预处理（request preprocessing），这会指向所有使用 `before_request` 钩子注册的函数。然后会调用 `dispatch_request()` 方法，它会调用与 URL 对应的视图函数，然后获取视图函数的返回值。最终会调用 `finalize_request()` 方法，并传入视图函数的返回值来生成响应。

#### 响应 Out

```python
class Flask(_PackageBoundObject):
    # ...
    def finalize_request(self, rv, from_error_handler=False):
        """将视图函数的返回值转换为响应，然后调用所有的后处理函数。"""
        response = self.make_response(rv)  # 生成响应对象
        try:
            response = self.process_response(response)     # 响应预处理
            request_finished.send(self, response=response) # 发送信号
        except Exception:
            if not from_error_handler:
                raise
            self.logger.exception('Request finalizing failed with an '
                                  'error while handling an error')
        return response
```

需要注意的是，这里的 `make_response()` 方法并不是我们从 `flask` 导入并在视图函数中生成响应对象的 `make_response`，我们平时使用的 `make_response` 是 `helpers` 模块中的 `make_response()` 函数，它对传入的参数进行简单的处理后，便将参数传给 `Flask` 类的 `make_response` 方法并返回。

创建了响应对象之后，会调用 `process_response()` 方法，这个方法会在把响应发送给 WSGI 服务器之前执行所有使用 `after_request` 钩子注册的函数。

返回响应之后，代码执行流程就回到了 `wsgi_app()` 方法，最终返回响应对象，WSGI 服务器会将这个响应对象转为 HTTP 响应报文发送给客户端。

下面我们来详细分析这一过程中发生的细节，如路由处理、请求和响应对象的封装等。

### 路由系统

#### 路由注册

Flask 的路由依赖于 Werkzeug 的路由实现。我们先看看如何在 Werkzeug 中使用路由功能：

```python
from werkzeug.routing import Map, Rule
m = Map()
rule1 = Rule('/', endpoint='index')
rule2 = Rule('/downloads/', endpoint='downloads.index')
rule3 = Rule('/downloads/<int:id>', endpoint='downloads.show')
m.add(rule1)
m.add(rule2)
m.add(rule3)
```

而在 Flask 中，我们使用 `route()` 装饰器来将视图函数注册为路由，`Flask.route()` 是 `Flask` 类实例的方法：

```python
class Flask(_PackageBoundObject):
    # ...
    def route(self, rule, **options):
        def decorator(f):
            endpoint = options.pop('endpoint', None)
            self.add_url_rule(rule, endpoint, f, **options)
            return f
        return decorator
```

route 装饰器内部调用了 `add_url_rule()` 来添加 URL 规则，所以注册路由也可以直接使用 `add_url_rule` 实现（0.2 版本及之后）。add_url_rule 的定义：

```python
class Flask(_PackageBoundObject):
    # ...
    @setupmethod
    def add_url_rule(self, rule, endpoint=None, view_func=None,
                     provide_automatic_options=None, **options):
        # 设置端点和 HTTP 方法 ...
        rule = self.url_rule_class(rule, methods=methods, **options)
        rule.provide_automatic_options = provide_automatic_options

        self.url_map.add(rule)   # 重点语句
        if view_func is not None:
            old_func = self.view_functions.get(endpoint)
            if old_func is not None and old_func != view_func:
                raise AssertionError('View function mapping is overwriting an '
                                     'existing endpoint function: %s' % endpoint)
            self.view_functions[endpoint] = view_func   # 重点语句
```

这个方法的重点语句是：

```python
self.url_map.add(rule)
# ...
self.view_functions[endpoint] = view_func
```

这里引入了两个对象：`url_map` 和 `view_functions`。`url_map` 是 Werkzeug 的 `Map` 类实例（`werkzeug.routing.Map`），它存储了 URL 规则和相关的配置，而 `rule` 是 `Rule` 类实例（`werkzeug.routing.Rule`），其中保存了 URL 规则和端点的映射关系。

而 `view_functions` 是 `Flask` 类定义的一个字典，它存储了端点和视图函数的映射关系。

Flask 的路由注册和 Werkzeug 的差不多：

```python
self.url_rule_class = Rule
self.url_map = Map()
rule = self.url_rule_class(rule, methods=methods, **options)
self.url_map.add(rule)
```

其中的 `url_rule_class` 存储了 `Rule` 类，而 `url_rule` 是 `Map` 类的实例。

#### URL 匹配

先来看下 Werkzeug 路由的 URL 匹配：

```bash
>>> urls = m.bind('example.com')   # 传入主机名作为参数
>>> urls.match('/', 'GET')
('index', {})
>>> urls.match('/downloads/42')
('download.show', {'id': 42})
>>> urls.match('/downloads')
Traceback (most recent call last):
 ...
 raise RequestSlash()
werkzeug.routing.RequestSlash
>>> urls.match('/missing')
Traceback (most recent call last):
 ...
werkzeug.exceptions.NotFound: 404 Not Found
```

`Map.bind()` 和 `Map.bind_to_environ()` 方法都会返回一个 `MapAdapter` 对象，它负责匹配和构建 URL。`MapAdapter` 类的 `match` 方法用来判断传入的 URL 是否匹配 `Map` 对象中存储的路由规则（存储在 `self.map._rules` 列表中）。

`MapAdapter` 类的 `build()` 方法用于创建 URL，Flask 的 `url_for()` 函数内部就是通过 `build()` 方法实现的。`build` 方法的用法：

```python
>>> urls.build('index', {})
'/'
>>> urls.build('downloads.show', {'id': 42})
'/downloads/42'
>>> urls.build('downloads.show', {'id': 42}, force_external=True)
'http://example.com/downloads/42'
```

这只是 Werkzeug 路由系统的一部分，全部内容可以查看 http://werkzeug.pocoo.org/docs/latest/routing/。

得到 URL 和端点和映射关系之后，就需要依据端点找到对应视图函数并执行，这个功能由 `dispatch_request()` 方法实现：

```python
class Flask(_PackageBoundObject):
    def dispatch_request(self):
        req = _request_ctx_stack.top.request
        if req.routing_exception is not None:
            self.raise_routing_exception(req)
        rule = req.url_rule
        # 如果给这个 URL 提供了 automatic 选项，且该请求是 HTTP 的 OPTIONS 方法，则自动响应。
        if getattr(rule, 'provide_automatic_options', False) \
           and req.method == 'OPTIONS':
            return self.make_default_options_response()
        # 否则就调用对应的视图函数
        return self.view_functions[rule.endpoint](**req.view_args)
```

正是 `dispatch_request()` 方法实现了从请求的 URL 找到端点，再从端点找到对应的视图函数并执行。

另外，这里的 `rule` 直接通过 `_request_ctx_stack.top.request` 对象（请求上下文对象）的 `url_rule` 属性获取。由此可知，URL 的匹配工作在请求上下文对象中实现，请求上下文对象在 `ctx.py` 模块中定义：

```python
class RequestContext(object):
    def __init__(self, app, environ, request=None, session=None):
        self.app = app
        if request is None:
            request = app.request_class(environ)
        self.request = request
        self.url_adapter = None
        try:
            self.url_adapter = app.create_url_adapter(self.request)
        except HTTPException as e:
            self.request.routing_exception = e
        # ...
        if self.url_adapter is not None:
            self.match_request()   # 匹配请求到对应的视图函数
```

在请求上下文对象的构造函数中调用了 `match_request()` 方法，顾名思义，这个方法用来匹配请求：

```python
class RequestContext(object):
    # ...
    def match_request(self):
        try:
            url_rule, self.request.view_args = \
                self.url_adapter.match(return_rule=True)
            self.request.url_rule = url_rule
        except HTTPException as e:
            self.request.routing_exception = e
```

可以看到，使用了 `MapAdapter` 类实例（即 `url_adapter`）的 `match` 方法（并设置 `return_rule=True`）来创建请求上下文对象的 `url_rule` 属性。

而 `url_adapter` 属性在构造函数中通过 `app.create_url_adapter()` 方法创建：

```python
class Flask(_PackageBoundObject):
    # ...
    def create_url_adapter(self, request):
        if request is not None:
            # 如果关闭了子域名匹配（默认值），则使用默认的子域名。
            subdomain = ((self.url_map.default_subdomain or None)
                         if not self.subdomain_matching else None)
            return self.url_map.bind_to_environ(
                request.environ,
                server_name=self.config['SERVER_NAME'],
                subdomain=subdomain)
        # We need at the very least the server name to be set for this
        # to work.
        if self.config['SERVER_NAME'] is not None:
            return self.url_map.bind(
                self.config['SERVER_NAME'],
                script_name=self.config['APPLICATION_ROOT'],
                url_scheme=self.config['PREFERRED_URL_SCHEME'])
```

可以看到，这个方法最终调用了 `Map` 类实例（即 `url_map`）的 `bind()` 方法或 `bind_to_environ()` 方法，所以，最终会返回一个 `MapAdapter` 类实例。

回到上面的 `dispatch_request()` 方法，`url_rule` 属性是 `Rule` 类的实例，而 `Rule` 类在实例化时需要传入一个端点参数，存储在实例的 `endpoint` 属性下，所以，在 `dispatch_request()` 的最后一行代码中，通过 `view_functions` 字典，根据端点作为键即可找到视图函数，并调用该视图函数：

```python
rule = req.url_rule
# ...
return self.view_functions[rule.endpoint](**req.view_args)
```

而参数 `**req.view_args` 包含了 URL 中解析出来的变量值，也就是 `match()` 函数返回的第二个值，这时代码执行流程才终于走到视图函数中。

### 本地上下文

Flask 提供了 2 种上下文：请求上下和程序上下文。这 2 种上下文分别包含 `request`、`session`、`current_app` 和 `g` 这 4 个变量，这些变量是实际对象的本地代理（local proxy），因此这些变量被称为本地上下文（context locals）。这些代理对象定义在 `globals.py` 模块中，该模块还包含了和上下文相关的 2 个错误信息和 3 个函数：

```python
from functools import partial
from werkzeug.local import LocalStack, LocalProxy

# 两个错误信息
_request_ctx_err_msg = '''\
Working outside of request context.
'''
_app_ctx_err_msg = '''\
Working outside of application context.
'''

# 查找请求上下文对象
def _lookup_req_object(name):
    top = _request_ctx_stack.top
    if top is None:
        raise RuntimeError(_request_ctx_err_msg)
    return getattr(top, name)

# 查找程序上下文对象
def _lookup_app_object(name):
    top = _app_ctx_stack.top
    if top is None:
        raise RuntimeError(_app_ctx_err_msg)
    return getattr(top, name)

# 查找程序实例
def _find_app():
    top = _app_ctx_stack.top
    if top is None:
        raise RuntimeError(_app_ctx_err_msg)
    return top.app

# 2 个栈
_request_ctx_stack = LocalStack()
_app_ctx_stack = LocalStack()

# 4 个全局上下文代理对象
current_app = LocalProxy(_find_app)
request = LocalProxy(partial(_lookup_req_object, 'request'))
session = LocalProxy(partial(_lookup_req_object, 'session'))
g = LocalProxy(partial(_lookup_app_object, 'g'))
```

从 `flask` 包直接导入的 `request` 和 `session` 就是这里定义的全局对象，这两个对象是对实际的 request 变量和 session 对象的代理。在了解代理之前，要先了解本地线程。

#### `Local` 实现本地线程

在处理多个请求时使用多线程后，如何确保这时的 `request` 对象是我们需要的那个呢？比如 A 用户和 B 用户同一时间访问 hello 视图，这时服务器分配了两个线程来处理这两个请求，如何确保每个线程内的 `request` 对象都是各自对应、互不干扰的？

解决方法是引入本地线程（Thread Local）的概念，在保存数据的同时记录下线程的 ID，获取数据时根据请求所在线程的 ID 即可获取到对应的数据，Werkzeug 提供的开发服务器默认会开启多线程支持。

Flask 中的本地线程使用了 Werkzeug 提供的 `Local` 类来实现，`werkzeug/local.py`：

```python
try:
    from greenlet import getcurrent as get_ident
except ImportError:
    try:
        from thread import get_ident
    except ImportError:
        from _thread import get_ident

class Local(object):
     __slots__ = ('__storage__', '__ident_func__')

    def __init__(self):
        object.__setattr__(self, '__storage__', {})
        object.__setattr__(self, '__ident_func__', get_ident)
    
    def __iter__(self):
        return iter(self.__storage__.items())

    def __call__(self, proxy):
        """Create a proxy for a name."""
        return LocalProxy(self, proxy)
    
    def __release_local__(self):
        self.__storage__.pop(self.__ident_func__(), None)

    # 获取属性时
    def __getattr__(self, name):
        try:
            return self.__storage__[self.__ident_func__()][name]
        except KeyError:
            raise AttributeError(name)
    
    # 设置属性时
    def __setattr__(self, name, value):
        ident = self.__ident_func__()
        storage = self.__storage__
        try:
            storage[ident][name] = value
        except KeyError:
            storage[ident] = {name: value}
    
    # 删除属性时
    def __delattr__(self, name):
        try:
            del self.__storage__[self.__ident_func__()][name]
        except KeyError:
            raise AttributeError(name)
```

`Local` 的构造函数中定义了 2 个属性：`__storage__` 和 `__ident_func__`。其中 `__storage__` 是一个嵌套字典，外层的字典使用了线程 ID 作为键来匹配内部的字典，内部的字典存储了真正的数据。它使用 `self.__storage__[self.__ident_func__()][name]` 来获取数据。例如，一个 `Local` 实例中的 `__storage__` 属性可能是：

```python
{
    线程 ID: {
        name1: 真正的数据,
        name2: 真正的数据,
    }
}
```

这里获取线程 ID 的方法是使用了 `get_ident()` 方法。这样一来，全局使用的上下文对象就不会在多个线程中产生混乱。

注：这里会先优先使用 Greenlet 提供的 **协程 ID**，如果 Greenlet 不可用再使用 `thred` 模块获取 **线程 ID**。还要注意的是，`Local` 类实例被调用时会返回一个 `LocalProxy` 类实例，这个对象在后面讲。

在 Python 类中，前后双下划线的方法常被称为魔方方法（Magic Methods），我们可以通过重写这些方法来改变类的行为。比如 `__init__()` 会在类被实例化时调用，`__repr__()` 会在类实例被打印时调用，`__getattr__()`、`__setattr__()`、`__delattr__()` 方法分别会在类属性被访问、设置、删除时调用，`__iter__()` 会在类实例被迭代时调用，`__call__()` 会在类实例被调用时执行。完整的列表可以查看 [https://docs.python.org/3/reference/datamodel.html](https://docs.python.org/3/reference/datamodel.html)。

#### `LocalStack` 实现上下文对象

Flask 的上下文对象存储在一个栈结构中，`globals.py` 模块的后两行代码创建了请求上下文栈和程序上下文栈：

```python
_request_ctx_stacl = LocalStack()  # 请求上下文栈
_app_ctx_stack = LocalStack()      # 程序上下文栈
```

我们平时导入的 `request` 对象就是保存在栈里的一个 `RequestContext` 实例，导入的操作相当于获取请求上下文栈的栈顶。`werkzeug/local.py` 定义的 `LocalStack`：

```python
class LocalStack(object):
    def __init__(self):
        self._local = Local()

    def __release_local__(self):
        self._local.__release_local__()
    
    # ...

    def __call__(self):
        def _lookup():
            rv = self.top
            if rv is None:
                raise RuntimeError('object unbound')
            return rv
        return LocalProxy(_lookup)
    
    def push(self, obj):
        """Pushes 一个新的 item 进栈。"""
        rv = getattr(self._local, 'stack', None)
        if rv is None:
            self._local.stack = rv = []
        rv.append(obj)
        return rv

    def pop(self):
        """移除并返回栈顶，如果栈为空则返回 `None`。"""
        stack = getattr(self._local, 'stack', None)
        if stack is None:
            return None
        elif len(stack) == 1:
            release_local(self._local)
            return stack[-1]
        else:
            return stack.pop()
    
    @property
    def top(self):
        """获取栈顶，如果栈为空则返回 `None`。"""
        try:
            return self._local.stack[-1]
        except (AttributeError, IndexError):
            return None
```

简单来说，`LocalStack` 就是基于 `Local` 实现的栈结构（即实现了本地线程的栈）。在构造函数中创建了 `Local()` 类的实例 `_local`，并将数据存放到 `_local.stack` 列表里。

注：`LocalStack` 和 `Local` 一样定义了 `__cal__` 方法，当 `LocalStack` 实例被调用时会返回栈顶对象的代理，即 `LocalProxy` 类的实例。

为什么 Flask 要使用 `LocalStack` 而不是直接使用 `Local` 存储上下文对象？主要原因是为了支持多程序共存。如果使用 Werkzeug 提供的 `DispatcherMiddleware` 中间件就可以把多个程序组合成一个 WSGI 程序运行，该中间件会根据请求的 URL 来分发给对应的程序处理，在这种情况下，就会有多个程序上下文存在，而使用栈结构可以让多个程序上下文共存。而活动的当前上下文总是可以在栈顶获得，我们可以在 `globals.py` 模块中的 `_request_ctx_context.top` 属性来获取当前的请求上下文对象。

#### `LocalProxy` 实现代理

代理（Proxy）是一种设计模式，通过代理对象，我们可以使用这个代理对象来操作实际的对象。

`Local` 类实例和 `LocalStack` 类实例被调用时都会使用 `LocalProxy` 包装成一个代理，因此当下面两个对象被调用时会返回代理：

```python
_request_ctx_stacl = LocalStack()  # 请求上下文栈
_app_ctx_stack = LocalStack()      # 程序上下文栈
```

`LocalProxy` 的定义：

```python
@implements_bool
class LocalProxy(object):
    __slots__ = ('__local', '__dict__', '__name__', '__wrapped__')

    def __init__(self, local, name=None):
        object.__setattr__(self, '_LocalProxy__local', local)
        object.__setattr__(self, '__name__', name)
        if callable(local) and not hasattr(local, '__release_local__'):
            # "local" is a callable that is not an instance of Local or
            # LocalManager: mark it as a wrapped function.
            object.__setattr__(self, '__wrapped__', local)
    
    def _get_current_object(self):
        """获取被代理的真实对象。"""
        if not hasattr(self.__local, '__release_local__'):
            return self.__local()
        try:
            return getattr(self.__local, self.__name__)
        except AttributeError:
            raise RuntimeError('no object bound to %s' % self.__name__)
    
    # ...

    def __getattr__(self, name):
        if name == '__members__':
            return dir(self._get_current_object())
        return getattr(self._get_current_object(), name)
    
    def __setitem__(self, key, value):
        self._get_current_object()[key] = value

    def __delitem__(self, key):
        del self._get_current_object()[key]
    
    # ...
```

注意：在 Python 类中，`__foo` 形式的属性会被替换为 `_classname__foo` 的形式，这种双下划线开头的属性在 Python 中表示类私有属性（私有程度强于单下划线）。这也是为什么在 `LocalProxy` 类的构造函数中设置了一个 `_LocalProxy__local` 属性，而在其他方法中却可以简写为 `__local`。

`LocalProxy` 定义了 50+ 个魔法方法，还定义了一个 `_get_current_object()` 方法，用来获取被代理的真实对象。可以用这个方法获取被 `current_user`（flask-login） 代理的当前用户对象。

Flask 为什么要使用代理呢？使用代理对象是因为这些代理可以在线程间共享，且可以让我们以动态的方式来获取被代理的真实对象。

当上下文还没 push 时，4 个全局对象就会处于未绑定状态，而如果不使用代理，那在导入这 4 个全局对象时就会尝试获取上下文，然而此时栈是空的，所以获取的全局对象只能是 `None`。当请求进入并调用视图函数时，虽然此时栈里已经 push 进了上下文，但之前导入的全局对象仍然是 `None`，而如果使用了代理，就可以动态地获取到上下文对象，自然就可以获取到正确的全局对象。

#### 请求上下文

在 Flask 中，请求上下文由 `RequestContext` 类表示。当请求进入时，被 WSGI 程序调用的 `Flask` 类实例（即我们的程序实例 `app`）会在 `wsgi_app()` 方法中调用 `Flask.request_context()` 方法。这个方法会实例化 `RequestContext` 类作为请求上下文，然后 `wsgi_app()` 会调用请求上下文的 `push()` 方法将请求上下文 push 进请求上下文栈，然后开始分开请求。`flask/ctx.py` 中定义的 `RequestContext`：

```python
class RequestContext(object):

    def __init__(self, app, environ, request=None, session=None):
        self.app = app
        if request is None:
            request = app.request_class(environ)
        self.request = request     # 请求对象
        self.url_adapter = None
        try:
            self.url_adapter = app.create_url_adapter(self.request)
        except HTTPException as e:
            self.request.routing_exception = e
        self.flashes = None        # flask 消息列表
        self.session = session     # session 字典
    
        self._implicit_app_ctx_stack = []
        self.preserved = False
        self._preserved_exc = None
        self._after_request_functions = []
        if self.url_adapter is not None:
            self.match_request()
    
    # ...

    def push(self):
        """绑定该请求上下文到当前的上下文。"""
        top = _request_ctx_stack.top    # 获取请求上下文栈顶
        if top is not None and top.preserved:
            top.pop(top._preserved_exc)
        
        # ...

        # 把该请求上下文 push 进上下文栈
        _request_ctx_stack.push(self)

        if self.session is None:
            session_interface = self.app.session_interface
            self.session = session_interface.open_session(
                self.app, self.request
            )

            if self.session is None:
                self.session = session_interface.make_null_session(self.app)

    def pop(self, exc=_sentinel):
        app_ctx = self._implicit_app_ctx_stack.pop()
        try:
            clear_request = False
            if not self._implicit_app_ctx_stack:
                self.preserved = False
                self._preserved_exc = None
                if exc is _sentinel:
                    exc = sys.exc_info()[1]
                self.app.do_teardown_request(exc)  # 这里会执行所有使用 `teardown_request` 构造注册的函数
                
                if hasattr(sys, 'exc_clear'):
                    sys.exc_clear()

                request_close = getattr(self.request, 'close', None)
                if request_close is not None:
                    request_close()
                clear_request = True
        finally:
            rv = _request_ctx_stack.pop()
        # ...
    
    def __enter__(self):
        self.push()
        return self
    
    def __exit__(self, exc_type, exc_value, tb):
        self.auto_pop(exc_value)

        if BROKEN_PYPY_CTXMGR_EXIT and exc_type is not None:
            reraise(exc_type, exc_value, tb)
```

构造函数中创建了 `request` 和 `session` 属性，`request` 属性为空时使用 `app.request_class(environ)` 创建，其中的 `environ` 字典包含了请求信息。而 `session` 属性在构造函数中还只是 `None`，它会在 `push()` 方法中进一步定义，即在请求上下文被 push 进请求上下文栈时。

另外，`pop()` 方法中还调用了 `do_teardown_request()` 方法，这个方法会执行所有使用 `teardown_request` 钩子注册的函数。

`__enter__()` 和 `__exit__()` 魔法方法会分别在进入和退出 `with` 语句时调用，这里用来在 `with` 语句执行前后分别 push 和 pop 请求上下文。

#### 程序上下文

程序上下文 `AppContext` 类的定义和 `RequestContext` 类基本相同，但要简单一些。它的构造函数里创建了 `current_app` 全局对象指向的 `app` 属性和 `g` 全局对象指向的 `g` 属性：

```python
class AppContext(object):
    def __init__(self, app):
        self.app = app
        self.url_adapter = app.create_url_adapter(None)
        self.g = app.app_ctx_globals_class()

        # ...
    
    def push(self):
        # ...
    
    def pop(self, exc=_sentinel):
        # ...
    
    # ...
```

有两种方式创建程序上下文，一种是自动创建，当请求进入时，程序上下文会随着请求上下文被创建。在 `RequestContext` 类中，程序上下文在请求上下文推入之前推入：

```python
class RequestContext(object):
    # ...
    def push(self):
        # ...
        # 在 push 请求上下文之前先 push 程序上下文
        app_ctx = _app_ctx_stack.top
        if app_ctx is None or app_ctx.app != self.app:
            app_ctx = self.app.app_context()
            app_ctx.push()
            self._implicit_app_ctx_stack.append(app_ctx)
        else:
            # ...
```

而在没有请求处理的时候，你就需要手动创建程序上下文。可以使用程序上下文对象的 `push()` 方法，也可以使用 `with` 语句。

`g` 只是一个普通的类字典对象，可以把它看作是 “增加了本地线程支持的全局变量”。有一个常见的疑问是，为什么说每次请求都会重置 `g`？这是因为 `g` 是保存在程序上下文中的，而程序上下文的生命周期是伴随着请求上下文产生和销毁的。每个请求会创建新的请求上下文，同样也会创建新的程序上下文，所以 `g` 会在每个新的请求中被重置。

#### 总结

Flask 的上下文有请求上下文（`RequestContext` 类的实例）和程序上下文（`AppContext` 类的实例）。请求上下文对象存储在请求上下文栈（`_request_ctx_stack`）中，程序上下文对象存储在程序上下文栈（`_app_ctx_stack`）中。而 `request`、`session` 则是保存在 `RequestContext` 中的变量，`current_app` 和 `g` 是保存在 `AppContext` 中的变量。

`request`、`session`、`current_app`、`g` 变量所指向的实例对象都有相应的类：

- `request`：`Request`
- `session`：`SecureCookieSession`
- `current_app`：`Flask`
- `g`：`_AppCtxGlobals`

再来看下为什么要有这一系列东西：

1. 需要保存请求相关的信息，于是有了请求上下文；
2. 为了更好地分离程序的状态，应用起来更加灵活，于是有了程序上下文；
3. 为了让上下文对象可以在全局访问，而不用显式地传入视图函数，同时确保线程安全，于是有了 `Local`（本地线程）；
4. 为了支持多个程序，于是有了 `LocalStack`；
5. 为了支持动态获取上下文对象，于是有了 `LocalProxy`

### 请求和响应对象

#### 请求对象

一个 HTTP 请求报文从客户端出发，它大致经过了这些变化：从 HTTP 请求报文到 WSGI 规定的 Python 字典，再到 Werkzeug 中的 `werkzeug.wrappers.Request` 对象，最后到 Flask 中我们熟悉的请求对象 `Request`。

从 `flask` 包中导入的 `request` 是代理，被代理的实际对象是请求上下文 `RequestContext` 对象的 `request` 属性，这个属性存储的是 `Request` 类实例，这个 `Request` 才是表示请求的请求对象，它定义在 `flask/wrappers.py` 中：

```python
from werkzeug.wrappers import Request as RequestBase

class JSONMixin(object):
    # 定义 is_json、json 属性和 get_json() 方法

class Request(RequestBase, JSONMixin):

    url_rule = None
    view_args = None
    routing_exception = None

    @property
    def max_content_length(self):
        """返回配置变量 MAX_CONTENT_LENGTH 的值。"""
        if current_app:
            return current_app.config['MAX_CONTENT_LENGTH']
        
    @property
    def endpoint(self):
        """与请求匹配的端点。"""
        if self.url_rule is not None:
            return self.url_rule.endpoint
    
    @property
    def blueprint(self):
        """当前蓝图的名称。"""
        if self.url_rule and '.' in self.url_rule.endpoint:
            return self.url_rule.endpoint.rsplit('.', 1)[0]
    
    # ...
```

Flask 的 `Request` 类继承 Werkzeug 提供的 `Request` 类（它又继承自好几个基础类）和提供 JSON 支持的 `JSONMixin` 类。请求对象 `request` 的大部分属性都直接继承 Werkzeug 中 `Request` 类的属性，比如 `method` 和 `args` 属性等。Flask 的 `Request` 类主要添加了一些 Flask 特有的属性，比如表示所在蓝图的 `blueprint` 属性，或是为了方便获取当前端点的 `endpoint` 属性等。

Flask 允许我们自定义请求类，通常情况下，我们会子类化这个 `Request` 类，并添加一些自定义的设置，然后把这个自定义的请求类赋值给程序实例的 `request_class` 属性。

#### 响应对象

响应对象是由 `finalize_request()` 方法生成的，它调用了 `flask.Flask.make_response()` 方法生成响应对象，传入的 `rv` 参数是 `dispatch_request()` 的返回值，也就是视图函数的返回值。

视图函数可以返回多种类型的返回值，完整的合法返回值如下：

|类型 |说明  |
|:---|:-----|
|response_class|如果返回值是响应类的实例，会被直接返回|
|str           |返回值为字符串，会作为响应的 body   |
|unicode       |返回值为 unicode 字符串，会被编码为 utf-8，然后作为响应的 body|
|a WSGI function|返回值为 WSGI 函数，会被作为 WSGI 程序调用并缓存（buffer）为响应对象|
|tuple          |返回值为元组，可以是两种形式：`(response, status, headers)` 或 `(response, headers)`。这里的 `response` 可以是上面任一形式，`status` 为状态码，`headers` 为 HTTP 头部字段的字典或列表|

这个 `Flask.make_response()` 方法的主要工作就是判断返回值是哪一种类型，然后根据类型做出相应处理，最后生成一个响应对象并返回该响应对象。响应对象为 `Response` 类的实例，`Response` 类定义在 `flask.wrappers.py` 中：

```python
from werkzeug.wrappers import Response as ResponseBase

class JSONMixin(object):
    # ...

class Response(ResponseBase, JSONMixin):
    default_mimetype = 'text/html'

    def _get_data_for_json(self, cache):
        return self.get_data()

    @property
    def max_cookie_size(self):
        """返回配置变量 MAX_COOKIE_SIZE 的值"""
        if current_app:
            return current_app.config['MAX_COOKIE_SIZE']
        # 上下文未被 push 时返回 Werkzeug 中 Response 类的默认值
        return super(Response, self).max_cookie_size
```

和 `Request` 类相似，这个响应对象继承 Werkzeug 的 `Response` 类和添加 JSON 支持的 `JSONMixin` 类。这个类比 `Request` 类更简单，只是设置了默认的 MIME 类型。

Flask 也允许自定义响应类，只需子类化 `Response` 类，然后将自定义类赋值给 `flask.Flask.response_class` 属性。

### session

向 `session` 中存储数据时，会生成加密的 cookie 加入响应中，当用户再次发起请求时，浏览器会自动在 HTTP 请求报文中加入这个 cookie 值。Flask 接收到请求会把名为 session 的 cookie 的值解析到 `session` 对象里，这时我们就可以再次从 `session` 中读取数据。

#### 操作 session

session 变量在 `globals` 模块中定义：

```python
session = LocalProxy(partial(_lookup_req_object, 'session'))
```

它会调用 `_lookup_req_object()` 函数，传入 `name` 参数的值为 `'session'`：

```python
def _lookup_req_object(name):
    top = _request_ctx_stack.top
    if top is None:
        raise RuntimeError(_request_ctx_err_msg)
    return getattr(top, name)
```

由上面的代码可以看出 `session` 就是请求上下文的一个属性，`session` 是在生成请求上下文时创建的。

之后会执行 `LocalProxy` 类的 `__setattr__()` 方法，它会将设置操作转交给真实的 session 对象：

```python
@implements_bool
class LocalProxy(object):
    # ...
    def __setitem__(self, key, value):
        self._get_current_object()[key] = value
```

而真实的 session 对象其实是 `sessions.py` 模块中的 `SecureCookieSession` 类的实例。而 `SecureCookieSession` 类继承自 `CallbackDict` 类和 `SessionMixin` 类，并添加了 `modified` 和 `accessed` 属性和一些方法。然后在 Werkzeug 中进行了一系列查询之后会决定是否调用 `on_update()` 方法，这个方法会将 `modufied` 和 `accessed` 属性设为 `True`，分别表示 session 是否被修改过和是否被读写过，这两个标志会在保存 session 时用到。那 Werkzeug 是如何知道是否要调动 `on_update()` 方法的呢？这得先了解 `CallbackDict` 类，它定义在 `werkzeug.datastructures` 模块中：

```python
class CallbackDict(UpdateDictMixin, dict):
    """一个字典，每当该字典发生变化时都会调用传入的函数。"""
    def __init__(self, initial=None, on_update=None):
        dict.__init__(self, initial or ())
        self.on_update = on_update
```

`CallbackDict` 类构造函数接受一个 `on_update` 参数，并将它传给了 `self.on_update` 属性。而 `SecureCookieSession` 类在构造函数中定义了一个 `on_update()` 函数，并将其传给了 `on_update` 参数：

```python
class SecureCookieSession(CallbackDict, SessionMixin):
    # ...
    def __init__(self, initial=None):
        def on_update(self):
            self.modified = True
            self.accessed = True

        super(SecureCookieSession, self).__init__(initial, on_update)

    # ...
```

为什么 `on_update()` 函数会自动调用，答案就在 `CallbackDict` 类的父类 `UpdateDictMixin` 里：

```python
class UpdateDictMixin(object):
    """当字典被修改的时候调用 `self.on_update` 。"""
    on_update = None

    def calls_update(name):
        def oncall(self, *args, **kw):
            rv = getattr(super(UpdateDictMixin, self), name)(*args, **kw)
            if self.on_update is not None:
                self.on_update(self)
            return rv
        oncall.__name__ = name
        return oncall
    
    def setdefault(self, key, default=None):
        # ...
    
    def pop(self, key, default=_missing):
        # ...

    __setitem__ = calls_update('__setitem__')
    __delitem__ = calls_update('__delitem__')
    clear = calls_update('clear')
    popitem = calls_update('popitem')
    update = calls_update('update')
    del calls_update
```

可以看到它重载了所有的字典操作（`setdefault`、`pop`、`__setitem__`、`__delitem__`、`clear`、`popitem`、`update`），并在这些操作中调用了 `on_update()` 函数。也就是说，一旦继承了 `CallbackDict` 类的对象进行了字典操作，就会执行 `on_update` 属性指向的函数。

我们在视图函数中对 `session` 执行写操作会触发这里的 `__setitem__` 方法，进而执行了 `calls_update('__setitem__')`，最后才得以调用 `SecureCookieSession` 类定义的 `on_update()` 函数。

Werkzeug 提供了许多有用的数据结构，比如 `ImmutableMultiDict`，这些数据结构都定义在 `werkzeug.datastructures` 模块中。

当我们对 `session` 进行写入和更新操作时，Flask 需要将新的 session 值写入到 cookie 中，这是如何做到的呢？首先，视图函数执行完毕后会返回到 `dispatch_request()` 方法中，而 `dispatch_request()` 方法执行完毕后会返回到 `full_dispatch_request()` 方法中。`full_dispatch_request()` 最后会调用 `finalize_request()` 方法来生成响应对象，并返回给 `Flask.wsgi_app()`。而 session 的更新就在 `finalize_request()` 方法中。`finalize_request()` 方法会调用 `Flask.process_response()` 方法来对响应对象进行预处理：

```python
class Flask(_PackageBoundObject):
    # ...
    def process_response(self, response):
        ctx = _request_ctx_stack.top
        # ...
        if not self.session_interface.is_null_session(ctx.session):
            self.session_interface.save_session(self, ctx.session, response)
        return response
```

从代码中可以看出，session 的操作使用到了中间变量 `self.session_interface`，它其实是 `SecureCookieSessionInterface` 类。Flask 用到很多这样的中间变量，比如请求类（`request_class`）和响应类（`response_class`），这是为了方便开发者自己定义这些类。

`process_response()` 方法首先会获得请求上下文对象，然后使用 `is_null_session()` 方法检测 `session` 是否是无效的，这个方法定义在 `SecureCookieSessionInterface` 继承的 `SessionInterface` 类中，它会判断 `session` 是否是 `NullSession` 类的实例。如果该 `session` 有效就会调用 `save_session()` 方法来保存 `session`，`save_session()` 方法的定义：

```python
class SecureCookieSessionInterface(SessionInterface):
    # ...
    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        path = self.get_cookie_path(app)

        # 如果 session 被修改为空，则删除该 cookie
        # 如果 session 为空，则直接返回
        if not session:
            if session.modified:
                response.delete_cookie(
                    app.session_cookie_name,
                    domain=domain,
                    path=path
                )

            return
        
        # 如果读或写过 session，则添加一个 Vary: Cookie 头部字段
        if session.accessed:
            response.vary.add('Cookie')

        # 检查是否需要设置 Cookie 头部，不需要则直接返回
        if not self.should_set_cookie(app, session):
            return

        httponly = self.get_cookie_httponly(app)
        secure = self.get_cookie_secure(app)
        samesite = self.get_cookie_samesite(app)
        expires = self.get_expiration_time(app, session)
        val = self.get_signing_serializer(app).dumps(dict(session))
        response.set_cookie(
            app.session_cookie_name,
            val,
            expires=expires,
            httponly=httponly,
            domain=domain,
            path=path,
            secure=secure,
            samesite=samesite
        )
```

在 `save_session()` 方法的最后对传入的响应对象调用了 `set_cookie()` 方法设置了 Cookie 头部，这个方法的定义在 `werkzeug.wrappers.BaseResponse` 类中，也就是 Flask 中的响应类的父类。

`set_cookie()` 方法接收的一系列参数都是通过 Flask 内置的配置键设置的，配置键如下：

|参数|配置变量|默认值|说明|
|:--|:------|:----|:--|
|key|'SESSION_COOKIE_NAME|`session`| Cookie 的名称（键）|
|expires|'PERMANENT_SESSION_LIFETIME'|`timedelta(days=31)`|过期时间|
|domain|'SESSION_COOKIE_DOMAIN'|`None`|Cookie 的域名（默认为当前域名）|
|path|'SESSION_COOKIE_PATH'|`None`|Cookie 的路径（默认为整个域）|
|httponly|'SESSION_COOKIE_HTTPONLY'|`True`|Cookie 是否设置 httplony，设置了则不允许用 JS 获取 Cookie|
|secure|'SESSION_COOKIE_SECURE'|`False`|Cookie 是否设置 secure，设置了则只允许以 HTTPS 的方式获取 Cookie|

在这些配置键中，'SESSION_COOKIE_NAME' 和 'PERMANENT_SESSION_LIFETIME' 也可以通过 `Flask` 类的属性来设置，分别是 `session_cookie_name` 和 `permanent_session_lifetime`。

其中，session Cookie 的值由下面这行代码生成：

```python
val = self.get_signing_serializer(app).dumps(dict(session))
```

签名的序列化器使用 `get_signing_serializer()` 方法生成，并传入了 `app` 对象来获取秘钥，`get_signing_serializer()` 方法的定义如下：

```python
class SecureCookieSessionInterface(SessionInterface):
    salt = 'cookie-session'   # 为计算增加随机性的 “盐”
    digest_method = staticmethod(hashlib.sha1)  # 用于计算签名的哈希函数，默认是 sha1
    key_derivation = 'hmac'   # itsdangerous 支持的秘钥衍生算法，默认是 hmac
    serializer = session_json_serializer   # 序列化器
    session_class = SecureCookieSession

    def get_signing_serializer(self, app):
        if not app.secret_key:
            return None
        signer_kwargs = dict(
            key_derivation=self.key_derivation,
            digest_method=self.digest_method
        )
        return URLSafeTimedSerializer(app.secret_key, salt=self.salt,
                                      serializer=self.serializer,
                                      signer_kwargs=signer_kwargs)
```

其中使用的序列化类是 `itsdangerous.URLSafeTimedSerializer` 类，这会创建一个具有过期时间且 URL 安全的 token 字符串。

最后，`session['answer'] = 42` 中的 `42` 会变成：

```jwt
eyJhbnN3ZXIiOjQyfQ.XFb53g.6yYZKZdYbZA8nAocAhy_W_huaF4
```

这个字符串的形式是 JSON Web Token 的形式，最后这个字符串会被存储到浏览器中名为 session 的 Cookie 中。

#### session 起源

`session` 在 `RequestContext` 类的 `push()` 方法中创建：

```python
class RequestContext(object):
    def __init__(self, app, environ, request=None):
        # ...
        self.session = None
        # ...
    # ...
    def push(self):
        # ...
        if self.session is None:
            session_interface = self.app.session_interface
            self.session = session_interface.open_session(
                self.app, self.request
            )

            if self.session is None:
                self.session = session_interface.make_null_session(self.app)
```

推送请求上下文的 `push()` 方法中调用了 `open_session()` 方法来创建 `session`，也就是说，一旦接收到请求，就会创建 `session` 对象。

`open_session()` 方法接收程序实例和请求对象作为参数，我们可以猜想，请求对象参数用于获取 Cookie 头部的值，而程序实例用于获取秘钥验证 session 是否合法。`open_session()` 方法定义在 `SecureCookieSessionInterface` 类里：

```python
class SecureCookieSessionInterface(SessionInterface):
    session_class = SecureCookieSession

    def open_session(self, app, request):
        s = self.get_signing_serializer(app)
        if s is None:
            return None
        val = request.cookies.get(app.session_cookie_name)
        if not val:
            return self.session_class()
        max_age = total_seconds(app.permanent_session_lifetime)
        try:
            data = s.loads(val, max_age=max_age)
            return self.session_class(data)
        except BadSignature:
            return self.session_class()
```

在这个方法里，如果请求的 Cookie 里包含 session 数据，就将数据解析到 `session` 对象里，否则就生成一个空的 session。这里要注意的是，如果没有设置秘钥，`open_session()` 就会返回 `None`，这时在 `push()` 方法里就会调用 `make_null_session()` 方法来生成一个无效的 session 对象（`NullSession` 类实例），对其执行字典操作会显示警告。

最终返回的 session 就是我们在视图函数里用的 `session` 对象所代理的真实对象，这就是 session 的整个生命轨迹。

签名可以确保 session Cookie 的内容不被篡改，但这并不意味着无法获取加密前的原始数据。事实上，session Cookie 的值可以被轻易地解析出来（即使不知道秘钥），这就是不能将敏感数据存放到 session 中的原因。使用 `itsdangerous` 解析 session：

```sh
>>> from itsdangerous import base64_decode
>>> s = 'eyJhbnN3ZXIiOjQyfQ.XFb53g.6yYZKZdYbZA8nAocAhy_W_huaF4'
>>> data, timestamp, secret = s.split('.')
>>> base64_decode(data)
b'{"answer":42}'
```

Flask 提供的 session 将用户回话存储在客户端，另一种实现用户回话的方式是在服务器端存储用户回话，而客户端只存储一个 session ID。当接收到客户端的请求时，可以根据 Cookie 中的 session ID 来找到对应的用户回话内容。这种方法更为安全和强健，你可以使用 [fengsp/flask-session](https://github.com/fengsp/flask-session) 来实现这种方式的 session。

### 蓝图

每个蓝图都是一个休眠的操作子集，只有注册到程序上才会获得生命。这种休眠状态是如何实现的呢？

`Blueprint` 类的大多数方法并不会直接执行逻辑代码，而是把函数作为参数传给 `Blueprint.record()` 方法或 `Blueprint.record_once()` 方法。`record()` 方法在 `blueprints.py` 模块中定义：

```python
class Blueprint(_PackageBoundObject):
    # ...
    def record(self, func):
        if self._got_registered_once and self.warn_on_modifications:
            from warnings import warn
            warn(Warning('The blueprint was already registered once '
                         'but is getting modified now.  These changes '
                         'will not show up.'))
        self.deferred_functions.append(func)
```

这个方法的主要作用是把传入的函数添加到 `self.deferred_functions` 属性中，它是一个存储所有延迟执行的函数的列表。

蓝图可以被注册多次，但并不代表蓝图里的其他函数可以被注册多次，为了避免重复写入 `deferred_functions` 列表，这些函数会使用 `record_once()` 方法来录入：

```python
class Blueprint(_PackageBoundObject):
    # ...
    def record_once(self, func):
        def wrapper(state):
            if state.first_registration:
                func(state)
        return self.record(update_wrapper(wrapper, func))
```

可以看到，`record_once()` 方法内调用了 `record()` 方法，并实现了一个 `wrapper` 函数，通过 `state` 对象的 `first_registration` 属性来判断蓝图是否是第一个注册，以决定是否将该函数加入到 `deferred_functions` 列表。`state` 对象是什么稍后会将。

注意，这里的 `update_wrapper` 是 Python 标准库 `functools` 模块提供的工具函数，用来更新封装函数（即 `wrapper`）。

蓝图中的视图函数及其他处理函数（回调函数）都会使用这种方法临时保存到 `deferred_functions` 列表中。可以猜想到，在注册蓝图时会依次执行这个列表里的函数。

在 Flask 中，我们使用 `Flask.register_blueprint()` 方法将蓝图注册到程序实例上，它的定义：

```python
class Flask(_PackageBoundObject):
    # ...
    @setupmethod
    def register_blueprint(self, blueprint, **options):
        first_registration = False

        if blueprint.name in self.blueprints:
            assert self.blueprints[blueprint.name] is blueprint, (
                'A name collision occurred between blueprints %r and %r. Both'
                ' share the same name "%s". Blueprints that are created on the'
                ' fly need unique names.' % (
                    blueprint, self.blueprints[blueprint.name], blueprint.name
                )
            )
        else:
            self.blueprints[blueprint.name] = blueprint
            self._blueprint_order.append(blueprint)
            first_registration = True

        blueprint.register(self, options, first_registration)
```

蓝图注册后，蓝图将保存在 `Flask` 类实例的 `blueprints` 属性中，它是一个存储蓝图名称与对应蓝图对象的字典。

`register_blueprint()` 方法会先检测要注册的蓝图名称是否已在 `self.blueprints` 属性中，如果已存在，则会再判断这两个蓝图是否是同一个蓝图；如果不存在，则会将该蓝图对象存进 `Flask.blueprints` 字典中，并将表示第一次注册的标志 `first_registration` 设为 `True`，最后调用蓝图对象 `Blueprint` 类的 `register()` 方法：

```python
class Blueprint(_PackageBoundObject):
    # ...
    def register(self, app, options, first_registration=False):
        self._got_registered_once = True
        state = self.make_setup_state(app, options, first_registration)

        if self.has_static_folder:
            state.add_url_rule(
                self.static_url_path + '/<path:filename>',
                view_func=self.send_static_file, endpoint='static'
            )

        for deferred in self.deferred_functions:
            deferred(state)
```

这里的 `register()` 方法会使用 `make_setup_state()` 方法创建一个 `state` 对象。根据传入的参数可知这个对象包含了蓝图的状态信息，比如是否是第一次注册。

最后迭代蓝图的 `self.deferred_functions` 列表并在执行列表里的函数时传入了这个 `state` 对象。

从 `make_setup_state()` 方法中可知这个 `state` 对象是 `BlueprintSetupState` 类的实例：

```python
class BlueprintSetupState(object):
    def __init__(self, blueprint, app, options, first_registration):
        self.app = app
        self.blueprint = blueprint
        self.options = options

        self.first_registration = first_registration

        subdomain = self.options.get('subdomain')
        if subdomain is None:
            subdomain = self.blueprint.subdomain
        self.subdomain = subdomain

        url_prefix = self.options.get('url_prefix')
        if url_prefix is None:
            url_prefix = self.blueprint.url_prefix
        self.url_prefix = url_prefix

        self.url_defaults = dict(self.blueprint.url_values_defaults)
        self.url_defaults.update(self.options.get('url_defaults', ()))

    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        if self.url_prefix is not None:
            if rule:
                rule = '/'.join((
                    self.url_prefix.rstrip('/'), rule.lstrip('/')))
            else:
                rule = self.url_prefix
        options.setdefault('subdomain', self.subdomain)
        if endpoint is None:
            endpoint = _endpoint_from_view_func(view_func)
        defaults = self.url_defaults
        if 'defaults' in options:
            defaults = dict(defaults, **options.pop('defaults'))
        self.app.add_url_rule(rule, '%s.%s' % (self.blueprint.name, endpoint),
                              view_func, defaults=defaults, **options)
```

除了定义存储蓝图信息的几个属性外，这个类还实现了 `add_url_rule()` 方法，它会在进行相关参数设置后调用程序实例上的 `Flask.add_url_rule()` 方法来添加 URL 规则。

### 模板渲染

在视图函数中，我们使用 `render_template()` 函数来渲染模板，传入模板名和需要注入模板的关键词参数。`render_template()` 函数的定义在 `flask/templating.py` 模块中：

```python
def render_template(template_name_or_list, **context):
    ctx = _app_ctx_stack.top
    ctx.app.update_template_context(context)
    return _render(ctx.app.jinja_env.get_or_select_template(template_name_or_list),
                   context, ctx.app)
```

这个函数先取得程序上下文，然后调用程序实例的 `Flask.update_template_context()` 方法更新模板上下文，定义如下：

```python
class Flask(_PackageBoundObject):
    # ...
    def update_template_context(self, context):
        # 获取全局的模板上下文处理函数
        funcs = self.template_context_processors[None]
        reqctx = _request_ctx_stack.top
        if reqctx is not None:
            bp = reqctx.request.blueprint
            if bp is not None and bp in self.template_context_processors:
                # 获取蓝图的上下文处理函数
                funcs = chain(funcs, self.template_context_processors[bp])
        orig_ctx = context.copy()
        for func in funcs:
            context.update(func())
         context.update(orig_ctx)
```

我们可以使用 `context_processor` 装饰器注册模板上下文处理函数，而注册的处理函数会被存储在 `Flask.template_context_processors` 字典里：

```python
self.template_context_processors = {
   None: [_default_template_ctx_processor]
}
```

字典的键是蓝图的名称，而全局的处理函数则使用 `None` 作为键，默认的处理函数是 `templating._default_template_ctx_processor()`，它把当前上下文的 `request`、`session` 和 `g` 注入到模板上下文。

而这个 `update_template_context()` 方法的主要工作就是调用这些模板上下文处理函数，获取返回的字典，然后统一添加到 `context` 字典。这里先复制原始的 `context` 字典，最后再将原始的字典合并到 `context` 字典中，这是为了确保最初设置的值不被覆盖，即视图函数中使用 `render_template()` 函数传入的上下文参数优先。

执行完 `update_template_context()` 函数后，`render_template()` 函数会用这个 `context` 字典调用 `_render()` 函数，并返回它。传入的第一个参数为 `ctx.app.jinja_env.get_or_select_template(template_name_or_list)`，这里对程序实例 `app` 调用的 `Flask.jinja_env()` 方法如下：

```python
class Flask(_PackageBoundObject):
    # ...
    @locked_cached_property
    def jinja_env(self):
        """用来加载模板的 Jinja2 环境（templating.Environment 类实例）。"""
        return self.create_jinja_environment()
```

这里的 `locked_cached_property` 装饰器定义在 `flask.helpers.locked_cached_property` 中，它的作用是将被装饰的函数转变为一个延迟函数，也就是它的返回值会在第一次获取后被缓存。同时为了线程安全添加了基于 RLock 的可重入线程锁。

`jinja_env()` 调用了 `Flask.create_jinja_environment()` 方法创建一个 Jinja2 环境（`templating.Environment` 类，继承自 `jinja2.Environment`），用于加载模板。这个方法完成了 Jinja2 环境在 Flask 中的初始化，向模板上下文添加了一些全局变量（如 `url_for()`、`get_flashed_message` 函数以及 `config` 对象等，更新了一些渲染设置，还添加了一个 `tojson` 过滤器，该方法定义如下：

```python
class Flask(_PackageBoundObject):
    # ...
    def create_jinja_environment(self):
        options = dict(self.jinja_options)

        if 'autoescape' not in options:   # 设置转义
            options['autoescape'] = self.select_jinja_autoescape

        if 'auto_reload' not in options:  # 设置自动重载选项
            options['auto_reload'] = self.templates_auto_reload
        rv = self.jinja_environment(self, **options)
        rv.globals.update(   # 添加多个全局对象
            url_for=url_for,
            get_flashed_messages=get_flashed_messages,
            config=self.config,
            request=request,
            session=session,
            g=g
        )
        rv.filters['tojson'] = json.tojson_filter  # 添加 tojson 过滤器
        return rv
```

最后调用的 `_render()` 函数如下：

```python
def _render(template, context, app):
    before_render_template.send(app, template=template, context=context)
    rv = template.render(context)
    template_rendered.send(app, template=template, context=context)
    return rv
```

这个函数调用了 Jinja2 的 `render()` 函数来渲染模板，并在渲染的前后发送相应的信号。而在调用 `_render()` 函数前，还经过了模板文件定位、加载、解析等。渲染工作结束后就会返回渲染好的 unicode 字符串，这个字符串就是最终的视图函数返回值，即响应的 body。
