from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RoleForm(FlaskForm):
    choice = RadioField(
        'Role', choices=[('reader', 'Reader'), ('blogger', 'Blogger')])
    submit = SubmitField('Proceed')


class SignupForm(FlaskForm):
    user_name = StringField('Username', validators=[DataRequired()])
    user_email = EmailField('Email address', validators=[DataRequired(), Email()])
    user_address = StringField('Address', validators=[DataRequired()])
    user_mobile = IntegerField('Mobile', validators=[DataRequired(), Length(10)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign up')

