# -*- coding: utf-8 -*-
"""Application configuration."""
import os

from dotenv import load_dotenv

load_dotenv()


class Config(object):

    # Path
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
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
    TESTING = True
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4  # For faster tests; needs at least 4 to avoid "ValueError: Invalid rounds"
    WTF_CSRF_ENABLED = False  # Allows form testing
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_TEST_DATABASE_URI')


CONFIG = dict(default=Config,
              testing=TestingConfig)
