# -*- coding: utf-8 -*-
from flask.helpers import get_debug_flag

from app.app import create_app

CONFIG_NAME = 'development' if get_debug_flag() else 'default'

app = create_app(CONFIG_NAME)  # pylint: disable=invalid-name
