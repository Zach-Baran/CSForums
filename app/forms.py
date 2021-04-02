from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextField, PasswordField
from wtforms.validators import DataRequired



class LoginUser(FlaskForm):
    email=StringField('Email:', validators=[DataRequired()])
    password=PasswordField('Password:', validators=[DataRequired()])
    submit=SubmitField('Login')

class CreateUser(FlaskForm):
    firstname=StringField('First Name:', validators=[DataRequired()])
    lastname=StringField('Last Name:', validators=[DataRequired()])
    email=StringField('Email:', validators=[DataRequired()])
    password=PasswordField('Password:', validators=[DataRequired()])
    submit=SubmitField('Login')
