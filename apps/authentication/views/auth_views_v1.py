from datetime import timedelta

from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import exceptions as e
from rest_framework import status
from rest_framework import status as s
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.user.constants import AuthProviderChoices
from apps.user.services import UserService
from core.serializers import FailResponseSerializer, SuccessResponseSerializer

from ..serializers.auth_serializers_v1 import (
    LoginSerializer,
    RegisterUserSerializer,
    ResetPasswordSerializer,
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
        _ = self.user_service.create_customer(serialized.validated_data)
        # TODO: customer email verification task should implement here [Celery Task]
        return Response(
            {"detail": "Successfully Registered."},
            status=s.HTTP_201_CREATED,
        )


class LoginAPIView(GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = LoginSerializer

    @extend_schema(
        request=LoginSerializer,
        responses={
            200: SuccessResponseSerializer,
            403: FailResponseSerializer,
            400: FailResponseSerializer,
        },
        examples=[
            OpenApiExample(
                name="Login Request",
                summary="Login Request Payload",
                description="Example of a valid request payload for login.",
                value={"email": "admin@aarothbd.com", "password": "*****"},
                response_only=False,
                request_only=True,
            )
        ],
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        serialized = LoginSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        email = serialized.validated_data["email"]
        password = serialized.validated_data["password"]

        authorized_user = authenticate(request, email=email, password=password)

        if authorized_user is None:
            raise e.AuthenticationFailed("Email or Password is incorrect")
        authorized_user.last_login = timezone.now()
        authorized_user.save()
        token_service = TokenService(request, authorized_user)
        response = token_service.get_secured_cookie_response()
        response.data = {"detail": "Logged in Successfully."}
        response.status_code = status.HTTP_200_OK
        return response


class LogoutAPIView(GenericAPIView):
    serializer_class = SuccessResponseSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        response = TokenService.get_removed_cookies_response(request)
        response.data = {"detail": "Logged out successfully."}
        response.status_code = status.HTTP_200_OK
        return response


class RefreshTokenAPIView(GenericAPIView):
    serializer_class = SuccessResponseSerializer

    def post(self, request: Request, *args, **kwargs):
        current_user = request.user
        token_service = TokenService(request, current_user)  # type: ignore
        response = token_service.get_refresh_token_response()
        response.data = {"detail": "token has been refreshed successfully."}
        response.status_code = status.HTTP_200_OK

        response["X-CSRFToken"] = request.COOKIES.get("csrftoken", "")
        return response


class ResetPasswordAPIView(GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = ResetPasswordSerializer
    user_service = UserService()

    def post(self, request: Request, *args, **kwargs):
        serialized = ResetPasswordSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        email = serialized.validated_data["email"]
        user = self.user_service.get(email=email, auth_provider=AuthProviderChoices.EMAIL)
        token = RefreshToken.for_user(user).access_token
        token.set_exp(lifetime=timedelta(minutes=10))
        reset_url = f"{request.scheme}://{request.get_host()}/reset-password?token={token}"
        context = {
            "reset_url": reset_url,
            "user": user,
        }
        email_html_message = render_to_string("reset-password-email.html", context)

        send_mail(
            "Password Reset Request",
            email_html_message,
            "no-reply@aarothbd.com",
            [email],
            fail_silently=False,
            html_message=email_html_message,
        )
        return Response(
            {"detail": "Password reset link has been sent to your email."},
            status=s.HTTP_200_OK,
        )
