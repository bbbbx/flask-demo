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
- Flask-Whooshee：集成 Whoosh，可以配置 `WHOOSHEE_MIN_STRING_LEN` 对搜索关键字的最小字符数进行限制，默认为 3。
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
- 后台管理系统应该拥有更多有用的功能，比如：
    - 用户行为分析
    - 网站访问分析
    - 内容过滤与关键词审核
    - 给用户推送系统消息
    - 给用户推送系统邮件
    - 编辑推荐内容
    - 网站固定内容编辑
    - 数据库在线操作
- i18n：[python-babel/babel](https://github.com/python-babel/babel)，不是编译 ES 6 的那个 babel
- 给 Flask 支持 i18n 和 l10n：[python-babel/flask-babel](https://github.com/python-babel/flask-babel)
- i18n：国际化，给网站提供多种不同的语言，需要开发者解决，翻译者解决不了
- l10n：本地化，将网站的语言转换为本地语言，只有翻译者可以解决，[https://wiki.mageia.org/en/What_is_i18n,_what_is_l10n](https://wiki.mageia.org/en/What_is_i18n,_what_is_l10n)
- [pytz](https://pythonhosted.org/pytz/)：时区数据库，tz 即为 timezone
- flask-cors：给 flask 支持 Cross Origin Resource Sharing，解决请求 API 时的跨域问题
- [webargs](https://webargs.readthedocs.io/en/latest/)：用于解析 HTTP 请求的 arguments
- [httpie](https://github.com/jakubroztocil/httpie)：命令行式的 HTTP 客户端，比 `curl` 简便
- 只需在 `<i>` 标签内写出图标的名词即可渲染出对应名称的图标，这种特性称为 **ligatures**，例如 `<i class="material-icons">face</i>`
- 另一个前端 framework：[Materialize](https://materializecss.com/)，基于 Material Design。
- 在以前，服务器端和客户端的 API 通信主要通过 RPC（Remote Procedure Call，远程过程调用）和 SOAP（Simple Object Access Protocol，简单对象访问协议）实现，但由于这些协议的规范过于严格，实现起来不够灵活，已经被逐渐抛弃。REST（Representational State Transfer，表现层状态转移）架构逐渐流行起来。为了方便理解，可以在 REST 前补全主语 Resource，即 Resouce REST，意思是 “资源（Resource）在网络中以某种表现形式（Representational）进行状态转移（State Transfer）。REST 不是规范，只是一种架构风格，设计 API 时不必完全按照 REST 的架构要求，要尽量从 API 自身特点和普适的规范来设计，而不是拘泥于 REST。

## 设计优美实用的 Web API

在设计 Web API 时有一个重要的考量：目标用户群，即 API 所面向的主要开发人员分类。是 LSUD（Large Set of Unknown Developers）还是 SSKD（Small Set of Known Developers）。

1. **使用 URL 定义资源。** 表示资源的 URL 也被称为端点或 API 端点。URL 的设计应遵循：
   1. 尽量保持简短易懂
   2. 避免暴露服务器架构
   3. 使用类似文件系统的层级结构。例如：
      1. `api.example.com/users`：所有用户
      2. `api.example.com/users/123/`：ID 为 123 的用户
      3. `api.example.com/users/123/posts`：ID 为 123 的用户的所有文章
      4. `api.example.com/posts/23/comments`：ID 为 23 的文章的所有评论
2. **使用 HTTP 方法描述操作。** 对资源的常见操作：创建、读取、更新、删除（CRUD），HTTP 方法与对应 URL 的关系：
    |URL|GET|PUT|PATCH|POST|DELETE|
    |:--|:--|:--|:----|:---|:-----|
    |资源集合，比如 `https://api.example.com/posts`|列出集合成员的所有信息|替换整个集合的资源|一般不使用|在集合中创建一个新条目，新条目的 URL 自动生成并包含在响应中返回|删除整个资源|
    |单个资源，比如 `https://api.example.com/posts/123`|获取指定资源的详细信息，采用 XML 或 JSON 等表现形式|替换指定的集合成员，如果不存在则创建|更新集合成员，仅提供更新的内容|一般不使用|删除指定的集合成员|

    每种方法应该返回的响应内容：

    |HTTP 方法|返回的响应|
    |:-------|:-------|
    |GET     |返回主体为目标资源的表现层，200（OK）响应|
    |POST    |返回指定数据新地址的表现层，头部的 `Location` 字段为指向资源的 URL，201（Greated）响应|
    |PUT     |若包含请求处理状态的表现出，则返回 200 响应；若空数据，则返回 204（No Content）响应|
    |PATCH   |同上  |
    |DELETE  |若请求被接收，但删除操作还未执行，则返回 202（Accept）响应；若删除操作已经执行，返回 204 响应；若删除操作已经执行，且返回包含状态信息的表现层，则返回 200 响应|

    HTTP 方法的详细定义和规则在 RFC 7231 中。

    **这里的表现层（repersentation）指的资源的表现形式，例如 JSON 格式的数据。**
3. **使用 JSON 交换数据。** JSON 已经取代了 XML 成为了 API 的标准数据格式，例如一篇文章可能会用下面的 JSON 数据表示：
    ```json
    {
        "id": 123,
        "url": "http://api.example.com/item/1",
        "html_url": "http://example.com/item/1",
        "title": "Hello Flask!",
        "body": "Something...",
        "created_at": "2019-01-27T15:44:05Z",
        "comments_url": "http://api.example.com/posts/123/comments",
        "author": {
            "id": 1,
            "url": "http://api.example.com/users/1",
            "html_url": "http://example.com/users/1",
            "username": "admin",
            "website": "http://example.com",
            "posts_url": "http://api.example.com/users/1/posts",
            "type": "Admin",
            "is_admin": true
        }
    }
    ```

    除了包含文章的基本内容（标题、正文）外，还应该添加指向其他相关资源的 URL（比如作者、评论等），这样 API 的使用者就可以自己探索其他资源了。
4. **设置 API 版本。** 当打算对 API 进行更新时，我们应该考虑到还有大量的用户使用的客户端依赖于旧版的 API。为此，我们需要保留旧版的 API，创建一个新版本。可以在 API 的 URL 中指定版本：
   - Version 1：`http://api.example.com/v1`
   - Version 2：`http://api.example.com/v2`

    或直接在子域中指定：
   - Version 1：`http://api.example.com`
   - Version 2：`http://api2.example.com`

## OAuth2

在传统的 Web 应用中，用户的认证信息存储在浏览器的 cookie 中，但 cookie 在其他客户端中是没有的，所以我们不能通过 cookie 来记住用户的状态。因为 API 的无状态特征，所以需要用户在每一次获取受登录保护的资源时都要提供认证信息，但每次都让用户附加认证信息并不合理。一个更好的方法是用户通过一次认证后，在服务器端为用户生成一个 token，在之后的请求中，客户端可以通过 token 进行认证。

OAuth（Open Authorization，开放授权）是一个 2007 年发布的授权标准，它是现代 Web API 中应用非常广泛的授权机制。

OAuth 允许用户授权第三方移动应用有限制地访问用户存储在其他服务器上的信息，而不需要将用户名和密码提供给第三方移动应用。除了这种认证类型之外，[OAuth2](https://oauth.net/2) 还提供了多种其他的认证类型：

|认证类型（Grant Type）|说明    |
|:-------------------|:-------|
|Authorization Code  |最常用，大多数在线服务都提供了这种认证类型的支持|
|Implicit            |同 Authorization Code 使用场景类似，但简化了认证过程，安全性也会有所降低|
|Resource Owner Password Credentials |直接使用用户名和密码登录，适用于可信的客户端，比如在线服务自己开发的官方客户端|
|Client Credentials  |不以用户为单位，而是通过客户端来认证，通常用于访问公开信息|

除了上面的认证类型，还有 SAML Bearer Assertion 认证和 JWT Bearer Token 认证，在 RFC 7522 中有详细定义，简化教程：[https://aaronparecki.com/oauth-2-simplified/](https://aaronparecki.com/oauth-2-simplified/)。

一般可以使用 `/oauth/token` 来作为 token 的端点，例如 `https://api.example.com/v1/oauth/token`。

**无论使用何种认证类型，都要使用 HTTPS 来防止信息在传输过程中被窃取，除非 API 不涉及会话信息，即任何人访问都获得相同的结果。**

使用密码认证类型时（也就是第三种），客户端在认证时需要以 `application/x-www-form-urlencoded` 的形式（也就是平时提交 HTML 表单时默认的类型）发送 POST 请求，并经过 UTF-8 编码后发送到服务器。提交的 key 和 value 如下：

|key          | value             |
|:------------|:------------------|
|`grant_type` | 必须为 `password`  |
|`username`   | 用户名（必填）      |
|`password`   | 密码（必填）        |
|`scope`      | 允许的权限范围（可选）|

比如，客户端发送的请求可能会是这样：

```http
POST /v1/oauth/token
Host: api.example.com
Content-Type: application/x-www-form-urlencoded

grant_type=password&username=venus&password=666666
```

如果不是开放的 API，还需要对客户端进行验证。可以使用 HTTP Basic 认证的方式将客户端 ID 和客户端密码进行 Base64 编码后存放在请求头部的 `Authorization` 字段中。在服务器端，Flask 将 Basic 认证信息解析在 `request.authorization` 中。认证 ID 存在 `request.authorization.name` 中，而认证密码存在 `request.authorization.password` 中。

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

Flask 提供了使用 Python 类来组织视图函数，其中 `MethodsView` 类可以让 Web API 的编写更加方便，并且让资源的表示更加直观：

```python
from flask.view import MethodView

class ItemAPI(MethodView):

    def get(self, item_id):
        pass
    
    def delete(self, item_id):
        pass


app.add_url_rule('/items/<int:item_id>', view_func=ItemAPI.as_view('item_api'), methods=['GET', 'DELETE'])
```

除了定义资源类，还需要使用 `add_url_rule()` 方法来注册路由，其中 `as_view()` 方法将资源类转换为视图函数，需要传入一个自定义的端点值（用来给 `url_for()` 生成 URL），并且需要在 `methods` 参数中传入在资源类中使用的方法。

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
