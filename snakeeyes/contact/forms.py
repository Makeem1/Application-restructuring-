from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, 
from wtforms.validators import InputRequired, Length
from wtforms_components import EmailField


class ContactForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired, ])
    message =  StringField("Message", validators=[InputRequired, Length(min=10, max=1800) ])
    submit = SubmitField("Send")
 
