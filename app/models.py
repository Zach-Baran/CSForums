from app import db
from flask_login import UserMixin
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), unique=True)
    first_name = db.Column(db.String(64), unique=False)
    last_name = db.Column(db.String(64), unique=False)
    role = db.Column(db.String(64), unique=False, nullable=False)
    code = db.Column(db.Integer, unique=False)
    def get(self):
        return 
    def __repr__(self):
        return self.email + ': ' + self.role + ':' + self.first_name + ':' + self.last_name

class Forums(db.Model):
    __tablename__ = 'forums'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    admin_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Integer, nullable=False)
    topic_name = db.Column(db.String(64), unique=False)
    topic_description = db.Column(db.String(64), unique=False)
    role = db.Column(db.String(64), unique=False)

    def __repr__(self):
        return str(self.users.id) + ': ' + str(self.date) + ': ' + self.topic_name + ': ' + self.topic_description + ': '+  self.role


class Add_member(db.Model):
    __tablename__ = 'add_member'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, nullable=False )
    admin_id = db.Column(db.Integer, nullable=False)
    approve_code = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return str(self.add_member.id) + ': ' + self.email + ': ' + str(self.admin_id)


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    forum_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Integer, nullable=False)
    post_content = db.Column(db.String(128), unique=False)

    def __repr__(self):
        return str(self.post.id) + ': ' + str(self.forum_id) + ': ' + str(self.user_id) + ': ' + str(self.date) + ': ' + self.content


class Events(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(64), nullable=False,)
    event_date = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(64), unique=False, nullable=False)
    event_content = db.Column(db.String(128), unique=False)
    role = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return str(self.events.id) + ': ' + str(self.event_date) + ': ' + self.description + ': ' + self.content + ': ' + self.role


class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), unique=True )
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    role = db.Column(db.String(64), nullable=False)
    generate_id = db.Column(db.Integer, nullable=False, unique=True)

    def __repr__(self):
        return str(self.admin.id) + ': ' + self.email + ': ' + self.first_name + ': ' + self.last_name + ': ' + self.role
