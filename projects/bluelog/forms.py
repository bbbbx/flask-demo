from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError, Email, Optional, URL
from flask_ckeditor import CKEditorField
from bluelog.models import Category

class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('密码', validators=[DataRequired(), Length(8, 128)])
    remeber = BooleanField('记住我？')
    submit = SubmitField('登录')

class PostForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired(), Length(1, 60)])
    body = CKEditorField('正文', validators=[DataRequired()])
    category = SelectField('分类', coerce=int, default=1)
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        # SelectField 的 choices 属性必须是一个二元素元组的列表，
        # 分别对应 option 的 value 和 name 值。
        self.category.choices = [(category.id, category.name) for category in Category.query.order_by(Category.name).all()]

class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField()

    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('Name already in use.')

class CommentForm(FlaskForm):
    author = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 254)])
    site = StringField('Site', validators=[Optional(), URL(), Length(1, 254)])
    body = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField()

class AdminCommentForm(CommentForm):
    author = HiddenField()
    email = HiddenField()
    site = HiddenField()
