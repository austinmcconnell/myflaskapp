# -*- coding: utf-8 -*-
"""Click commands."""
from glob import glob
import os
from subprocess import call

import click

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir)
TEST_PATH = os.path.join(PROJECT_ROOT, 'tests')


@click.command()
def test():
    import pytest
    status_code = pytest.main([TEST_PATH])
    exit(status_code)


@click.command()
def lint():
    skip = ['__pycache__', 'migrations', 'static']
    root_files = glob('*.py')
    root_directories = [name for name in next(os.walk('.'))[1] if not name.startswith('.')]
    files_and_directories = [arg for arg in root_files + root_directories if arg not in skip]

    def execute_tool(description, *args):
        """Execute a checking tool with its arguments."""
        command_line = list(args) + files_and_directories
        click.echo('{}: {}'.format(description, ' '.join(command_line)))
        status_code = call(command_line)
        if status_code != 0:
            exit(status_code)
    execute_tool('Checking code style', 'pylint')


@click.command()
def clean():
    for dirpath, dirnames, filenames in os.walk('.'):
        for filename in filenames:
            if filename.endswith('.pyc') or filename.endswith('.pyo'):
                full_pathname = os.path.join(dirpath, filename)
                click.echo('Removing {}'.format(full_pathname))
                os.remove(full_pathname)
