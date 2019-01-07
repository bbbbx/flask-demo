import click
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>hello world</h1>'

@app.route('/hello/<name>')
def greet(name):
    return 'hello %s!' % name

@app.cli.command()
def hello():
    click.echo('Hello, Human!')
