# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from functools import wraps
from flask import abort, flash, current_app


def flash_errors(form, category='warning'):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash('{0} - {1}'.format(getattr(form, field).label.text, error), category)


def development_only(f):
    @wraps(f)
    def wrapped(**kwargs):
        if not current_app.env == 'development':
            abort(404)
        return f(**kwargs)
    return wrapped
