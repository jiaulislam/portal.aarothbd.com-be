from core.env import env

if env.bool("DJANGO_DEBUG", default=True):
    LOG_LEVEL = "DEBUG"
else:
    LOG_LEVEL = "WARNING"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue"},
    },
    "formatters": {
        "main_formatter": {
            "format": "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s "
            "(%(filename)s:%(lineno)d)",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "console": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "main_formatter",
        },
        "production_file": {
            "level": "WARNING",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/main.log",
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 7,
            "formatter": "main_formatter",
            "filters": ["require_debug_false"],
        },
        "debug_file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/debug.log",
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 7,
            "formatter": "main_formatter",
            "filters": ["require_debug_true"],
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "production_file", "debug_file"],
            "level": LOG_LEVEL,
        },
    },
}
