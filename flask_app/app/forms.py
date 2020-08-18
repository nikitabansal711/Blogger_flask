from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms import StringField, PasswordField, BooleanField
from wtforms import TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from .models import User


def validate_username(form, field):
    user = User.query.filter_by(user_name=field.data)
    if user:
        raise ValidationError('Please try another username')


class LoginForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(message="Enter Your Name Please")]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(message="Enter Your password Please")]
    )
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class SignupForm(FlaskForm):
    user_name = StringField(
        "Username", validators=[DataRequired(message="Enter Your Name Please"),
                                validate_username]
    )
    user_email = EmailField(
        "Email address",
        validators=[DataRequired(message="Enter Your Email Please"), Email()],
    )
    user_address = StringField(
        "Address", validators=[DataRequired(message="Enter Your address Please")]
    )
    user_mobile = StringField(
        "Mobile",
        validators=[
            DataRequired(message="Enter Your Mobile number Please"),
            Length(min=10, max=10, message="Enter 10 digit phone number"),
        ],
    )
    password = PasswordField(
        "Password", validators=[DataRequired(message="Enter Your Password Please")]
    )
    submit = SubmitField("Sign up")


class BlogForm(FlaskForm):
    blog_title = StringField(
        "Title", validators=[DataRequired(message="Title can't be empty!")]
    )
    blog_type = StringField(
        "Blog type", validators=[DataRequired(message="Type can't be empty!")]
    )
    blog_desc = TextAreaField(
        "Blog description",
        validators=[DataRequired(message="Provide description please!")],
    )
    blog_content = TextAreaField(
        "Blog content", validators=[DataRequired(message="Content can't be empty!")]
    )
    submit = SubmitField("Create")


class UpdateForm(FlaskForm):
    blog_title = StringField(
        "Title", validators=[DataRequired(message="Title can't be empty!")]
    )
    blog_type = StringField(
        "Blog type", validators=[DataRequired(message="Type can't be empty!")]
    )
    blog_desc = TextAreaField(
        "Blog description",
        validators=[DataRequired(message="Provide description please!")],
    )
    blog_content = TextAreaField(
        "Blog content", validators=[DataRequired(message="Content can't be empty!")]
    )
    submit = SubmitField("update")
