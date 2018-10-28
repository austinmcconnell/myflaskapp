# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, flash, render_template, request, session
from flask_babel import _
from flask_login import current_user, login_required

from app.extensions import db, login_manager
from app.user.forms import (EditProfileForm)
from app.user.models import User
from app.utils import flash_errors

user_bp = Blueprint(name='user',  # pylint: disable=invalid-name
                    import_name=__name__,
                    template_folder='templates')


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@user_bp.route('/users')
@login_required
def members():
    """List members."""
    return render_template('members.html')


@user_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.locale = form.locale.data
        db.session.commit()
        session['locale'] = form.locale.data
        flash(_('Your changes have been saved.'))
        # return redirect(url_for('public.home'))
        return render_template('profile.html', title=_('Profile'), form=form)
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.locale.data = current_user.locale
    else:
        flash_errors(form)
    return render_template('profile.html', title=_('Profile'), form=form)
