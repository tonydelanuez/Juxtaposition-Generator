import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DATABASE_USER = os.getenv("DATABASE_USER", "postgres")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "password")
    DATABASE_HOST = os.getenv("DATABASE_HOST", "postgres")
    DATABASE_PORT = os.getenv("DATABASE_PORT", 5432)
    DATABASE_NAME = os.getenv("DATABASE_NAME", "juxgen")
    DATABASE_SCHEME = os.getenv("DATABASE_SCHEME", "sqlite://")
    SQLALCHEMY_DATABASE_URI = f'{DATABASE_SCHEME}{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
