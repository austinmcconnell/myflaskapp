from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user

from myflaskapp.user.forms import LoginForm
from myflaskapp.utils import flash_errors

bp = Blueprint(name='public',  # pylint: disable=invalid-name
               import_name=__name__,
               template_folder='templates')


@bp.route('/about/')
def about():
    """About page."""
    form = LoginForm(request.form)
    return render_template('about.html', nav_form=form)


@bp.route('/', methods=['GET', 'POST'])
def home():
    """Home page."""
    form = LoginForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash('You are logged in.', 'success')
            redirect_url = request.args.get('next') or url_for('user.members')
            return redirect(redirect_url)
        else:
            flash_errors(form)

    return render_template('home.html', nav_form=form)
