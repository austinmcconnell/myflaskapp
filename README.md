# My Flask App

[![CircleCI][circleci_logo]][circleci_link] [![Codecov][codecov_logo]][codecov_link] [![Pyup][pyup_logo]][pyup_link]

[circleci_logo]: https://circleci.com/gh/austinmcconnell/myflaskapp.svg?style=shield
[circleci_link]: https://circleci.com/gh/austinmcconnell/myflaskapp
[codecov_logo]: https://codecov.io/gh/austinmcconnell/myflaskapp/branch/master/graph/badge.svg
[codecov_link]: https://codecov.io/gh/austinmcconnell/myflaskapp
[pyup_logo]: https://pyup.io/repos/github/austinmcconnell/myflaskapp/shield.svg
[pyup_link]: https://pyup.io/repos/github/austinmcconnell/myflaskapp/

A flasky app.

## Prerequisites

### Pyenv

This project uses [pipenv](https://github.com/pypa/pipenv) to manage requirements.

From the pipenv project readme:

>Pipenv — the officially recommended Python packaging tool from Python.org, free (as in freedom).
>
>Pipenv is a tool that aims to bring the best of all packaging worlds (bundler, composer, npm, cargo, yarn, etc.) to the Python world. Windows is a first–class citizen, in our world.
>
>It automatically creates and manages a virtualenv for your projects, as well as adds/removes packages from your Pipfile as you install/uninstall packages. It also generates the ever–important Pipfile.lock, which ensures deterministic builds.

Install with pip

```bash
pip install pipenv
```

## Installation

Run the following commands to setup your environment :

```shell
git clone https://github.com/austinmcconnell/myflaskapp
cd myflaskapp
pre-commit install
pipenv install --dev
```

You will see a pretty welcome screen [here](http://localhost:5000)

### Generate a secret key

Generate a secret key by opening up a python shell and running this code:

```python
import secrets

secrets.token_hex(20)
```

Take the token from above and place it in a .env file along with the following information:

```ini
SECRET_KEY=secret_token_from_above
POSTGRES_PASSWORD=secret_password
```

For local development, also add then following environment variable

```ini
FLASK_ENV=development
```

If you are using docker-compose to run the app locally, add the domain env var

```ini
DOMAIN=myflaskapp.localhost
```

and add this to your `/etc/hosts` file

```
 localhost    myflaskapp.localhost, traefik.myflaskapp.localhost, postgres.myflaskapp.localhost
 ```

This uses a sqlite database by default for local development. If you would like to setup something more powerful (or that matches your production setup), add the following section to your .env file:

```ini
# Database
DB_USERNAME=username
DB_PASSWORD=password
DB_HOST=host
DB_NAME=port
```

Once you have installed your DBMS, run the following to create your
app\'s database tables and perform the initial migration:

```python
    flask db init
    flask db migrate
    flask db upgrade
```

## Shell

To open the interactive shell, run :

```shell
flask shell
```

By default, you will have access to the flask `app`.

## Running Tests

To run all tests, run :

```shell
flask test
```

## Migrations

To update the database migration, run the following
commands:

```shell
flask db migrate
```

This will generate a new migration script. Then run :

```shell
flask db upgrade
```

To apply the migration.

For a full migration command reference, run `flask db --help`.

## Asset Management

Webpack\'s `file-loader` will copy files placed inside the `assets`
directory and its subdirectories (excluding `js` and `css`)
into the `static/build` directory, with hashes of their contents
appended to their names. For instance, if you have the file
`assets/img/favicon.ico`, this will get copied into something like
`static/build/img/favicon.fec40b1d14528bf9179da3b6b78079ad.ico`. You can
then put this line into your header:

```html
<link rel="shortcut icon" href="{{asset_url_for('img/favicon.ico') }}">
```

to refer to it inside your HTML page. If all your static files are
managed this way, then their filenames will change whenever their
contents do, and you can ask Flask to tell web browsers that they should
cache all your assets forever by including the following line in your
`settings.py`:

```ini
SEND_FILE_MAX_AGE_DEFAULT = 31556926  # one year
```
