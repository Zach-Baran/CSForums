from app import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), unique=True)
    username = db.Column(db.String(64), unique=True)
    first_name = db.Column(db.String(64), unique=False)
    last_name = db.Column(db.String(64), unique=False)
    role = db.Column(db.String(64), unique=False, nullable=False)
    code = db.Column(db.Integer, unique=False)
    post = db.relationship('Post', backref='users', lazy='dynamic')

    def pw_reset_token(self, expires_time_sec=120):
        tokenSer = Serializer('fantasticfour', expires_time_sec)
        return tokenSer.dumps({'userID': self.id}).decode('utf-8')

    @staticmethod
    def verify_token(token):
        tokenSer = Serializer('fantasticfour')
        try:
            user_ID = tokenSer.loads(token)['userID']
        except:
            return None
        return User.query.get(user_ID)

    def __repr__(self):
        return self.email + ': ' + self.role + ':' + self.first_name + ':' + self.last_name

class Forums(db.Model):
    __tablename__ = 'forums'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    topic_name = db.Column(db.String(64), unique=False)
    topic_description = db.Column(db.String(500), unique=False)
    posts = db.relationship('Post', backref='forums', lazy='dynamic')


    def __repr__(self):
        return str(self.users.id) + ': ' + str(self.date) + ': ' + self.topic_name + ': ' + self.topic_description + ': '+  self.role


# class Add_member(db.Model):
#     __tablename__ = 'add_member'
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(64), unique=True, nullable=False )
#     admin_id = db.Column(db.Integer, nullable=False)
#     approve_code = db.Column(db.Integer, nullable=False)
#
#     def __repr__(self):
#         return str(self.add_member.id) + ': ' + self.email + ': ' + str(self.admin_id)


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'), nullable=False)
    username = db.Column(db.String(64))
    date = db.Column(db.DateTime, nullable=False)
    post_content = db.Column(db.String(1000), unique=False)
    forum_id = db.Column(db.Integer, db.ForeignKey('forums.id'))
    status = db.Column(db.String(1))

    def __repr__(self):
        return str(self.post.id) + ': ' + str(self.forum_id) + ': ' + str(self.user_id) + ': ' + str(self.date) + ': ' + self.content


class Events(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(64), nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(500), unique=False, nullable=True)
    event_content = db.Column(db.String(255), unique=False)

    def __repr__(self):
        return self.event_name + ': ' + str(self.event_date) + ': ' + self.description


class Career(db.Model):
    __tablename__ = 'job'
    id = db.Column(db.Integer, primary_key=True)
    comp_name = db.Column(db.String(64), unique=False, nullable=False)
    job_name = db.Column(db.String(64), unique=False, nullable=False,)
    job_date = db.Column(db.DateTime, unique=False, nullable=False)
    applyBy_date = db.Column(db.String(64), unique=False, nullable=False)
    description = db.Column(db.String(64), unique=False, nullable=False)
    apply_link = db.Column(db.String(64), unique=False, nullable=False)

    def __repr__(self):
        return str(self.id) + ': ' + str(self.job_date) + ': ' + self.description + ': ' + self.job_name



# class GCode(db.Model):
#     __tablename__ = 'code'
#     a_id = db.Column(db.Integer, primary_key=True)
#     code = db.Column(db.Integer, nullable=False, unique=True)
#
#     def __repr__(self):
#         return str(self.a.id) + ': ' + str(self.code)

class RegisterRequest(db.Model):
    __tablename__ = 'regrequest'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    email_conf = db.Column(db.Integer, unique=False, nullable=False)
    admin_code = db.Column(db.String(64), unique=True, nullable=True)

    def __repr__(self):
        return str(self.email) + ': ' + str(self.admin_code)
