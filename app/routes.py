import flask_login
from app import app, db, mail
from app.models import User, Forums, Events, Post, Career, RegisterRequest
from flask import Flask, render_template, redirect, url_for, flash, request, abort, session
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import CreateUser, LoginUser, createTopic, createEvent, createPost, createCareer, memberRequest, emailAnnouncement, \
    resetPassword, forgotPassword, changeEmail, changePassword
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from threading import Thread
import sys
import datetime


@app.route('/', methods=['GET', 'POST'])
def home():
    events = db.engine.execute("SELECT event_name, event_date, description FROM events ORDER BY event_date DESC LIMIT 2")
    return render_template('homepage.html', events=events)



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = CreateUser()
    if form.validate_on_submit():
        checkUsers = db.session.query(User).filter_by(username=form.username.data).first()
        if checkUsers == None:
            submit = User(username=form.username.data, email=form.email.data, first_name=form.firstname.data,
                          last_name=form.lastname.data,
                          password_hash=generate_password_hash(form.password.data), role="Member", code=0)
            db.session.add(submit)
            db.session.commit()
            form.username.data = ''
            form.firstname.data = ''
            form.lastname.data = ''
            form.email.data = ''
            form.password.data = ''
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
    if current_user.is_authenticated and current_user.role != 'banned':
        if request.endpoint == 'createtopic':  # If requested url is createtopic
            if current_user.role == 'admin':
                form = createTopic()
                if form.validate_on_submit():
                    topic = Forums(admin_id=current_user.id, date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                   topic_name=form.title.data, topic_description=form.description.data)
                    db.session.add(topic)
                    db.session.commit()

                    form.title.data = ''
                    form.description.data = ''
                    return redirect(url_for('home'))
                return render_template('createtopic.html', form=form)
            else:
                abort(404)
        elif request.endpoint == 'forums':  # If requested url is forums
            if request.method == 'POST':  # if admin clicked delete topic button
                if request.form['action'] == 'del_topic':
                    db.engine.execute('DELETE FROM forums where id = {};'.format(request.form.get("del_topic")))
                    db.engine.execute('UPDATE post SET status = 0 WHERE forum_id = {}'.format(request.form.get('del_topic')))
                    return redirect(url_for('forums'))
            if request.method == 'GET':

                topics = db.engine.execute('SELECT * from forums;')
                return render_template('forums.html', topics=topics)
    else:
        return redirect(url_for('login'))


#Function to test if session variable is defined
def postWait():
    try:
        post = (datetime.datetime.now()-session['postTime']).total_seconds()
        return post
    except KeyError:
        session['postTime']=None

#Takes unique topic id and the topic name
@app.route('/forums/<topicID>/<topicName>', methods=['GET', 'POST'])
def post(topicID, topicName):
    if current_user.is_authenticated and current_user.role != 'banned':
        form = createPost()
        data = db.engine.execute('SELECT * FROM post WHERE forum_id = {};'.format(topicID))
        if request.method == 'GET':  # Display posts under the topic and allow user to post
            return render_template('post.html', posts=data, form=form)
        if request.method == 'POST':  # When user submits post
            #Check if user has posted within the past 60 seconds
            if postWait()==None or postWait() > 60:
                if form.validate_on_submit():
                    post = Post(username=current_user.username, user_id=current_user.id,
                                date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), \
                                post_content=form.content.data, forum_id=topicID, status='1')
                    session['postTime']=datetime.datetime.now()
                    db.session.add(post)
                    db.session.commit()
                    form.content.data = ''
                    return redirect(url_for('post', topicID=topicID, topicName=topicName))
                else:
                    return render_template('post.html', posts=data, form=form)
            else:
                flash('Please wait 1 minute before posting again')
                return render_template('post.html', posts=data, form=form)


# Dynamic user route, displays a profile given a unique first name
@app.route('/profile/<user>', methods=['GET', 'POST'])
def profile(user):
    if current_user.role != 'banned':
        if request.method == 'POST':  # if admin clicked ban or delete button
            if request.form['action'] == 'banuser':
                db.engine.execute('UPDATE users SET role = "banned" WHERE id = {};'.format(request.form.get("ban_button")))
                return redirect(request.url)
            elif request.form['action'] == 'deleteuser':
                db.engine.execute('DELETE FROM users WHERE id = {};'.format(request.form.get("delete_button")))
                return redirect(request.url)
            elif request.form['action'] == 'unbanuser':
                db.engine.execute('UPDATE users SET role = "Member" WHERE id = {};'.format(request.form.get("unban_button")))
                return redirect(request.url)
            elif request.form['action'] == 'change-email':
                return redirect(url_for('change_email'))
            elif request.form['action'] == 'change-password':
                return redirect(url_for('change_password'))
        if request.method == 'GET':  # if user is viewing profile
            if current_user.is_authenticated:
                posts = db.engine.execute('SELECT post.post_content,post.date, forums.topic_name, forums.id, post.username FROM \
                                            post INNER JOIN forums WHERE post.forum_id=forums.id AND post.username="{}" AND post.status="1" \
                                            ORDER BY post.date DESC;'.format(user))
                valid = db.session.query(User).filter_by(username=user).first()
                if posts != None and valid != None:
                    print(user)
                    return render_template('profile.html', posts=posts, user=valid)
                else:
                    abort(404)
            else:
                return redirect(url_for('login'))
    return redirect(url_for('home'))

