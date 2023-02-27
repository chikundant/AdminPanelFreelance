from project import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from project import login


class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True)
    phone = db.Column(db.String(64), unique=True)
    date = db.Column(db.Date)
    additional_comment = db.Column(db.String(64))

    game = db.relationship('Game', backref='Game.friend_id', primaryjoin='User.id==Game.user_id', lazy='dynamic')

    def __repr__(self):
        return '<User {} {}>'.format(self.id, self.name)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_comment = db.Column(db.String(250))
    personal_comment = db.Column(db.String(250))
    #conclusion = db.Column(db.String(250))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<User {} {}>'.format(self.id, 'Game')



@login.user_loader
def load_user(id):
    return Admin.query.get(int(id))
