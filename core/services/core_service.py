from typing import Optional

from django.http.request import HttpRequest
from rest_framework.request import Request

from apps.user.models import User


class CoreService:
    def get_user(self, request: HttpRequest | Request | None) -> Optional[User]:
        """gets the authenticated user object from request object"""
        if request and request.user.is_authenticated:
            user: User = request.user  # type: ignore
            return user
        return None