#Allows admins to send a mass email
@app.route('/announcement', methods=['GET', 'POST'])
def announcement():
    if current_user.role=='admin':
        form = emailAnnouncement()
        if form.validate_on_submit():
            subject = form.topic.data
            body = form.message.data
            emailThreading = Thread(target=sendMassEmail, args=(subject, body,))
            emailThreading.start()
            form.topic.data=''
            form.message.data=''
            flash('Emails sent')
        return render_template('announcements.html', form=form)
    else:
        abort(404)

#Sends email to all registered users
def sendMassEmail(subject, body):
    with app.app_context():
        recipient = db.engine.execute('SELECT email FROM users;')
        for email in recipient:
            mail.send(Message(subject, recipients=[email[0]], body=body))



# Function handles viewing creating events
@app.route('/events/createevent/', methods=['GET', 'POST'])
def createevents():
    if current_user.role=='admin':
        form = createEvent()
        if form.validate_on_submit():
            event = Events(event_name=form.event_name.data, event_date=form.event_date.data,
                           description=form.description.data)
            db.session.add(event)
            db.session.commit()
            date = form.event_date.data - datetime.timedelta(hours=12)
            date = date.strftime('%m/%d at %H:%M EST')
            subject = "A new event has been posted: "+form.event_name.data+" taking place on "+date
            body = form.description.data
            #Create thread so admin does not have to wait for emails to be sent before leaving page
            emailThreading = Thread(target=sendMassEmail, args=(subject, body,))
            emailThreading.start()
            form.event_name.data = ''
            form.event_date.data = ''
            form.description.data = ''
            flash('Event Posted and members notified')
        return render_template('create_event.html', form=form)
    else:
        abort(404)

# Function handles viewing events
@app.route('/events')
def events():
    all = db.session.query(Events).all()
    time = datetime.datetime.now()
    return render_template('view_events.html', events=all, time=time)


@app.route('/createcareer', methods=['GET', 'POST'])
def createcareer():
    if current_user.role=='admin':
        form = createCareer()
        if form.validate_on_submit():
            jobs = Career(comp_name=form.comp_name.data, job_name=form.job_name.data, job_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),applyBy_date=form.applyBy_date.data,
                         description=form.description.data, apply_link=form.apply_link.data)
            db.session.add(jobs)
            db.session.commit()
            form.comp_name.data = ''
            form.job_name.data = ''
            form.applyBy_date.data = ''
            form.description.data = ''
            form.apply_link.data = ''
        return render_template('create_career.html', form=form)
    else:
        abort(404)


@app.route('/career')
def career():
      all = db.session.query(Career).all()
      return render_template('view_career.html', job=all)


@app.route('/member_req', methods=['GET', 'POST'])
def member_req():
    form = memberRequest()
    if form.validate_on_submit():
        req = RegisterRequest(email=form.email.data, email_conf=0, admin_code=None)
        db.session.add(req)
        db.session.commit()
        form.email.data = ''
        flash('E-mail sent for verification')
        return redirect('member_req')
    return render_template('memreq.html', form=form)


@app.route('/userauth')
def userauth():
    if current_user.is_authenticated and current_user.role!='banned':
        if current_user.role == 'admin':
            all = db.session.query(RegisterRequest).all()
            print(all, file=sys.stderr)
            return render_template('userauth.html', regrequest=all)
        else:
            return redirect(url_for('home'))



def reset_email(user):
    token = user.pw_reset_token()
    resetMSG = Message('Password Reset', sender='csc330emaildisposable@gmail.com', recipients=[user.email])
    resetMSG.body = f'''Password Reset Link : {url_for('reset_password', token=token, _external=True)}'''
    mail.send(resetMSG)


@app.route('/reset_password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = forgotPassword()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        reset_email(user)
        form.email.data = ''
        flash('Reset link sent for resetting the password')
        return redirect(url_for('login'))
    return render_template('forgot_request.html', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_token(token)
    if user is None:
        flash('Expired or Invalid token')
        return redirect(url_for('reset_password'))
    form = resetPassword()
    if form.validate_on_submit():
        if form.password.data == form.confirmPw.data:
            user.password_hash = generate_password_hash(form.password.data)
            db.session.commit()
            flash('Your password is updated')
            return redirect(url_for('login'))
        else:
            flash('Make sure the Passwords in both fields match')
    return render_template('reset_password.html', form=form)


@app.route('/change_email', methods=['GET', 'POST'])
def change_email():
    form = changeEmail()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            if form.email.data == form.confirmEm.data:
                current_user.email = form.email.data
                db.session.commit()
                form.email.data = ''
                form.confirmEm.data = ''
                flash('Email Changed')
            else:
                flash('Make sure the E-mails in both fields match')
        return render_template('changeEm.html', form=form)
    else:
        return redirect(url_for('login'))

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    form = changePassword()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            if not check_password_hash(current_user.password_hash, form.previousPW.data):
                flash('Make sure the Old password is entered in correctly')
            else:
                if form.newPW.data == form.confirmPW.data:
                    current_user.password_hash = generate_password_hash(form.confirmPW.data)
                    db.session.commit()
                    flask_login.logout_user()
                    return redirect(url_for('login'))
                else:
                    flash('Make sure the re-entered password matches the new password')
        return render_template('changePw.html', form=form)
    else:
        return redirect(url_for('login'))

@app.errorhandler(404)
def errorpage(e):
    return render_template('404.html'),404
