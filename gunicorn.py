import multiprocessing

# System Configs
bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1 - 2
worker_connections = 200
max_requests = 1000
max_requests_jitter = 1000
graceful_timeout = 30
limit_request_line = 4094
limit_request_field_size = 100
reload = True
sendfile = False
proxy_allow_ips = "127.0.0.1"
timeout = 30
keepalive = 3

# Logging
accesslog = "./logs/gunicorn.access.log"
errorlog = "./gunicornlogs/gunicorn.error.log"
logger_class = "gunicorn.glogging.Logger"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
loglevel = "info"


# Worker & App
worker_class = "uvicorn.workers.UvicornWorker"
wsgi_app = "core.wsgi:application"
