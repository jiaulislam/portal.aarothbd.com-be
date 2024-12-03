from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import exceptions as e
from rest_framework import status as s
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenRefreshView

from ..serializers.auth_serializers_v1 import (
    CookieTokenRefreshSerializer,
    LoginSerializer,
    RegisterUserSerializer,
)
from ..services import TokenService


class RegisterUserAPIView(GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = RegisterUserSerializer

    def post(self, request: Request, format=None):
        body = RegisterUserSerializer(data=request.data)
        body.is_valid(raise_exception=True)

        user = body.save()

        if user is None:
            return Response(
                {"status": "error", "msg": "create user failed !"},
                status=s.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"status": "success", "msg": "account created"},
            status=s.HTTP_201_CREATED,
        )


class LoginAPIView(GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = LoginSerializer

    @TokenService.set_auth_cookies
    def post(self, request, format=None):
        body = LoginSerializer(data=request.data)

        body.is_valid(raise_exception=True)

        email = body.validated_data["email"]
        password = body.validated_data["password"]

        authorized_user = authenticate(request, email=email, password=password)

        if authorized_user is None:
            raise e.AuthenticationFailed("Email or Password is incorrect")

        tokens = TokenService.generate_user_token(authorized_user)

        return Response(tokens)


class LogoutView(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @TokenService.unset_auth_cookies
    def post(self, request, format=None):
        return Response(status=s.HTTP_204_NO_CONTENT)


class CookieTokenRefreshView(TokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get("refresh"):
            response.set_cookie(
                key=settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"],
                value=response.data["refresh"],
                expires=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTPONLY"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            )
            del response.data["refresh"]

        response["X-CSRFToken"] = request.COOKIES.get("csrftoken", "")
        return super().finalize_response(request, response, *args, **kwargs)
