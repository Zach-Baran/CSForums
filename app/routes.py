from app import app, users
from flask import Flask, render_template, redirect, url_for, flash
from app.forms import CreateUser, LoginUser
from werkzeug.security import generate_password_hash

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/Register', methods=['GET','POST'])
def register():
    form=CreateUser()
    if form.validate_on_submit():
        users[form.username.data] = generate_password_hash(form.password.data)
        form.username.data=''
        form.password.data=''
        return redirect(url_for('view_users'))
    return render_template('createuser.html', form=form)


@app.route('/Users', methods=['GET'])
def view_users():
    return render_template('users.html', users=users)
