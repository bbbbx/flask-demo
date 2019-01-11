# flask-demo

Flask 不是辣椒，是一个角状的容器，和 Bottle 有 PY 交易（同样是以容器命名的 Web 框架）。

## Flask 第三方扩展

- UI：flask-bootstrap（很久没更新了）、[greyli/bootstrap-flask](https://github.com/greyli/bootstrap-flask) 或者不使用这些 flask 扩展。
- 数据库：flask-sqlalchemy
- 邮件：flask-mail
    - 异步任务队列：Celery + Redis + RabbitMQ
- 表单：flask-wtf
    - 文件上传：flask-wtf 的 `FileField`、flask-uploads
    - 富文本编辑器：flask-CKEditor（谨防 XSS）
- 日期和时间：flask-moment
- HTML 模板引擎：Jinja2
- 环境变量：python-dotenv
- Python 环境：pipenv
- 在 Python 中嵌入 C：ctypes
- 生成测试假数据：[joke2k/faker](https://github.com/joke2k/faker)
- 调试工具：flask-debugtoolbar
- 用户认证：flask-login
- unidecode
- Web 服务器：uWSGI
- 代理服务器：Nginx
- 表格化导出 XLS、CSV、JSON、YAML 等格式：[kennethreitz/tablib](https://github.com/kennethreitz/tablib)

## 原型设计工具

- [Axure RP](https://www.axure.com/)
- [Mockplus](https://www.mockplus.cn/)
- [Sketch](https://www.sketchapp.com/)

## Flask 的一些概念

### 实例文件夹（instance folder）

为了方便存储开发和部署时的各类文件，Flask 提供了实例文件夹的支持。可以在项目根目录中创建一个名为 `instance` 的文件夹，在这个文件夹中存储开发或部署时使用的配置文件，包含敏感信息的文件，或是临时创建的数据库文库等。

```python
app = Flask(__name__, instance_relative=True)  # 告诉 Flask，配置文件的路径是相对于实例文件夹的。
app.config.from_object('config')      # 通用配置文件
app.config.from_pyfile('config.py')   # instance 文件夹下的配置文件
```

当使用 `flask run` 命令时，输出的信息会给出实例文件夹的合适位置。

除了使用实例文件夹配置之外，还可以使用环境变量优先的方式，即 `.env` > `.flaskenv`。
