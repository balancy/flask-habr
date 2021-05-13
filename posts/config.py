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
    HOST = os.getenv('POSTGRES_HOST')
    SECRET_KEY = os.urandom(32)
    REMEMBER_COOKIE_DURATION = timedelta(days=5)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = ('postgresql+psycopg2://'
                               f'{USERNAME}:{PASSWORD}@{HOST}:5432/habr_db')


class ProductionConfig(Config):
    """Uses production database server.
    """

    DEBUG = False


class DevelopmentConfig(Config):
    """Config used for development.
    """

    DEBUG = True


class TestingConfig(Config):
    DEBUG = True
