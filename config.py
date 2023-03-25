import os

KEY = 'Your key here'
basedir = os.path.abspath(os.path.dirname(__file__))
USERS_PER_PAGE = 10


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or KEY
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'main.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

