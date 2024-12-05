from typing import Tuple

from django.conf import settings as s
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import AuthUser, JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import Token


class SecureCookieAuthentication(JWTAuthentication):
    def authenticate(self, request: Request) -> Tuple[AuthUser, Token] | None:
        access_token = request.COOKIES.get(s.SIMPLE_JWT["AUTH_COOKIE"])
        if not access_token:
            return None

        valid_token = self.get_validated_token(str.encode(access_token))
        try:
            auth_user = self.get_user(valid_token)
        except (KeyError, AuthenticationFailed) as _:
            return None
        return (auth_user, valid_token)
