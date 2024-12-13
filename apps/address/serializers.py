from rest_framework import serializers as s

from core.constants.serializer_constant import COMMON_EXCLUDE_FIELDS

from .models import Address


class AddressSerializer(s.ModelSerializer):
    class Meta:
        model = Address
        exclude = COMMON_EXCLUDE_FIELDS


class AddressCreateSerializer(s.ModelSerializer):
    class Meta:
        model = Address
        exclude = ("object_id", "content_type", "created_at", "updated_at", "created_by", "updated_by", "is_active")
