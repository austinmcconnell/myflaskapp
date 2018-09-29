# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask, render_template, got_request_exception
from flask_mail import email_dispatched

import rollbar
import rollbar.contrib.flask

from myflaskapp import commands, user, public
from myflaskapp.extensions import (bcrypt, cache, csrf_protect, db, debug_toolbar, login_manager,
                                   migrate, mail, moment)
from myflaskapp.settings import ProdConfig


def create_app(config_object=ProdConfig):
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)

    @app.before_first_request
    def init_rollbar():
        if app.config['ENV'] in ('production',) and app.config['ROLLBAR_API']:
            rollbar.init(access_token=app.config['ROLLBAR_API'],
                         environment=app.config['ENV'],
                         root=app.config['APP_DIR'],
                         allow_logging_basic_config=False)

            got_request_exception.connect(rollbar.contrib.flask.report_exception, app)

    def log_email_message(message, app):
        app.logger.debug(message.body)

    if app.config['DEBUG']:
        email_dispatched.connect(log_email_message)

    return app


def register_extensions(app):
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    moment.init_app(app)


def register_blueprints(app):
    app.register_blueprint(user.views.bp)
    app.register_blueprint(public.views.bp)


def register_errorhandlers(app):
    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template('{0}.html'.format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)


def register_shellcontext(app):
    def shell_context():
        """Shell context objects."""
        return {
            'db': db,
            'User': user.models.User}

    app.shell_context_processor(shell_context)


def register_commands(app):
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)
