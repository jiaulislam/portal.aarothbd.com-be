from django.contrib.auth.models import AbstractBaseUser
from django.http.request import HttpRequest
from rest_framework.request import Request


class CoreService:
    def get_user(self, request: HttpRequest | Request | None) -> AbstractBaseUser | None:
        """gets the authenticated user object from request object"""
        if request and request.user.is_authenticated:
            user: AbstractBaseUser = request.user  # type: ignore
            return user
        return None
