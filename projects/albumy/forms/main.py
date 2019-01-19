from wtforms import TextAreaField, SubmitField, StringField
from flask_wtf import FlaskForm
from wtforms.validators import Optional, Length, DataRequired

class DescriptionForm(FlaskForm):
    description = TextAreaField('描述', validators=[Optional(), Length(0, 500)])
    submit = SubmitField('确定')

class TagForm(FlaskForm):
    tag = StringField('添加标签（多个标签使用空格隔开）', validators=[Optional(), Length(0, 64)])
    submit = SubmitField('确定')

class CommentForm(FlaskForm):
    body = TextAreaField('', validators=[DataRequired()])
    submit = SubmitField('发表评论')
