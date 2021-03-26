import pyodbc
import os
import urllib.parse
from flask import Flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:compsciserver.database.windows.net,1433;DATABASE=CompSciHub;UID=fantasticfour;PWD=CSC330sp1")

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'fantasticfour'
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" %  params
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)


users={}
from app import routes, models
