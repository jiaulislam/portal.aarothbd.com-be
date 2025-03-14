from typing import Any, MutableMapping

from django.contrib.auth import get_user_model
from rest_framework import serializers as s
from rest_framework.exceptions import ValidationError

from apps.address.serializers import AddressCreateSerializer
from apps.company.serializers.company_serializer_v1 import CompanySerializer

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
    addresses = AddressCreateSerializer(many=True, write_only=True, required=False)

    def _check_password_match(self, password: str, password2: str) -> bool:
        return password == password2

    def validate(self, attrs: MutableMapping[str, Any]) -> MutableMapping[str, Any]:
        if not self._check_password_match(attrs.get("password", ""), attrs.get("password2", "")):
            raise ValidationError({"password": "passwords mismatch. Try again !"}, code="client_error")
        return attrs

    def to_representation(self, instance: User) -> dict[str, Any]:
        response = super().to_representation(instance)
        response["company"] = CompanySerializer(instance=instance.company).data
        return response

    def validate_email(self, value: str | None) -> str | None:
        if get_user_model().objects.filter(email=value).exists():
            raise ValidationError("Email already exists !", code="client_error")
        return value

    def validate_phone(self, value: str | None) -> str | None:
        if get_user_model().objects.filter(phone=value).exists():
            raise ValidationError("Phone number already exists !", code="client_error")
        return value

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "email",
            "phone",
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
            "groups",
            "user_type",
            "addresses",
        ]
        read_only_fields = ("is_active",)


class UserUpdateSerializer(s.ModelSerializer[User]):
    profile = UserProfileSerializer(write_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            "first_name",
            "last_name",
            "profile",
            "groups",
            "company",
            "user_type",
        ]


class UserDetailSerializer(s.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    addresses = s.SerializerMethodField()

    def get_addresses(self, instance: User) -> dict[str, Any]:
        data = AddressCreateSerializer(instance.addresses.all(), many=True).data
        return data

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
        read_only_fields = ("groups", "is_active")


class UserUpdateStatusSerializer(s.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "is_active")

    def validate(self, attrs):
        try:
            _ = attrs["is_active"]
        except KeyError as _:
            raise ValidationError({"is_active": "'is_active' field is required !"}, code="client_error")
        return attrs


class UserChangePasswordSerializer(s.Serializer):
    old_password = s.CharField(required=True)
    new_password = s.CharField(required=True)
    new_password2 = s.CharField(required=True)

    def validate(self, attrs: Any) -> Any:
        if attrs["new_password"] != attrs["new_password2"]:
            raise ValidationError({"new_password": "passwords mismatch. Try again !"}, code="client_error")
        return attrs
