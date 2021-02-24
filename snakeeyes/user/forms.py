from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Optional
from wtforms_components import EmailField, Email
from snakeeyes.user.models import User


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(min=5, max=35, message="Your password must be 8-32 character long")])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=32)])
    remember_me = BooleanField('Keep me signed in.')


class RegisterForm(Form):
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(min=5, max=35)])
    password = PasswordField('Password', validators=[DataRequired(), 
                                            Length(min=8, max=32, message="Your password must be 8-32 character long")])
    confirm_password = PasswordField("Confirm password", validators=[DataRequired(), 
                        Length(min=8, max=32, message="Your password must be 8-32 character long"), EqualTo('password', message='Your input must match the password field.')])

    def validate_email(self, email):
        user= User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already taken")


class WelcomeForm(Form):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=24, message='Username must be 4-24 character long')])

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already taken by another user, please choose another username. Thanks")


class RequestPasswordResetForm(Form):
    email = EmailField("Email", validators=[DataRequired(), Email(), Length(min=5, max=35)])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("There's no user with these email, sign up to create an account.")


class NewPasswordForm(Form):
    password = PasswordField('Enter a new password', validators=[DataRequired(), Length(min=8, max=32, message="Your password must be 8-32 character long")])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), Length(min=8, max=32), EqualTo('password', message='Your input must match the password field.')])


class UpdateAccountForm(Form):
    email = EmailField("Email", validators=[DataRequired(), Email(), Length(min=5, max=35)])
    password = PasswordField('Password', validators=[Optional(), 
                                            Length(min=8, max=32, message="Your password must be 8-32 character long")])
    confirm_password = PasswordField("Confirm password", validators=[Optional(), 
                                            Length(min=8, max=32, message="Your password must be 8-32 character long"), EqualTo(password, message='Your input must match the password field.')])

    def validate_username(self, email):
        user = User.query.filter_by(username=email.data).first()
        if user:
            raise ValidationError("Email already taken by another user, please choose another username. Thanks")


class PasswordForm(Form):
    email = EmailField("Email", validators=[DataRequired(), Email(), Length(min=5, max=35)])
            
















