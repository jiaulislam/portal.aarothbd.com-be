from typing import Any, MutableMapping

import sentry_sdk
from django.forms.models import model_to_dict
from rest_framework.request import Request
from sentry_sdk import capture_exception

__all__ = ["capture_exception_sentry"]


def capture_exception_sentry(e, **kwargs: MutableMapping[str, Any]) -> None:
    request: Request = kwargs.pop("request", None)  # type: ignore
    scope = sentry_sdk.get_current_scope()
    if bool(request):
        user_ctx = model_to_dict(instance=request.user, fields=["id", "email", "user_type"])  # type: ignore
        scope.set_user(user_ctx)
    for k, v in kwargs.items():
        scope.set_extra(str(k), v)
    capture_exception(e)
