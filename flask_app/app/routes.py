# comprises of all the routes required in the project
import uuid

from app import app, db
from app.forms import LoginForm, SignupForm, BlogForm, UpdateForm
from flask import render_template, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash

from .models import User, Blog
from app.config import logger


@app.route("/", methods=["post", "get"])
def home():
    """Home page"""
    return render_template("home.html")


@app.route("/login", methods=["post", "get"])
def login():
    """api for login"""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_name=form.username.data).first()
        if not user:
            flash("Wrong credentials provided!")
        if check_password_hash(user.password, form.password.data):
            session["username"] = user.user_name
            session["user_id"] = user.user_id
            session["user_email"] = user.user_email
            session["user_mobile"] = user.user_mobile
            return redirect(url_for("dashboard"))

        flash("Wrong credentials provided!")

    return render_template("login.html", title="Sign In", form=form)


@app.route("/signup", methods=["post", "get"])
def signup():
    """api for signup"""
    try:
        form = SignupForm()
        if form.validate_on_submit():
            hashed_password = generate_password_hash(
                form.password.data, method="sha256")
            new_user = User(
                public_id=str(uuid.uuid4()),
                user_name=form.user_name.data,
                user_email=form.user_email.data,
                user_address=form.user_address.data,
                user_mobile=form.user_mobile.data,
                password=hashed_password,
            )
            db.session.add(new_user)
            db.session.commit()
            flash("New user created with username {}".format(
                new_user.user_name))
        return render_template("signup.html", title="Sign In", form=form)
    except (Exception, TypeError)as e:
        logger.info(e)


@app.route("/dashboard", methods=["post", "get"])
def dashboard():
    """takes the user to dashboard"""
    if not session.get("user_id") is None:
        form = BlogForm()
        user = session.get("username")
        if form.validate_on_submit():
            new_blog = Blog(
                blog_title=form.blog_title.data,
                blog_type=form.blog_type.data,
                blog_desc=form.blog_desc.data,
                blog_content=form.blog_content.data,
                blog_user_id=user["user_id"],
            )
            db.session.add(new_blog)
            db.session.commit()
            flash("New blog created with title {}".format(new_blog.blog_title))

        return render_template("dashboard.html", form=form, user=user)
    else:
        return redirect(url_for("page_error"))


@app.route("/log_out", methods=["post", "get"])
def log_out():
    """enables user to log out"""
    session.pop("user_id", None)
    return redirect(url_for("home"))


@app.route("/show_my_blogs", methods=["post", "get"])
def show_my_blogs():
    """for listing all the blogs of current user only"""
    if not session.get("user_id") is None:
        user_id = session.get("user_id")
        user = session.get("username")
        blogs = Blog.query.filter_by(blog_user_id=user_id).all()
        output = []
        for blog in blogs:
            blog_data = {}
            blog_data["blog_id"] = blog.blog_id
            blog_data["blog_title"] = blog.blog_title
            blog_data["blog_type"] = blog.blog_type
            blog_data["blog_content"] = blog.blog_content
            blog_data["blog_desc"] = blog.blog_desc
            output.append(blog_data)
        return render_template("show_blogs.html", blogs=output, user=user)
    else:
        return redirect(url_for("page_error"))


@app.route("/show_this_blog/<blog_id>", methods=["post", "get"])
def show_this_blog(blog_id):
    """for showing the detail of current selected blog only"""
    if not session.get("user_id") is None:
        user_id = session.get("user_id")
        user = session.get("username")
        blog = Blog.query.filter_by(
            blog_id=blog_id, blog_user_id=user_id
        ).first()
        if not blog:
            flash("sorry no such blog found")
        return render_template("show_this_blog.html", blog=blog, user=user)

    else:
        return redirect(url_for("page_error"))


@app.route("/show_all_blogs", methods=["post", "get"])
def show_all_blogs():
    """lists all blogs stored in db"""
    blogs = Blog.query.all()
    output = []
    for blog in blogs:
        user = User.query.filter_by(user_id=blog.blog_user_id).first()
        blog_data = {}
        blog_data["blog_id"] = blog.blog_id
        blog_data["blog_title"] = blog.blog_title
        blog_data["blog_type"] = blog.blog_type
        blog_data["blog_content"] = blog.blog_content
        blog_data["blog_desc"] = blog.blog_desc
        blog_data["username"] = user.user_name
        output.append(blog_data)
    return render_template("show_all_blogs.html", blogs=output)


@app.route("/show_chosen_blog/<blog_id>", methods=["post", "get"])
def show_chosen_blog(blog_id):
    """show choosen blog for a reader"""
    blog = Blog.query.filter_by(blog_id=blog_id).first()
    user = User.query.filter_by(user_id=blog.blog_user_id).first()
    if not blog:
        flash("sorry no such blog found")
    return render_template("show_chosen_blog.html",
                           blog=blog, username=user.user_name)


@app.route("/delete_blog/<blog_id>", methods=["DELETE", "GET", "POST"])
def delete_blog(blog_id):
    """deletes the blog"""
    if not session.get("user_id") is None:
        user_id = session.get("user_id")
        blog = Blog.query.filter_by(
            blog_id=blog_id, blog_user_id=user_id
        ).first()
        if not blog:
            flash("No such blog found!")
        db.session.delete(blog)
        db.session.commit()
        return redirect(url_for("show_my_blogs"))
    else:
        return redirect(url_for("page_error"))


@app.route("/update_my_blog/<blog_id>", methods=["GET", "POST", "PUT"])
def update_my_blog(blog_id):
    """update the blog"""
    if not session.get("user_id") is None:
        user_id = session.get("user_id")
        user = session.get("username")
        blog = Blog.query.filter_by(
            blog_id=blog_id, blog_user_id=user_id
        ).first()
        form = UpdateForm(obj=blog)
        if not blog:
            flash("No such blog found!")
        if form.validate_on_submit():
            blog.blog_title = form.blog_title.data
            blog.blog_type = form.blog_type.data
            blog.blog_content = form.blog_content.data
            blog.blog_desc = form.blog_desc.data
            db.session.commit()
            flash("Blog succesfully updated!")
            return redirect(url_for("show_my_blogs"))
        return render_template("update.html", form=form, user=user)
    else:
        return redirect(url_for("page_error"))


@app.route("/error", methods=["GET"])
def page_error():
    """shows up if the user is not  logged in or not registered"""
    return render_template("error.html")
