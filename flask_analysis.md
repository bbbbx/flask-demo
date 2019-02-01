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

这里引入了两个对象：`url_map` 和 `view_functions`。`url_map` 是 Werkzeug 的 `Map` 类实例（`werkzeug.routing.Map`），它存储了 URL 规则和相关的配置，而 `rule` 是 `Rule` 类实例（`werkzeug.routing.Rule`），其中保存了端点和 URL 规则的映射关系。

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

Flask 提供了 2 种上下文：请求上下和程序上下文。这 2 种上下文分别包含 `request`、`session`、`current_app` 和 `g` 这 4 个变量，这些变量是实际对象的本地代理（local proxy），因此这些变量被称为本地上下文（context locals）。这些代理对象定义在 `global.py` 模块中，该模块还包含了和上下文相关的 2 个错误信息和 3 个函数：

### 请求和响应对象

### session

### 蓝图

### 模板渲染
