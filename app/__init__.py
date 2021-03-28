from flask import Flask

import mysql.connector
from mysql.connector import errorcode
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

import os

load_dotenv('.flaskenv')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'fantasticfour'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://fantasticfour@compscihubserver:CSC330sp1@compscihubserver.mysql.database.azure.com/compscihub"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True


db = SQLAlchemy(app)
login_manager=LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()

from app import routes, models
from app.models import User
