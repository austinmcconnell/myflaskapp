"""User views."""
import maya
from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for
from flask_babel import _
from flask_login import current_user, login_required

from app.extensions import db, login_manager
from app.notification.models import Notification
from app.user.forms import EditProfileForm
from app.user.models import User
from app.utils import flash_errors

user_bp = Blueprint(
    name='user',  # pylint: disable=invalid-name
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


@user_bp.route('/notifications')
@login_required
def notifications():

    def to_date(date_string):
        return maya.when(date_string).datetime()

    since = request.args.get('since', maya.when('Jan 1 2019').datetime(), type=to_date)

    user_notifications = current_user.notifications\
        .filter(Notification.timestamp > since)\
        .order_by(Notification.timestamp.asc())

    response = [{
        'name': n.name,
        'data': n.payload,
        'timestamp': n.timestamp
    } for n in user_notifications]
    return jsonify(response)


@user_bp.route('/example_task')
@login_required
def example_task():
    if current_user.get_task_in_progress('example'):
        flash(_('An export task is currently in progress'))
    else:
        current_user.launch_task('example', _('Runing example task...'), 25)
        db.session.commit()
    return redirect(url_for('user.members'))
