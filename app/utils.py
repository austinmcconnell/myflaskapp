"""Helper utilities and decorators."""
from functools import wraps

from flask import abort, current_app, flash


def flash_errors(form, category='warning'):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash('{} - {}'.format(getattr(form, field).label.text, error), category)


def development_only(func):

    @wraps(func)
    def wrapped(**kwargs):
        if not current_app.env == 'development':
            abort(404)
        return func(**kwargs)

    return wrapped
