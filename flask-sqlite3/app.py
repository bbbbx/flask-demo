from flask import Flask
from flask_sqlite3 import SQLite3

app = Flask(__name__)
db = SQLite3()
db.init_app(app)

@app.route('/')
def show_all():
    cur = db.connection.cursor()
    # cur.execute('...')
    return 'Hello'
