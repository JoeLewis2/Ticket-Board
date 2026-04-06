import os

class Config:
    # path to this folder
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # sqlite database stored in the instance folder
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'tickets.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # secret key for sessions
    SECRET_KEY = os.environ.get('SECRET_KEY')
