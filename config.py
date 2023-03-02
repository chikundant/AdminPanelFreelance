import os

KEY = 'you-will-never-guess'
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or KEY
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'main.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

