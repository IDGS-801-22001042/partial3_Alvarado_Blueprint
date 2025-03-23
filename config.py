import os
from sqlalchemy import create_engine

import urllib
class Config(object):
    SECRET_KEY = 'Las Pipsas'
    SESSION_COOKIE_SECRET = False
    TEMP_DIR = 'tmp'  # Agrega esta línea

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Asakalaluya1$@127.0.0.1/ExamenPizzas'
    SQLALCHEMY_TRACK_MODIFICATIONS = False