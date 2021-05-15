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
    SECRET_KEY = os.urandom(32)
    REMEMBER_COOKIE_DURATION = timedelta(days=5)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = os.getenv(
        'SQLALCHEMY_DATABASE_URI',
        f'postgresql+psycopg2://{USERNAME}:{PASSWORD}@localhost:5432/{DB}')


class ProductionConfig(Config):
    """Uses production database server.
    """

    DB_SERVER = '0.0.0.0'
    DEBUG = False


class DevelopmentConfig(Config):
    """Config used for development.
    """

    DEBUG = True


class TestingConfig(Config):
    DEBUG = True
