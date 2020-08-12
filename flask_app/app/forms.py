from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms import StringField, PasswordField, BooleanField
from wtforms import TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class SignupForm(FlaskForm):
    user_name = StringField("Username", validators=[DataRequired()])
    user_email = EmailField("Email address", validators=[DataRequired(), Email()])
    user_address = StringField("Address", validators=[DataRequired()])
    user_mobile = IntegerField("Mobile", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign up")


class BlogForm(FlaskForm):
    blog_title = StringField("Title", validators=[DataRequired()])
    blog_type = StringField("Blog type", validators=[DataRequired()])
    blog_desc = TextAreaField("Blog description", validators=[DataRequired()])
    blog_content = TextAreaField("Blog content", validators=[DataRequired()])
    submit = SubmitField("Create")


class UpdateForm(FlaskForm):
    blog_title = StringField("Title")
    blog_type = StringField("Blog type")
    blog_desc = TextAreaField("Blog description")
    blog_content = TextAreaField("Blog content")
    submit = SubmitField("update")
