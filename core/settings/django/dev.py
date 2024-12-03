# ruff: noqa: F405, F403

from typing import List

from .base import *

DEBUG = True

hosts: List[str] = env.tuple("ALLOWED_HOSTS")

ALLOWED_HOSTS = [host.strip() for host in hosts]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASS"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}
