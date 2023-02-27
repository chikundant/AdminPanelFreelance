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
    birthday = db.Column(db.Date)
    additional_comment = db.Column(db.String(64))


    def __repr__(self):
        return '<User {} {}>'.format(self.id, self.name)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_comment = db.Column(db.String(250))
    personal_comment = db.Column(db.String(250))
    cell_id = db.Column(db.Integer, db.ForeignKey('cell.id'))
    #conclusion = db.Column(db.String(250))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", backref="users")

    def __repr__(self):
        return '<User {} {}>'.format(self.id, 'Game')


class Type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    description = db.Column(db.String(250))

    cell = db.relationship('Cell', backref='Cell.type_id', primaryjoin='Type.id==Cell.type_id', lazy='dynamic')


class Cell(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    description = db.Column(db.String(250))

    cell = db.relationship('Game', backref='Game.cell_id', primaryjoin='Cell.id==Game.cell_id', lazy='dynamic')

    type_id = db.Column(db.Integer, db.ForeignKey('type.id'))
    type = db.relationship("Type", backref="cells")

    def __repr__(self):
        return '<Cell {} {}>'.format(self.id, 'Cell')


@login.user_loader
def load_user(id):
    return Admin.query.get(int(id))
