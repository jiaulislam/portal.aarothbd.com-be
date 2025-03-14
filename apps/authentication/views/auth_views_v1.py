from django.contrib.auth import authenticate
from django.utils import timezone
from django.utils.crypto import get_random_string
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import exceptions as e
from rest_framework import status
from rest_framework import status as s
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from apps.user.services import UserService
from core.exceptions.common import CustomException
from core.serializers import FailResponseSerializer, SuccessResponseSerializer

from ..serializers.auth_serializers_v1 import (
    LoginSerializer,
    OTPVerificationSerializer,
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
        from sms_service.services import SSLWirelessService

        serialized = RegisterUserSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        user = self.user_service.create_customer(serialized.validated_data)
        otp_code = self.user_service.assign_otp_code(user)

        sms_service = SSLWirelessService()
        sms_service.send_sms(
            message=f"Your OTP code is: {otp_code}",
            phone_number=user.phone,
        )
        return Response(
            {"user_id": user.pk, "detail": "Successfully Registered. An OTP has been sent to your phone."},
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
                value={"user_name": "admin@aarothbd.com", "password": "*****"},
                response_only=False,
                request_only=True,
            )
        ],
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        serialized = LoginSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        user_name = serialized.validated_data["user_name"]  # This can be email or phone number
        password = serialized.validated_data["password"]

        authorized_user = authenticate(request, user_name=user_name, password=password)
        if authorized_user is None:
            raise e.AuthenticationFailed("Authentication Failed !")

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
        from sms_service.services import SSLWirelessService

        serialized = ResetPasswordSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        user_name = serialized.validated_data["user_name"]
        user = self.user_service.get(user_name=user_name)
        otp_code = self.user_service.assign_otp_code(user)

        sms_service = SSLWirelessService()
        sms_service.send_sms(
            message=f"Your OTP code is: {otp_code}",
            phone_number=user.phone,
        )
        return Response(
            {"user_id": user.pk, "detail": "OTP has been sent to your phone."},
            status=s.HTTP_200_OK,
        )


class PasswordResetOTPAPIview(GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = OTPVerificationSerializer
    user_service = UserService()

    def post(self, request: Request, *args, **kwargs):
        serializer = OTPVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            from sms_service.services import SSLWirelessService

            user_id = serializer.validated_data["user_id"]
            otp_code = serializer.validated_data["otp_code"]
            user = self.user_service.get(id=user_id, otp_code=otp_code)
            # Generate a random password
            random_password = get_random_string(length=8)
            user.set_password(random_password)
            user.otp_code = None
            user.save()
            sms_service = SSLWirelessService()
            sms_service.send_sms(
                message=f"Your new password is: {random_password}. Please change it after login.",
                phone_number=user.phone,
            )
            return Response(
                {"detail": "A new password has been sent to your email."},
                status=s.HTTP_200_OK,
            )
        except self.user_service.model_class.DoesNotExist:
            exc = CustomException(detail="Invalid OTP code.")
            exc.default_code = "invalid_otp_code"
            exc.status_code = s.HTTP_400_BAD_REQUEST
            raise exc


class RegisterOTPValidationAPIView(GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = OTPVerificationSerializer
    user_service = UserService()

    def post(self, request: Request, *args, **kwargs):
        serializer = OTPVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user_id = serializer.validated_data["user_id"]
            otp_code = serializer.validated_data["otp_code"]
            user = self.user_service.get(id=user_id, otp_code=otp_code, is_active=False)
            user.otp_code = None
            user.is_active = True
            user.save()
            return Response(
                {"detail": "Account created. Login to continue."},
                status=s.HTTP_200_OK,
            )
        except self.user_service.model_class.DoesNotExist:
            exc = CustomException(detail="Invalid OTP code.")
            exc.default_code = "invalid_otp_code"
            exc.status_code = s.HTTP_400_BAD_REQUEST
            raise exc
