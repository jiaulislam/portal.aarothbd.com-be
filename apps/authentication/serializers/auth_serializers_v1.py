import re
from typing import Any, MutableMapping

from django.contrib.auth import get_user_model
from rest_framework import serializers as s
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer


class RegisterUserSerializer(s.ModelSerializer):
    first_name = s.CharField(max_length=88, allow_blank=True, default="")
    last_name = s.CharField(max_length=88, allow_blank=True, default="")
    password2 = s.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ("email", "phone", "first_name", "last_name", "password", "password2")
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, attrs: MutableMapping[str, Any]) -> MutableMapping[str, Any]:
        self._validate_user_name(attrs)
        self._validate_password(attrs)
        return attrs

    def _validate_password(self, attrs: MutableMapping[str, Any]):
        password = attrs.get("password", "")
        password2 = attrs.get("password2", "")
        if password != password2:
            raise s.ValidationError({"password": "Passwords do not match!"})

    def _validate_user_name(self, attrs: MutableMapping[str, Any]):
        email = attrs.get("email", "")
        phone = attrs.get("phone", "")
        if not bool(email) and not bool(phone):
            raise s.ValidationError({"email": "Email or Phone is required!"})

    def validate_phone(self, value: str | None) -> str | None:
        if not bool(value):
            return None

        if not value.isdigit():
            raise s.ValidationError("Phone number must contain only digits")

        # Check for valid BD number with optional country code
        pattern = re.compile(r"^(?:\+88)?(01[3-9]\d{8})$")
        match = pattern.match(value)
        if not match:
            raise s.ValidationError(
                "Phone number must be a valid Bangladeshi number, optionally starting with '+88', "
                "and 11 digits long starting with '01'."
            )

        # Return the number without the country code
        return match.group(1)


class LoginSerializer(s.Serializer):
    user_name = s.CharField()
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
    user_name = s.EmailField()


class ConfirmResetPasswordSerializer(s.Serializer):
    user_name = s.CharField()
    otp_code = s.CharField()
