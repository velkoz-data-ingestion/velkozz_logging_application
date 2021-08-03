"""Logger Application Configuration."""
# Importing environment modules:
from os import environ, path
from dotenv import load_dotenv

# Loading External Environment Configuration File: 
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.logger.env'))

class Config:
    "Base Configuration"
    SECRET_KEY = environ.get('SECRET_KEY')
    #SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = environ.get('DEV_DATABASE_URI')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = f"postgresql://{environ['POSTGRES_USER']}:{environ['POSTGRES_PASSWORD']}@velkozz_logger_psql:{environ['POSTGRES_PORT']}/{environ['POSTGRES_DB']}"
    SQLALCHEMY_TRACK_MODIFICATIONS=False