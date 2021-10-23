# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from flask_babel import Babel
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from flask_caching import Cache
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from secure import Secure
from sqlalchemy import MetaData

# pylint: disable=invalid-name

convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}

babel = Babel()
bcrypt = Bcrypt()
bootstrap = Bootstrap()
csrf_protect = CSRFProtect()
login_manager = LoginManager()
db = SQLAlchemy(metadata=MetaData(naming_convention=convention))
migrate = Migrate(compare_type=True, compare_server_default=True)
cache = Cache()
debug_toolbar = DebugToolbarExtension()
mail = Mail()
moment = Moment()
secure_headers = Secure()
