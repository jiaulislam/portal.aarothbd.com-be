from typing import Unpack

import sentry_sdk
from django.forms.models import model_to_dict
from rest_framework.request import Request
from sentry_sdk import capture_exception

from core.types import SentryKwargsType

__all__ = ["capture_exception_sentry"]


def capture_exception_sentry(e, **kwargs: Unpack[SentryKwargsType]):
    request: Request = kwargs.pop("request", None)
    scope = sentry_sdk.get_current_scope()
    if bool(request):
        user_ctx = model_to_dict(instance=request.user, fields=["id", "email", "user_type"]) # type: ignore
        scope.set_user(user_ctx)
    for k, v in kwargs.items():
        scope.set_extra(str(k), v)
    capture_exception(e)
