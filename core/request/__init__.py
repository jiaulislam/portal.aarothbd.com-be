from django.contrib.auth.models import AnonymousUser
from rest_framework.request import Request as BaseRequest

from apps.user.types import User


class Request(BaseRequest):
    @property
    def user(self) -> User | AnonymousUser | None:
        return super().user
