import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from core.env import env

# from ..django.base import SENTRY_DEBUG, SENTRY_DSN, SENTRY_ENV

SENTRY_DSN = env("SENTRY_DSN")
SENTRY_ENV = env("SENTRY_ENV")
SENTRY_DEBUG = env.bool("SENTRY_DEBUG", default=False)  # type: ignore

sentry_sdk.init(
    dsn=SENTRY_DSN,  # type: ignore
    debug=SENTRY_DEBUG,  # type: ignore
    environment=SENTRY_ENV,  # type: ignore
    integrations=[
        DjangoIntegration(),
    ],
    send_default_pii=True,
    traces_sample_rate=1.0,
)
