import multiprocessing

# System Configs
bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1 - 2

# Logging
accesslog = "./logs/gunicorn.access.log"
errorlog = "./logs/gunicorn.error.log"
logger_class = "gunicorn.glogging.Logger"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
loglevel = "warning"

raw_env = ["DJANGO_SETTINGS_MODULE=core.settings.django.dev", "DEBUG=False"]

# Worker & App
wsgi_app = "core.wsgi:application"
