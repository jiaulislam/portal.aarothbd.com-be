from typing import Any, MutableMapping

from django.contrib.auth import get_user_model
from rest_framework import serializers as s
from rest_framework.exceptions import ValidationError

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
    groups = s.PrimaryKeyRelatedField(
        read_only=True,
        many=True,
    )
    profile = UserProfileSerializer(read_only=True)

    def _check_password_match(self, password: str, password2: str) -> bool:
        return password == password2

    def validate(self, data: MutableMapping[str, Any]) -> MutableMapping[str, Any]:
        if not self._check_password_match(data.get("password", ""), data.get("password2", "")):
            raise ValidationError({"password": "passwords mismatch. Try again !"}, code="client_error")
        return data

    class Meta:
        model = get_user_model()
        exclude = [
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
            "is_superuser",
        ]
        read_only_fields = ("groups", "user_permissions")
