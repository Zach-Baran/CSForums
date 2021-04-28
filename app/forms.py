from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextField, PasswordField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired


class LoginUser(FlaskForm):
    email = StringField('Email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Login')


class CreateUser(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    firstname = StringField('First Name:', validators=[DataRequired()])
    lastname = StringField('Last Name:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Login')

class createTopic(FlaskForm):
    title = StringField('Title:', validators=[DataRequired()])
    description = StringField('Description:', validators=[DataRequired()])
    submit = SubmitField('Create Topic')


class createEvent(FlaskForm):
    event_name = StringField('Event Name:', validators=[DataRequired()])
    description = StringField('Description:', validators=[DataRequired()])
    event_date = DateTimeLocalField('Event Date:', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    submit = SubmitField('Create Event')


class createPost(FlaskForm):
    content = StringField('Content:', validators=[DataRequired()])
    submit = SubmitField('Post')

class createCareer(FlaskForm):
    job_name = StringField('Job Name:', validators=[DataRequired()])
    job_date = StringField('Posted Date:', validators=[DataRequired()])
    applyBy_date = StringField('Apply By:', validators=[DataRequired()])
    description = StringField('Description:', validators=[DataRequired()])
    submit = SubmitField('Create Career')

class memberRequest(FlaskForm):
    email = StringField('Email:', validators=[DataRequired()])
    submit = SubmitField('Submit')

class emailAnnouncement(FlaskForm):
    topic = StringField('Email Topic:', validators=[DataRequired()])
    message = StringField('Message:', validators=[DataRequired()])
    submit = SubmitField('Send Emails')
