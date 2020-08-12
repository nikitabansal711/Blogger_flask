import datetime
import uuid
import jwt
from flask import render_template, redirect, url_for, flash, session
from flask import jsonify, make_response
from werkzeug.security import check_password_hash, generate_password_hash
from app import app, db
from app.forms import LoginForm, SignupForm, BlogForm, UpdateForm
from .models import User, Blog


@app.route("/", methods=["post", "get"])
def home():
    return render_template("home.html")


@app.route("/login", methods=["post", "get"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_name=form.username.data).first()
        if not user:
            return make_response(
                "Could not verify",
                401,
                {"WWW-Authenticate": 'Basic realm="Login required!"'},
            )
        if check_password_hash(user.password, form.password.data):
            token = jwt.encode(
                {
                    "public_id": user.public_id,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
                },
                app.config["SECRET_KEY"],
            )
            data = jsonify({"token": token.decode("UTF-8")})
            user_dict = {
                "username": user.user_name,
                "user_id": user.user_id,
                "user_email": user.user_email,
                "user_mobile": user.user_email
            }
            session["token"] = token
            session["user"] = user_dict
            print('session set')
            return redirect(url_for("dashboard"))

        return make_response(
            "Could not verify",
            401,
            {"WWW-Authenticate": 'Basic realm="Login required!"'},
        )

    return render_template("login.html", title="Sign In", form=form)


@app.route("/signup", methods=["post", "get"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method="sha256")
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
        flash("New user created with username {}".format(new_user.user_name))

    return render_template("signup.html", title="Sign In", form=form)


@app.route("/dashboard", methods=["post", "get"])
def dashboard():
    if not session.get("token") is None:
        form = BlogForm()
        user = session.get('user')
        if form.validate_on_submit():
            new_blog = Blog(
                blog_title=form.blog_title.data,
                blog_type=form.blog_type.data,
                blog_desc=form.blog_desc.data,
                blog_content=form.blog_content.data,
                blog_user_id=user["user_id"]
            )
            db.session.add(new_blog)
            db.session.commit()
            flash("New blog created with title {}".format(new_blog.blog_title))

        return render_template("dashboard.html", form=form, user=user)
    else:
        return redirect(url_for('page_error'))


@app.route("/log_out", methods=["post", "get"])
def log_out():
    session.pop("token", None)
    return redirect(url_for("home"))


@app.route("/show_my_blogs", methods=["post", "get"])
def show_my_blogs():
    if not session.get("token") is None:
        user = session.get('user')
        blogs = Blog.query.filter_by(blog_user_id=user["user_id"]).all()
        output = []
        for blog in blogs:
            blog_data = {}
            blog_data['blog_id'] = blog.blog_id
            blog_data['blog_title'] = blog.blog_title
            blog_data['blog_type'] = blog.blog_type
            blog_data['blog_content'] = blog.blog_content
            blog_data['blog_desc'] = blog.blog_desc
            output.append(blog_data)
        return render_template("show_blogs.html", blogs=output, user=user)
    else:
        flash("you are not logged in buddy!")
        return redirect(url_for('page_error'))


@app.route("/show_this_blog/<blog_id>", methods=["post", "get"])
def show_this_blog(blog_id):
    if not session.get("token") is None:
        user = session.get('user')
        blog = Blog.query.filter_by(blog_id=blog_id, blog_user_id=user["user_id"]).first()
        if not blog:
            flash("sorry no such blog found")
        return render_template("show_this_blog.html", blog=blog, user=user)

    else:
        return redirect(url_for('page_error'))


@app.route("/show_all_blogs", methods=["post", "get"])
def show_all_blogs():
    blogs = Blog.query.all()
    output = []
    for blog in blogs:
        blog_data = {}
        blog_data['blog_id'] = blog.blog_id
        blog_data['blog_title'] = blog.blog_title
        blog_data['blog_type'] = blog.blog_type
        blog_data['blog_content'] = blog.blog_content
        blog_data['blog_desc'] = blog.blog_desc
        output.append(blog_data)
    return render_template("show_all_blogs.html", blogs=output)


@app.route("/show_chosen_blog/<blog_id>", methods=["post", "get"])
def show_chosen_blog(blog_id):
    blog = Blog.query.filter_by(blog_id=blog_id).first()
    if not blog:
        flash("sorry no such blog found")
    return render_template("show_chosen_blog.html", blog=blog)


@app.route('/delete_blog/<blog_id>', methods=['DELETE', 'GET', 'POST'])
def delete_blog(blog_id):
    if not session.get("token") is None:
        user = session.get('user')
        blog = Blog.query.filter_by(blog_id=blog_id, blog_user_id=user["user_id"]).first()
        if not blog:
            flash("No such blog found!")
        db.session.delete(blog)
        db.session.commit()
        return redirect(url_for("show_my_blogs"))
    else:
        return redirect(url_for('page_error'))


@app.route('/update_my_blog/<blog_id>', methods=['GET', 'POST', 'PUT'])
def update_my_blog(blog_id):
    if not session.get("token") is None:
        user = session.get('user')
        blog = Blog.query.filter_by(blog_id=blog_id, blog_user_id=user["user_id"]).first()
        form = UpdateForm()
        print("hi")
        if not blog:
            flash("No such blog found!")
        if form.validate_on_submit():
            if form.blog_title.data:
                blog.blog_title = form.blog_title.data
            if form.blog_type.data:
                blog.blog_type = form.blog_type.data
            if form.blog_content.data:
                blog.blog_content = form.blog_content.data
            if form.blog_desc.data:
                blog.blog_desc = form.blog_desc.data
            print(blog)
            db.session.commit()
            return redirect(url_for("show_my_blogs"))
        return render_template("update.html", form=form, user=user)
    else:
        return redirect(url_for('page_error'))


@app.route('/error', methods=['GET'])
def page_error():
    return render_template("error.html")