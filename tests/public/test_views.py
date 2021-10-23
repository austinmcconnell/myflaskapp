# -*- coding: utf-8 -*-
from flask import url_for
import pytest


def test_get_robots_txt(testapp):
    response = testapp.get(url_for('public.robots_txt'))

    assert 'User-agent:' in response.text
    assert 'Disallow:' in response.text


@pytest.mark.xfail(reason='https://github.com/Alexis-benoist/eralchemy/issues/80')
def test_get_erd(testapp):
    response = testapp.get(url_for('public.show_database_diagram'))

    assert 'image/png' in response.content_type
