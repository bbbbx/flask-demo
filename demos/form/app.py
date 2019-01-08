import os
import uuid
from flask import Flask, request, render_template, session, redirect, url_for, flash, send_from_directory
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_ckeditor import CKEditor, CKEditorField, upload_fail, upload_success

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB
app.config['UPLOAD_PATH'] = 'uploads'
app.config['CKEDITOR_LANGUAGE'] = 'zh-CN'
app.config['CKEDITOR_FILE_UPLOADER'] = 'edit_uploader'

bootstrap = Bootstrap(app)
ckeditor = CKEditor(app)

class NameForm(FlaskForm):
    name = StringField('你的名字？', validators=[DataRequired()])
    submit = SubmitField('提交')

class UploadForm(FlaskForm):
    photo = FileField('上传文件', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    submit = SubmitField('提交')

class PostForm(FlaskForm):
    title = StringField('标题')
    body = CKEditorField('正文')
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
    filename = os.path.join(app.config['UPLOAD_PATH'], 'database.txt')
    database = ''
    with open(filename, 'r') as f:
        for line in f.readlines():
            database += line
    return render_template('index.html', form=form, name=session.get('name'), database=database)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        f = form.photo.data
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

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    form = PostForm()
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        # 防 XSS
        body = body.replace('<script>*.</script>', '').body.replace('javascript:', '')
        
        # 保存 title 和 body ...
        filename = os.path.join(app.config['UPLOAD_PATH'], 'database.txt')
        with open(filename, 'a') as f:
            f.write(title + '|' + body + '\n')
        flash('发表成功！')
        form.title.data = ''
        form.body.data = ''
    return render_template('edit.html', form=form)

@app.route('/edit_upload', methods=['POST'])
def edit_uploader():
    f = request.files.get('upload')
    ext = os.path.splitext(f.filename)[1]
    if ext not in ['jpg', 'png', 'jpeg']:
        upload_fail(message='上传失败！')
    filename = random_filename(f.filename)
    f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    url = url_for('get_file', filename=filename)
    return upload_success(url=url)
