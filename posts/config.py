import os
from datetime import timedelta

from dotenv import load_dotenv


class Config(object):
    """Base config, uses staging database server.
    """

    DEBUG = False

    load_dotenv()
    USERNAME = os.getenv('POSTGRES_USER')
    PASSWORD = os.getenv('POSTGRES_PASSWORD')
    DB = os.getenv('POSTGRES_DB')
    HOST = os.getenv('HOST')
    PORT = os.getenv('PORT')
    SECRET_KEY = os.urandom(32)
    REMEMBER_COOKIE_DURATION = timedelta(days=5)

    SQLALCHEMY_DATABASE_URI = ('postgresql+psycopg2://'
                               f'{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB}')


class ProductionConfig(Config):
    """Uses production database server.
    """

    DEBUG = False
    pass


class DevelopmentConfig(Config):
    """Config used for development.
    """

    DEBUG = True

    load_dotenv()
    USERNAME = os.getenv('POSTGRES_USER')
    PASSWORD = os.getenv('POSTGRES_PASSWORD')
    DB = os.getenv('POSTGRES_DB')
    SECRET_KEY = os.urandom(32)
    REMEMBER_COOKIE_DURATION = timedelta(days=5)

    SQLALCHEMY_DATABASE_URI = ('postgresql+psycopg2://'
                               f'{USERNAME}:{PASSWORD}@localhost:5432/{DB}')


class TestingConfig(Config):
    DEBUG = True
    pass
