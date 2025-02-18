import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from ..django.base import SENTRY_DEBUG, SENTRY_DSN, SENTRY_ENV

sentry_sdk.init(
    dsn=SENTRY_DSN,
    debug=SENTRY_DEBUG,
    environment=SENTRY_ENV,
    integrations=[
        DjangoIntegration(),
    ],
)
