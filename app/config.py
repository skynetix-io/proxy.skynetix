import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    MYSQL_DATABASE_HOST = 'localhost'
    MYSQL_DATABASE_USER = 'sito'
    MYSQL_DATABASE_PASSWORD = 'Cazzogloria00%'
    MYSQL_DATABASE_DB = 'sito'
