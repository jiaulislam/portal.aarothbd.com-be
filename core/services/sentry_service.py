from django.forms.models import model_to_dict
from rest_framework.request import Request
from sentry_sdk import capture_exception, push_scope

from core.exceptions import MissingSentryRequestParamException


def capture_exception_sentry(e, **kwargs):
    request: Request = kwargs.get("request", None)
    if not request:
        raise MissingSentryRequestParamException()
    with push_scope() as scope:
        scope.set_extra("tenant", model_to_dict(request.user))  # type: ignore
        capture_exception(e)
