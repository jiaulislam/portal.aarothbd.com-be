# ruff: noqa: F405, F403

from typing import List

from .base import *

DEBUG = True

hosts: List[str] = env.tuple("ALLOWED_HOSTS")

ALLOWED_HOSTS = [host.strip() for host in hosts]

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
