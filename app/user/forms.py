"""User forms."""
from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired


class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    first_name = StringField(_l('First Name'))
    last_name = StringField(_l('Last Name'))
    locale = SelectField(_l('Preferred Language'),
                         choices=[('en', _l('English')), ('fr', _l('French'))])
    submit = SubmitField(_l('Submit'))
