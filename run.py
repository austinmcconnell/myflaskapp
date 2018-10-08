# -*- coding: utf-8 -*-
from flask.helpers import get_debug_flag

from myflaskapp.app import create_app

CONFIG_NAME = 'development' if get_debug_flag() else 'default'

APP = create_app(CONFIG_NAME)  # pylint: disable=invalid-name
