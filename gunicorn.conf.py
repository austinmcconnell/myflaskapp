# pylint: disable=invalid-name

wsgi_app = 'wsgi:app'
bind = '0.0.0.0:5000'
# workers = multiprocessing.cpu_count() * 2 + 1  # Using WEB_CONCURRENCY env var

accesslog = '-'
errorlog = '-'
