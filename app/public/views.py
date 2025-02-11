from flask import Blueprint, flash, redirect, render_template, request, send_from_directory, url_for
from flask_babel import _
from flask_login import login_user

from app.auth.forms import LoginForm
from app.database import Model
from app.utils import development_only, flash_errors

public_bp = Blueprint(
    name='public',  # pylint: disable=invalid-name
    import_name=__name__,
    template_folder='templates')


@public_bp.route('/about/')
def about():
    """About page."""
    form = LoginForm(request.form)
    return render_template('about.html', nav_form=form)


@public_bp.route('/', methods=['GET', 'POST'])
def home():
    """Home page."""
    # pylint: disable=duplicate-code
    form = LoginForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash(_('You are logged in.'), 'success')
            redirect_url = request.args.get('next') or url_for('user.members')
            return redirect(redirect_url)
        else:
            flash_errors(form)

    return render_template('home.html', nav_form=form)


@public_bp.route('/robots.txt')
def robots_txt():
    return send_from_directory('static', 'robots.txt')


@public_bp.route('/erd')
@development_only
def show_database_diagram():
    from eralchemy import render_er

    filename = 'erd_from_sqlalchemy.png'
    render_er(Model, f'app/static/{filename}')
    return send_from_directory(directory='static', filename=filename)
