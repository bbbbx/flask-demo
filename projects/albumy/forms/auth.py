from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, DataRequired, Length, Regexp, EqualTo, ValidationError
from albumy.models import User

class RegisterForm(FlaskForm):
    name = StringField('姓名', validators=[DataRequired(), Length(1, 30)])
    email = StringField('邮箱', validators=[DataRequired(), Email(), Length(1, 64)])
    username = StringField('用户名', validators=[DataRequired(), Length(1, 20), Regexp('^[a-zA-Z0-9]*$', message='用户名必须只包含英文字母或数字')])
    password = PasswordField('密码', validators=[DataRequired(), Length(8, 128)])
    password_confirm = PasswordField('确认密码', validators=[DataRequired(), Length(8, 128), EqualTo('password')])
    submit = SubmitField()

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已使用。')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已使用。')
