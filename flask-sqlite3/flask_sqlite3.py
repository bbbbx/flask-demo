import sqlite3
from flask import current_app, _app_ctx_stack

class SQLite3(object):
    def __init__(self, app=None):
        self.app = app
        # 如果有提供 app 参数，就调用 init_app(app)
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        # 设置默认配置变量
        app.config.setdefault('SQLITE3_DATABASE', ':memory:')
        # 挂载一个 teardown handler
        app.teardown_appcontext(self.teardown)

    def connect(self):
        # 打开一个 database connection，并返回该 connection。
        return sqlite3.connect(current_app.config['SQLITE3_DATABASE'])

    def teardown(self, exception):
        ctx = _app_ctx_stack.top
        # 每次弹出 app context 的时候，
        # 都会自动关闭该 app context 的 database connection
        if hasattr(ctx, 'sqlite3_db'):
            ctx.sqlite3_db.close()

    @property
    def connection(self):
        ctx = _app_ctx_stack
        if ctx is not None:
            # 若是首次打开 database connection，
            # 则存储该 connection 在 context 的属性上。
            if not hasattr(ctx, 'sqlite3_db'):
                ctx.sqlite3_db = self.connect()
            # 返回 context 的属性
            return ctx.sqlite3_db
