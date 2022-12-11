import os
from datetime import timedelta
from os.path import join, dirname, realpath
import os
import re
from decouple import config

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = join(dirname(realpath(__file__)), "static/uploads")

uri = config("DATABASE_URL")  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)


# rest of connection code using the connection string `uri

class Config:
    SECRET_KEY = config('SECRET_KEY', 'secret')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_SECRET_KEY = config('JWT_SECRET_KEY')
    UPLOAD_FOLDER = UPLOAD_FOLDER
    ALLOWED_EXTENSIONS = ["jpg", "png"]
    MAX_CONTENT_LENGTH = 1000 * 1024 * 1024  # 1000mb


class DevConfig(Config):
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True


class TestConfig(Config):
    pass


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = config('DEBUG', cast=bool)


config_dict = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'test': TestConfig
}
