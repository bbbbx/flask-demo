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


## Flask 与 WSGI


## Flask 的工作流程与机制

