from django.conf import settings as s
from django.contrib.auth.models import AbstractBaseUser
from django.middleware import csrf
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt import tokens
from rest_framework_simplejwt.tokens import RefreshToken

from ..exceptions import TokenServiceFailureException
from ..types import TokenResponse

__all__ = ["TokenService"]


class TokenService:
    token = TokenResponse()

    def __init__(self, request: Request, user: AbstractBaseUser):
        self.request = request
        self.user = user

    def _set_token_for_user(self):
        if not self.user:
            raise TokenServiceFailureException(detail="user not found to create token !")
        refresh = RefreshToken.for_user(self.user)
        self.token = TokenResponse(
            refresh_token=str(refresh),
            access_token=str(refresh.access_token),  # type: ignore
            iat=refresh.get("iat"),
            exp=refresh.get("exp"),
        )

    def get_secured_cookie_response(self) -> Response:
        self._set_token_for_user()
        response = Response()

        access_token = self.token.get("access_token")
        refresh_token = self.token.get("refresh_token")

        if not access_token or not refresh_token:
            raise TokenServiceFailureException(detail="access or refresh token maybe null !")

        response.set_cookie(
            key=s.SIMPLE_JWT["AUTH_COOKIE"],
            value=access_token,
            expires=s.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
            secure=s.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            httponly=s.SIMPLE_JWT["AUTH_COOKIE_HTTPONLY"],
            samesite=s.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )

        response.set_cookie(
            key=s.SIMPLE_JWT["AUTH_COOKIE_REFRESH"],
            value=refresh_token,
            expires=s.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
            secure=s.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            httponly=s.SIMPLE_JWT["AUTH_COOKIE_HTTPONLY"],
            samesite=s.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )
        response["X-CSRFToken"] = csrf.get_token(self.request)
        return response

    @classmethod
    def get_removed_cookies_response(cls, request: Request) -> Response:
        refresh_token = request.COOKIES.get(s.SIMPLE_JWT["AUTH_COOKIE_REFRESH"])
        token = tokens.RefreshToken(refresh_token)  # type: ignore
        token.blacklist()
        response = Response()
        response.delete_cookie(s.SIMPLE_JWT["AUTH_COOKIE"])
        response.delete_cookie(s.SIMPLE_JWT["AUTH_COOKIE_REFRESH"])
        response.delete_cookie("X-CSRFToken")
        response.delete_cookie("csrftoken")
        del response["X-CSRFToken"]
        return response
