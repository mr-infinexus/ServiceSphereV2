from os import getenv
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    FLASK_DEBUG = getenv("FLASK_DEBUG", False)
    FLASK_RUN_HOST = getenv("FLASK_RUN_HOST")
    FLASK_RUN_PORT = getenv("FLASK_RUN_PORT")
    SECRET_KEY = getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = getenv("SQLALCHEMY_TRACK_MODIFICATIONS", False)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=3)
    JWT_SECRET_KEY = getenv("JWT_SECRET_KEY")
    CELERY_BROKER_URL = getenv("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = getenv("CELERY_RESULT_BACKEND")
    CACHE_TYPE = getenv("CACHE_TYPE")
    CACHE_REDIS_HOST = getenv("CACHE_REDIS_HOST")
    CACHE_REDIS_PORT = getenv("CACHE_REDIS_PORT")
    MAIL_SERVER = getenv("MAIL_SERVER")
    MAIL_PORT = getenv("MAIL_PORT")
    SENDER_EMAIL = getenv("SENDER_EMAIL")
    SENDER_PASSWORD = getenv("SENDER_PASSWORD")
