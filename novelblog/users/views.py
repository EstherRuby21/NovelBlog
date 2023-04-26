from flask import render_template, redirect, request, url_for, flash, Blueprint
from flask_login import login_user, login_required, logout_user
from novelblog import db
from novelblog.users.forms import RegistrationForm, LoginForm
from novelblog.models import User

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        flash("Thanks for registering!")
        return redirect(url_for('users.login'))
        
    return render_template('register.html', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None:
            return render_template('login.html', form=form, message="User not found! Please register!")

        elif not user.check_password(form.password.data):
            return render_template('login.html', form=form, message="Wrong password! Please try again!")

        elif user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash("Login successful!")

            next = request.args.get('next')

            if next == None or not next[0] == '/':
                next = url_for('novels.index')

            return redirect(next)

    return render_template('login.html', form=form)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('core.home'))
