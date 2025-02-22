from flask_babel import _
from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from app.user.models import User


class RegisterForm(FlaskForm):
    """Register form."""

    username = StringField(label=_l('Username'), validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField(label=_l('Email'),
                        validators=[DataRequired(), Email(),
                                    Length(min=6, max=40)])
    password = PasswordField(label=_l('Password'),
                             validators=[DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField(
        label=_l('Verify password'),
        validators=[DataRequired(),
                    EqualTo('password', message=_l('Passwords must match'))])
    submit = SubmitField(_l('Register'))

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super().__init__(*args, **kwargs)
        self.user = None

    def validate(self, extra_validators=None):
        """Validate the form."""
        initial_validation = super().validate(extra_validators=extra_validators)
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append(_('Username already registered'))
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append(_('Email already registered'))
            return False
        return True


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField(_l('Username'),
                           validators=[DataRequired()],
                           render_kw={'placeholder': _l('Username')})
    password = PasswordField(_l('Password'),
                             validators=[DataRequired()],
                             render_kw={'placeholder': _l('Password')})
    submit = SubmitField(_l('Log In'))

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super().__init__(*args, **kwargs)
        self.user = None

    def validate(self, extra_validators=None):
        """Validate the form."""
        initial_validation = super().validate(extra_validators=extra_validators)
        if not initial_validation:
            return False

        self.user = User.query.filter_by(username=self.username.data).first()
        if not self.user:
            self.username.errors.append(_('Unknown username'))
            return False

        if not self.user.check_password(self.password.data):
            self.password.errors.append(_('Invalid password'))
            return False

        if not self.user.active:
            self.username.errors.append(_('User not activated'))
            return False
        return True


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Request Password Reset'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(_l('Repeat Password'),
                              validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Reset Password'))
