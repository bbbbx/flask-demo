from wtforms import TextAreaField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import Optional, Length

class DescriptionForm(FlaskForm):
    description = TextAreaField('描述', validators=[Optional(), Length(0, 500)])
    submit = SubmitField('确定')
