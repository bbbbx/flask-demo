# flask-demo

Flask 不是辣椒，是一个角状的容器，和 Bottle 有 PY 交易（同样是以容器命名的 Web 框架）。

## Flask 第三方扩展

- UI：flask-bootstrap（很久没更新了）、[greyli/bootstrap-flask](https://github.com/greyli/bootstrap-flask) 或者不使用 Bootstrap。
    - Bootstrap 主题：[startbootstrap](https://startbootstrap.com/)、[bootswatch](https://bootswatch.com/)
- 数据库 ORM：flask-sqlalchemy
- 邮件：flask-mail
    - 异步任务队列：Celery + Redis + RabbitMQ（启动 Celery `celery worker -A bluelog.celery_worker.celery --loglevel=info -E` 记得先导入环境变量）
- 表单：flask-wtf
    - 使用隐藏字段 `<input type="hidden" name="csrf_token" value="xxxxxxx">`，带上一个 token 给服务器校验，防止 CSRF
    - 文件上传：flask-wtf 的 `FileField`、flask-uploads
    - 富文本编辑器：flask-CKEditor（谨防 XSS）
- 日期和时间：flask-moment
- HTML 模板引擎：Jinja2
- 环境变量：python-dotenv
- Python 环境：pipenv
- 在 Python 中嵌入 C：ctypes
- 生成测试假数据：[joke2k/faker](https://github.com/joke2k/faker)
- 调试工具：flask-debugtoolbar
- 管理用户认证（根据用户的身份开放不同的功能）：flask-login，Flask-Login 要求表示用户的模型类必须实现下列的这几个属性或方法，以便用来判断用户的认证状态：
    - `is_authenticated`：如果用户已通过认证，则返回 `True`
    - `is_active`：是否允许该用户登录
    - `is_anonymous`：如果当前用户未登录，则返回 `True`
    - `get_id()`：以 Unicode 形式返回用户的唯一标识符
- 将数据序列化为字符串：[pallets/itsdangerous](https://github.com/pallets/itsdangerous)，可用于将用户 ID 生成 token 来传输。
- 生成 slug（将标题转换为音译，可读性好，对搜索引擎和用户友好）：avian/unidecode
- Web 服务器：uWSGI
- 代理服务器：Nginx
- 表格化导出 XLS、CSV、JSON、YAML 等格式：[kennethreitz/tablib](https://github.com/kennethreitz/tablib)
    - 前端纯 JS 操作 Excel 文件：xlsx.js
- 拷贝到剪切板：cliboard.js
- 常用的计算散列值的 Python 库有 [PassLib](https://bitbucket.org/ecollins/passlib)、[bcrybt](https://github.com/pyca/bcrypt)
    - Werkzeug 在 `security` 模块中提供了一个 `generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)` 函数用于生成散列值，`check_password_hash(pwhash, password)` 函数用来检查密码散列值与密码是否对应。
- Exception 追踪：[Sentry](https://sentry.io/welcome/)
- Flask-Avatars：生成头像
- [Whoosh](https://bitbucket.org/mchaput/whoosh)：数据库搜索引擎，Python 写的。全文搜索的原理是对每个词建立一个索引，指明该词在数据库中出现的次数和位置，当用户查询时，检索程序通过索引进行查找，并返回匹配的数据。
- Flask-Whooshee：集成 Whoosh
- [Flask-Dropzone](https://github.com/greyli/flask-dropzone)：使用 Dropzone.js 在 Flask 应用中上传文件
- 占位图片：
    - 基于 Unsplash 的 [Lorem Picsum](http://picsum.photos/)
    - 使用 Pillow 生成图片：
        ```python
        >>> from PIL import Image
        >>> import random
        >>> r = lambda: random.randint(128, 255)
        >>> img = Image.new(mode='RGB', size=(800, 800), color=(r(), r(), r()))
        >>> img.save(the_desctination_path)  # 或是调用 img.show() 直接显示图片
        ```
- 开源的图标集：[Font Awesome](https://fontawesome.com/)、[Material Design Icons](https://material.io/icons)、[Octicons](https://octicons.github.com/)、和 Bootstrap 集成良好的 [Iconic](https://useiconic.com/open)
- 查看 SQLite 的 ER 图：[Alexis-benoist/eralchemy](https://github.com/Alexis-benoist/eralchemy)
- [Identicon](https://zh.wikipedia.org/wiki/Identicon)：一种基于用户信息的散列值，可用作默认头像
- 使用轮询（`setInterval` 每 30 秒发送一个 Ajax）模拟服务器推送比较简单，但存在较大的缺陷。如轮询时间间隔过长会有一定的延迟，太短又会增加服务器负担。长轮询可以解决这个问题，但在实现上比较复杂。我们也可以使用 Server-sent Events（SSE，服务器推送事件）来实现真正的服务器端推送，具体实现上可以考虑使用 [singingwolfboy/flask-sse](https://github.com/singingwolfboy/flask-sse)，还可以使用更完善和强大的双向通信协议 WebSocket 来实现实时更新。
- 图片裁剪：Jquery 插件 [content/Jcrop](http://deepliquid.com/content/Jcrop.html)。另一个裁剪库[Jcrop](https://github.com/tapmodo/Jcrop)
- 用户自定义头像流程：
    1. 用户上传图片文件；
    2. 上传完成后图片会显示在裁剪窗口；
    3. 用户裁剪图片时可以在裁剪窗口右侧看到预览；
    4. 用户单击 “保存” 按钮；
    5. 程序保存裁剪后的图片并更新头像。
    
    所以，一共上传两张图片，一张用户上传的原图片，一张用户裁剪后的图片。
- `<form>` 上传文件时，需要将 `enctype` 编码类型 attribute 设为 `multipart/form-data`。
- 注销用户的处理方式一般有下面 3 种：
    1. 临时屏蔽用户信息。通过给 User Model 设置一个字段来判断用户是否已注销，使用占位信息显示已注销用户的个人信息和头像等，保留图片和评论等数据。用户可以登录重新激活账户。
    2. 临时屏蔽用户信息，如果一定时间后用户没有激活账户，则直接删除用户的所有数据。
    3. 直接删除用户的相关信息。在真实中一般不使用这种方法。
- 在大多数情况下，联结（join）查询比子查询的性能要好。

## 原型设计工具

- [Axure RP](https://www.axure.com/)
- [Mockplus](https://www.mockplus.cn/)
- [Sketch](https://www.sketchapp.com/)

## Flask 的一些概念

### 实例文件夹（instance folder）

为了方便存储开发和部署时的各类文件，Flask 提供了实例文件夹的支持。可以在项目根目录中创建一个名为 `instance` 的文件夹，在这个文件夹中存储开发或部署时使用的配置文件，包含敏感信息的文件，或是临时创建的数据库文库等。

```python
app = Flask(__name__, instance_relative=True)  # 告诉 Flask，配置文件的路径是相对于实例文件夹的。
app.config.from_object('config')               # 通用配置文件
app.config.from_pyfile('config.py')            # instance 文件夹下的配置文件
```

当使用 `flask run` 命令时，输出的信息会给出实例文件夹的合适位置。

除了使用实例文件夹配置之外，还可以使用环境变量优先的方式，即 `.env` > `.flaskenv`。还可以使用类来组织配置，即自己定义一个配置类，然后调用 `app.config.from_object()` 方法。

### 端点（endpoint）

端点是 URL 规则和视图函数之间的桥梁，使用 `url_for(endpoint， **values)` 函数可以对指定的端点生成对应的 URL。

可以使用 `app.route(rule)` 来将视图函数注册为路由，或使用 `app.add_url_rule(rule, endpoint, view_function)`。

```python
@app.route('/hello')
def say_hello():
    return 'Hello!'

app.add_url_rule('/hello', 'say_hello', say_hello)
```

在路由里，URL 规则和视图函数并不是直接映射的，而是通过端口作为中间媒介，类似：

```
+-------------------+     +-----------------+     +---------------------+
| /hello（URL 规则） | --> | say_hello（端点） | --> | say_hello（视图函数） |
+-------------------+     +-----------------+     +---------------------+
```

端点名默认是视图函数名，可以使用 `flask routes` 命令来查看当前程序注册的所有路由：

```bash
$ flask routes
Endpoint     Methods  Rule
-----------  -------  -----------------------
auth.login   GET      /auth/login
auth.logout  GET      /auth/logout
static       GET      /static/<path:filename>
```

上面的输出中，端点不再仅仅是视图函数名，而是 “蓝图名.视图函数名”（中间有一点），**使用端口可以实现蓝图的视图函数命名空间**。

### 视图函数（view function）

```python
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)
```

其中的 `hello` 函数就是一个视图函数， **业务逻辑（business logic）** 的处理都应该在视图函数中处理，例如对数据库的 CURD、向任务队列（如 Celery）发起异步任务 等等。而 **展示逻辑（display logic）** 的处理应该在 HTML 模板（Jinja2）中处理。

当你在 JS 中插入了太多了 jinja2 语法时，或许这时你考虑将程序转变为 Web API，然后专心用 JS 来写客户端。

### 蓝图（blueprint）

当某个模块包含太多代码时，常见的做法是将单一模块升级为包，然后把源模块的内容分离成多个模块。例如将包含视图函数的的 `views.py` 转为 `blueprints` 子包。

使用蓝图不仅仅是对视图函数分类，而是将程序某一部分的所有操作组织在一起。一个蓝图实例以及一系列注册在蓝图实例上的操作的集合被称为一个蓝图。

例如，为了让移动设备拥有更好的体验，可以为移动设备创建一个单独的视图函数，这部分视图函数可以使用单独的 `mobile` 蓝图注册。

蓝图对象可以使用的所有方法及属性：[http://flask.pocoo.org/docs/latest/api/#blueprint-objects](http://flask.pocoo.org/docs/latest/api/#blueprint-objects)

### 上下文（Context）

有 app context、request context、template context、shell context。

## 其他

### 什么是 slug？

音译，即将中文转变为拼音。如将 “举个例子” 转为 “ju-ge-li-zi”，这样对用户和搜索引擎都友好，而不是将 ID 作为 URL。

### 什么是 Role-Based Access Control?

通常大型程序需要多个用户角色：拥有最高权限的管理员、负责管理内容的协管员、使用网站提供服务的普通用户、被临时封禁的用户等。各类用户所能进行的操作不能完全相同，在计算机安全领域，这种管理方法称为 RBAC（Role-Based Access Control，基于角色的权限控制）。
