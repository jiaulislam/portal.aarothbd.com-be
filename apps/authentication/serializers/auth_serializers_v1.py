from django.contrib.auth import get_user_model
from rest_framework import serializers as s
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from ..types import RegisterUserValidatedDataType


class RegisterUserSerializer(s.ModelSerializer):
    first_name = s.CharField(max_length=88, allow_blank=True, default="")
    last_name = s.CharField(max_length=88, allow_blank=True, default="")
    password2 = s.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ("email", "first_name", "last_name", "password", "password2")
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, attrs: RegisterUserValidatedDataType) -> RegisterUserValidatedDataType:
        password = attrs.get("password", "")
        password2 = attrs.get("password2", "")

        if password != password2:
            raise s.ValidationError({"password": "Passwords do not match!"})
        return attrs


class LoginSerializer(s.Serializer):
    email = s.EmailField()
    password = s.CharField(style={"input_type": "password"}, write_only=True)


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None

    def validate(self, attrs):
        attrs["refresh"] = self.context["request"].COOKIES.get("refresh")
        if attrs["refresh"]:
            return super().validate(attrs)
        else:
            raise InvalidToken("No valid token found in cookie 'refresh'")


class ResetPasswordSerializer(s.Serializer):
    email = s.EmailField()


class ConfirmResetPasswordSerializer(s.Serializer):
    token = s.CharField()
