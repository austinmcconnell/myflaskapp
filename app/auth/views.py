from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from flask_babel import _
from flask_login import current_user, login_required, login_user, logout_user

from app.auth.email import send_confirm_email, send_password_reset_email
from app.auth.forms import LoginForm, RegisterForm, ResetPasswordForm, ResetPasswordRequestForm
from app.extensions import db
from app.user.models import User
from app.utils import flash_errors

auth_bp = Blueprint(
    name='auth',  # pylint: disable=invalid-name
    import_name=__name__,
    template_folder='templates')


@auth_bp.route('/logout/')
@login_required
def logout():
    """Logout."""
    logout_user()
    flash(_('You are logged out.'), 'info')
    return redirect(url_for('public.home'))


@auth_bp.route('/register/', methods=['GET', 'POST'])
def register():
    """Register new user."""
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User.create(username=form.username.data,
                           email=form.email.data,
                           password=form.password.data,
                           active=False,
                           locale=g.locale)
        session['locale'] = user.locale
        flash(_('Thank you for registering. Please validate your email address before logging in.'),
              'success')
        send_confirm_email(user)
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)
    return render_template('register.html', form=form)


@auth_bp.route('/login/', methods=['GET', 'POST'])
def login():
    """Login user."""
    if current_user.is_authenticated:
        return redirect(url_for('public.home'))
    # pylint: disable=duplicate-code
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash(_('You are logged in.'), 'success')
            redirect_url = request.args.get('next') or url_for('user.members')
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template('login.html', form=form)


@auth_bp.route('/reset_password_request/', methods=['GET', 'POST'])
def reset_password_request():
    nav_form = LoginForm(request.form)
    if current_user.is_authenticated:
        flash(_('You are already logged in.'), 'info')
        return redirect(url_for('public.home'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(_('Check your email for the instructions to reset your password'))
        return redirect(url_for('auth.login'))
    return render_template('reset_password_request.html',
                           title='Reset Password',
                           nav_form=nav_form,
                           form=form)


@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        flash(_('You are already logged in.'), 'info')
        return redirect(url_for('public.home'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('public.home'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('auth.login'))
    return render_template('reset_password.html', form=form)


@auth_bp.route('/confirm/<token>', methods=['GET'])
def confirm_email(token):
    if not current_user.is_anonymous:
        if current_user.email_confirmed:
            flash(_('You have already verified your email address.'), 'info')
            return redirect(url_for('public.home'))
    user = User.verify_confirmation_token(token)
    if not user:
        return redirect(url_for('public.home'))
    user.confirm_email()
    user.active = True
    db.session.commit()
    flash(_('Your email has been confirmed.'), 'success')
    return redirect(url_for('public.home'))
