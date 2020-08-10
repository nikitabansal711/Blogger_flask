from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm, RoleForm, SignupForm


@app.route('/', methods=['post', 'get'])
def home():
    form = RoleForm()
    if form.validate_on_submit():
        if form.choice.data == 'blogger':
            return redirect(url_for('login'))

        # else:
        # return redirect(url_for('show_all'))
    else:
        print(form.errors)
    return render_template('home.html', form=form)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)


@app.route('/signup')
def signup():
    form = SignupForm()
    return render_template('signup.html', title='Sign In', form=form)
