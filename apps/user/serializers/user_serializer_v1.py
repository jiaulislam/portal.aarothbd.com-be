from typing import Any, MutableMapping

from django.contrib.auth import get_user_model
from rest_framework import serializers as s
from rest_framework.exceptions import ValidationError

from ...company.serializers.company_serializer_v1 import CompanySerializer
from ..models import User, UserProfile


class UserProfileSerializer(s.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ("user",)


class UserSerializer(s.ModelSerializer[User]):
    password = s.CharField(write_only=True)
    password2 = s.CharField(write_only=True, allow_null=False, allow_blank=False)
    date_joined = s.DateTimeField(read_only=True)
    is_admin = s.BooleanField(read_only=True)
    last_login = s.DateTimeField(read_only=True)

    profile = UserProfileSerializer(read_only=True)
    company = CompanySerializer(read_only=True)

    def _check_password_match(self, password: str, password2: str) -> bool:
        return password == password2

    def validate(self, data: MutableMapping[str, Any]) -> MutableMapping[str, Any]:
        if not self._check_password_match(data.get("password", ""), data.get("password2", "")):
            raise ValidationError({"password": "passwords mismatch. Try again !"}, code="client_error")
        return data

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "is_admin",
            "date_joined",
            "is_active",
            "password",
            "password2",
            "profile",
            "company",
            "last_login",
        ]
        read_only_fields = ("is_active",)


class UserDetailSerializer(s.ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = [
            "password",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
            "is_superuser",
        ]
        read_only_fields = ("groups", "user_permissions", "is_active")


class UserUpdateStatusSerializer(s.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "is_active")

    def validate(self, data):
        try:
            _ = data["is_active"]
        except KeyError as _:
            raise ValidationError({"is_active": "'is_active' field is required !"}, code="client_error")
        return data
