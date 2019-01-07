import os
import uuid
from flask import Flask, render_template, session, redirect, url_for, flash, send_from_directory
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from flask_wtf.file import FileField, FileRequired, FileAllowed

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024  # 3 MB
app.config['UPLOAD_PATH'] = 'uploads'

class NameForm(FlaskForm):
    name = StringField('你的名字？', validators=[DataRequired()])
    submit = SubmitField('提交')

class UploadForm(FlaskForm):
    photo = FileField('上传文件', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    submit = SubmitField('提交')

def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()

    # 提交表单后，如果数据能被所有验证函数接受，
    # 那么validate_onsubmit() 方法的返回值为True，
    # 否则返回 False。
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('看来你修改了你的密码！')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        f = form.photo.data
        # filename = f.filename
        filename = random_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        flash('上传成功。')
        session['filename'] = [filename]
        return redirect(url_for('show_images'))
    return render_template('upload.html', form=form)

@app.route('/show_images')
def show_images():
    files = os.listdir(app.config['UPLOAD_PATH'])
    images = []
    for filename in files:
        images.append('/' + app.config['UPLOAD_PATH'] + '/' + filename)
    return render_template('show_images.html', images=images)

@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)
