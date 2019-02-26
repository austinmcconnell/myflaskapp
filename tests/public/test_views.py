# -*- coding: utf-8 -*-
from flask import url_for


def test_get_robots_txt(testapp):
    response = testapp.get(url_for('public.robots_txt'))

    assert 'User-agent:' in response.text
    assert 'Disallow:' in response.text
