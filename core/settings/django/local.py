# ruff: noqa: F405, F403

from .base import *

DEBUG = True

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME", cast=str),
        "USER": env("DB_USER", cast=str),
        "PASSWORD": env("DB_PASS", cast=str),
        "HOST": env("DB_HOST", cast=str),
        "PORT": env("DB_PORT", cast=int),
    }
}
