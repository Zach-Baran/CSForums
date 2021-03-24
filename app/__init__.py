from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'csc330temppass'


users={}
from app import routes
