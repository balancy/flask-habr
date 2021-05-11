import os
from datetime import timedelta

from dotenv import load_dotenv


class Config(object):
    """Base config, uses staging database server."""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """Uses production database server."""
    DB_SERVER = ''


class DevelopmentConfig(Config):
    DEBUG = True

    load_dotenv()
    username = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')
    db = os.getenv('POSTGRES_DB')
    SECRET_KEY = os.urandom(32)
    REMEMBER_COOKIE_DURATION = timedelta(days=5)

    SQLALCHEMY_DATABASE_URI = ('postgresql+psycopg2://'
                               f'{username}:{password}@localhost:5432/{db}')


class TestingConfig(Config):
    DEBUG = True
