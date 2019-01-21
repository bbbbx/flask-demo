from wtforms import StringField, SubmitField, TextAreaField, HiddenField, PasswordField
from wtforms.validators import DataRequired, Length, Email, Regexp, Optional, ValidationError, EqualTo
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_login import current_user
from albumy.models import User

class EditProfileForm(FlaskForm):
    name = StringField('姓名', validators=[DataRequired(), Length(1, 30)])
    username = StringField('用户名', validators=[DataRequired(), Length(1, 20), Regexp('^[a-zA-Z0-9]*$', message='用户名只能是字母或数字。')])
    website = StringField('个人网站', validators=[Optional(), Length(0, 254)])
    location = StringField('城市', validators=[Optional(), Length(0, 50)])
    bio = TextAreaField('简介', validators=[Optional(), Length(0, 120)])
    submit = SubmitField('确定')

    def validate_username(self, field):
        if field.data != current_user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在！')

class UploadAvatarForm(FlaskForm):
    image = FileField('头像（<= 3M）', validators=[FileRequired(), FileAllowed(['jpg', 'png'], '文件格式必须为 .png 或 .jpg')])
    submit = SubmitField('确定')

class CropAvatarForm(FlaskForm):
    x = HiddenField()
    y = HiddenField()
    h = HiddenField()
    w = HiddenField()
    submit = SubmitField('裁剪并上传')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('旧密码', validators=[DataRequired()])
    new_password = PasswordField('新密码', validators=[DataRequired(), Length(8, 128)])
    new_password_confirm = PasswordField('确认新密码', validators=[DataRequired(), Length(8, 128), EqualTo('new_password')])
    submit = SubmitField('确定')
