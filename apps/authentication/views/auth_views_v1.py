from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import exceptions as e
from rest_framework import status
from rest_framework import status as s
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView

from apps.user.services import UserService

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
    user_service = UserService()

    def post(self, request: Request, *args, **kwargs):
        serialized = RegisterUserSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        plain_text_password = serialized.validated_data["password"]
        serialized.validated_data["password"] = self.user_service.hash_password(plain_text_password)
        _ = self.user_service.create(serialized.validated_data)
        return Response(
            {"detail": "Successfully Registered."},
            status=s.HTTP_201_CREATED,
        )


class LoginAPIView(GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = LoginSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        body = LoginSerializer(data=request.data)
        body.is_valid(raise_exception=True)
        email = body.validated_data["email"]
        password = body.validated_data["password"]

        authorized_user = authenticate(request, email=email, password=password)

        if authorized_user is None:
            raise e.AuthenticationFailed("Email or Password is incorrect")
        token_service = TokenService(request, authorized_user)
        response = token_service.get_secured_cookie_response()
        response.data = {"detail": "Logged in Successfully."}
        response.status_code = status.HTTP_200_OK
        return response


class LogoutAPIView(GenericAPIView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        response = TokenService.get_removed_cookies_response(request)
        response.data = {"detail": "Logged out successfully."}
        response.status_code = status.HTTP_200_OK
        return response


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
