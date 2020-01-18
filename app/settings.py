# -*- coding: utf-8 -*-
"""Application configuration."""
import os

from dotenv import load_dotenv

load_dotenv(override=True, verbose=True)


class Config(object):

    # Path
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

    # Database
    DB_USERNAME = os.getenv('DATABASE_USERNAME')
    DB_PASSWORD = os.getenv('DATABASE_PASSWORD')
    DB_HOST = os.getenv('DATABASE_HOST')
    DB_PORT = os.getenv('DATABASE_PORT', 5432)
    DB_NAME = os.getenv('DATABASE_NAME')
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@' \
                              f'{DB_HOST}:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email
    MAIL_SERVER = os.environ.get('MAILGUN_SMTP_SERVER')
    MAIL_PORT = int(os.environ.get('MAILGUN_SMTP_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAILGUN_SMTP_LOGIN')
    MAIL_PASSWORD = os.environ.get('MAILGUN_SMTP_PASSWORD')
    ADMINS = ['austin.s.mcconnell@gmail.com']

    # Access tokens
    ROLLBAR_API = os.getenv('ROLLBAR_ACCESS_TOKEN')
    PAPERTRAIL_API = os.getenv('PAPERTRAIL_API_TOKEN')

    # Misc Extension
    LANGUAGES = ['en', 'fr']
    SECRET_KEY = os.environ.get('SECRET_TOKEN')
    BCRYPT_LOG_ROUNDS = 13
    CACHE_TYPE = 'simple'
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://')


class TestingConfig(Config):
    # ENV = 'test'
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'postgresql://{Config.DB_USERNAME}:{Config.DB_PASSWORD}@' \
        f'localhost:{Config.DB_PORT}/myflaskapp-test'
    BCRYPT_LOG_ROUNDS = 4  # For faster tests; needs at least 4 to avoid "ValueError: Invalid rounds"
    WTF_CSRF_ENABLED = False  # Allows form testing
    PRESERVE_CONTEXT_ON_EXCEPTION = False


CONFIG = dict(default=Config,
              testing=TestingConfig)
