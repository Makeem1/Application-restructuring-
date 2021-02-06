from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms_components import EmailField


class ContactForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    message =  StringField("Message", validators=[DataRequired(), Length(min=10, max=1800) ])
    submit = SubmitField("Send")
 
