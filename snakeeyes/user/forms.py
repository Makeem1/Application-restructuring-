from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(min=5, max=35)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=32)])
    remember_me = BooleanField('Keep me signed in.')


class RegisterForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(min=5, max=35)])
    password = PasswordField('Password', validators=[DataRequired(), 
                                            Length(min=8, max=32, message="Your password must be 8-32 character long")])
    confirm_password = PasswordField("Confirm password", validators=[DataRequired(), 
                                            Length(min=8, max=32, message="Your password must be 8-32 character long"), EqualTo(password, message='Your input must match the password field.')])













