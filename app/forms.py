from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextField, PasswordField
from wtforms.validators import DataRequired



class LoginUser(FlaskForm):
    username=StringField('Username:', validators=[DataRequired()])
    password=PasswordField('Password:', validators=[DataRequired()])
    submit=SubmitField('Login')

class CreateUser(FlaskForm):
    username=StringField('Username:', validators=[DataRequired()])
    password=PasswordField('Password:', validators=[DataRequired()])
    submit=SubmitField('Login')
