from flask import render_template
from sayhello import app

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', e=e), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html', e=e), 500
