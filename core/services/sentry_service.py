from typing import Unpack

from django.forms.models import model_to_dict
from rest_framework.request import Request
from sentry_sdk import capture_exception, push_scope

from core.exceptions import MissingSentryRequestParamException
from core.types import SentryKwargsType

__all__ = ["capture_exception_sentry"]


def capture_exception_sentry(e, **kwargs: Unpack[SentryKwargsType]):
    request: Request | None = kwargs.pop("request")
    if not request:
        raise MissingSentryRequestParamException()
    with push_scope() as scope:
        scope.set_extra("user", model_to_dict(request.user))  # type: ignore
        for k, v in kwargs.items():
            scope.set_extra(str(k), v)
        capture_exception(e)
