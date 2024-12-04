from typing import TypedDict

from rest_framework.request import Request


class SentryKwargsType(TypedDict, total=False):
    request: Request
