web: flask translate compile; gunicorn wsgi:app
release: flask db upgrade
worker: rq worker --url $REDIS_URL myflaskapp-tasks
