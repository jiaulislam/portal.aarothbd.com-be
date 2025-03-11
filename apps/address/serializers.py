from rest_framework import serializers as s

from core.constants.common import AUDIT_COLUMNS

from .models import Address


class AddressSerializer(s.ModelSerializer):
    class Meta:
        model = Address
        exclude = (
            "object_id",
            "content_type",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
            "is_active",
        ) + AUDIT_COLUMNS
        read_only_fields = ("id", "is_active")


class AddressCreateSerializer(s.ModelSerializer):
    class Meta:
        model = Address
        exclude = (
            "object_id",
            "content_type",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
            "is_active",
        ) + AUDIT_COLUMNS
