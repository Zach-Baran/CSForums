from app import app, db
from app.models import User, Forums, Events, Post
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import CreateUser, LoginUser, createTopic, createEvent, createPost
from werkzeug.security import generate_password_hash, check_password_hash

import sys, time
import datetime




@app.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        return render_template('homepage.html', users=db.session.query(User).all())
    else:
        return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = CreateUser()
    if form.validate_on_submit():
        checkUsers = db.session.query(User).filter_by(username=form.username.data).first()
        if checkUsers == None:
            submit = User(username=form.username.data, email=form.email.data, first_name=form.firstname.data, last_name=form.lastname.data,  \
                password_hash=generate_password_hash(form.password.data), role="Member", code=0)
            db.session.add(submit)
            db.session.commit()
            form.username.data=''
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
    form = LoginUser()
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


# Function handles creating and deleting topics, and viewing the forums
@app.route('/forums/createtopic', endpoint='createtopic', methods=['GET', 'POST'])
@app.route('/forums', endpoint='forums', methods=['GET', 'POST'])
def forums():
    if current_user.is_authenticated:
        if request.endpoint == 'createtopic':  # If requested url is createtopic
            if current_user.role == 'admin':
                form = createTopic()
                if form.validate_on_submit():
                    topic = Forums(admin_id=current_user.id, date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),\
                    topic_name=form.title.data, topic_description=form.description.data)
                    db.session.add(topic)
                    db.session.commit()
                    form.title.data = ''
                    form.description.data = ''
                    return redirect(url_for('home'))
                return render_template('createtopic.html', form=form)
            else:
                return redirect(url_for('forums'))
        elif request.endpoint == 'forums':  # If requested url is forums
            if request.method == 'POST':  # if admin clicked delete topic button
                if request.form['action'] == 'del_topic':
                    db.engine.execute('DELETE FROM forums where id = {};'.format(request.form.get("del_topic")))
                    return redirect(url_for('forums'))
            if request.method == 'GET':
                topics = db.engine.execute('SELECT * from forums;')
                return render_template('forums.html', topics=topics)
    else:
        return redirect(url_for('login'))



# Dynamic user route, displays a profile given a unique first name

@app.route('/forums/<topicID>/<topicName>', methods=['GET', 'POST'])
def post(topicID, topicName):
    if current_user.is_authenticated:
        form=createPost()
        data = db.engine.execute('SELECT * FROM post WHERE forum_id = {};'.format(topicID))
        if request.method == 'GET': #Display posts under the topic and allow user to post
            return render_template('post.html', posts=data, form=form)
        if request.method == 'POST': #When user submits post
            if form.validate_on_submit():
                post = Post(username=current_user.username, user_id=current_user.id, date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), \
                    post_content=form.content.data, forum_id=topicID)
                db.session.add(post)
                db.session.commit()
                form.content.data=''
                return redirect(url_for('post', topicID=topicID, topicName=topicName))
            else:
                return render_template('post.html', posts=data, form=form)



#Dynamic user route, displays a profile given a unique first name

@app.route('/profile/<user>', methods=['GET', 'POST'])
def profile(user):
    if request.method == 'POST':  # if admin clicked ban or delete button
        if request.form['action'] == 'banuser':
            db.engine.execute('UPDATE users SET role = "banned" WHERE id = {};'.format(request.form.get("ban_button")))
            return '{}'.format(request.form.get("ban_button"))
        elif request.form['action'] == 'deleteuser':
            db.engine.execute('DELETE FROM users WHERE id = {};'.format(request.form.get("delete_button")))
            return 'Account Deleted'
    if request.method == 'GET':  # if user is viewing profile
        if current_user.is_authenticated:
            valid = db.session.query(User).filter_by(username=user).first()
            if valid != None:
                return render_template('profile.html', user=valid)
            else:
                return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))


# Function handles viewing creating events
@app.route('/createevents/', methods=['GET', 'POST'])
def createevents():
    if current_user.is_authenticated:
        #if current_user.role=='admin':
            form = createEvent()
            if form.validate_on_submit():
                event = Events(event_name=form.event_name.data, event_date=form.event_date.data,
                                    description=form.description.data)
                db.session.add(event)
                db.session.commit()
                form.event_name.data = ''
                form.event_date.data = ''
                form.description.data = ''
            return render_template('create_event.html', form=form)
    else:
        return redirect(url_for('login'))

# Function handles viewing events
@app.route('/events')
def events():
        all = db.session.query(Events).all()
        print(all, file=sys.stderr)
        return render_template('view_events.html', events=all)

