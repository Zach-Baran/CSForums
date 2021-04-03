from app import app, db
from app.models import User
from flask import Flask, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import CreateUser, LoginUser
from werkzeug.security import generate_password_hash, check_password_hash
import sys


@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('homepage.html', user=current_user)


@app.route('/register', methods=['GET','POST'])
def register():
    form=CreateUser()
    if form.validate_on_submit():
        submit = User(email=form.email.data, first_name=form.firstname.data, last_name=form.lastname.data,  \
            password_hash=generate_password_hash(form.password.data), role="Member", code=0)
        db.session.add(submit)
        db.session.commit()
        form.firstname.data=''
        form.lastname.data=''
        form.email.data=''
        form.password.data=''
        return redirect(url_for('home'))
    return render_template('createuser.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=LoginUser()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data).first()
        if user == None or check_password_hash(user.password_hash, form.password.data) != True:
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('home'))
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
