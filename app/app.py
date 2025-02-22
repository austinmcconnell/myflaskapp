import maya
import rollbar
import rollbar.contrib.flask
import rq
from flask import Flask, current_app, g, got_request_exception, render_template, request, session
from flask_login import current_user
from flask_mail import email_dispatched
from redis import Redis

from app import commands
from app.auth import auth_bp
from app.extensions import (babel, bcrypt, bootstrap, cache, csrf_protect, db, debug_toolbar,
                            login_manager, mail, migrate, moment, secure_headers)
from app.messages import Message, message_bp
from app.notification.models import Notification
from app.public import public_bp
from app.settings import CONFIG
from app.task.models import Task
from app.user import user_bp
from app.user.models import User


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(CONFIG[config_name])

    register_blueprints(app)
    register_extensions(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)

    @app.before_request
    def before_request():
        if current_user.is_authenticated:
            current_user.last_seen = maya.now().datetime()
            db.session.commit()
        g.locale = str(get_locale())

    @app.after_request
    def set_secure_headers(response):
        secure_headers.framework.flask(response)
        return response

    with app.app_context():
        if not app.config['DEBUG'] and app.config['ROLLBAR_API']:
            app.logger.info('Initiating rollbar connection')
            rollbar.init(access_token=app.config['ROLLBAR_API'],
                         environment=app.config['ENV'],
                         root=app.config['APP_DIR'],
                         allow_logging_basic_config=False)

            got_request_exception.connect(rollbar.contrib.flask.report_exception, app)
            app.logger.info('Rollbar initiated successfully')

    def log_email_message(message, app):
        app.logger.debug(message.body)

    if app.config['DEBUG']:
        email_dispatched.connect(log_email_message)

    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = rq.Queue('myflaskapp-tasks', connection=app.redis)

    return app


def register_extensions(app):
    babel.init_app(app, locale_selector=get_locale)
    bcrypt.init_app(app)
    bootstrap.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    moment.init_app(app)


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(message_bp)
    app.register_blueprint(public_bp)
    app.register_blueprint(user_bp)


def register_errorhandlers(app):

    def render_error(error):
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template('{}.html'.format(error_code)), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)


def register_shellcontext(app):

    def shell_context():
        return {
            'db': db,
            'Message': Message,
            'Notification': Notification,
            'User': User,
            'Task': Task
        }

    app.shell_context_processor(shell_context)


def register_commands(app):
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.check)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.translate)


def get_locale():
    if current_user.is_authenticated:
        locale = current_user.locale
    elif 'locale' in session:
        return session['locale']
    else:
        locale = request.accept_languages.best_match(current_app.config['LANGUAGES'])
    return locale
