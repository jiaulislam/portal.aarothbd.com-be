from rest_framework import serializers as s

from core.constants.serializer_constant import COMMON_EXCLUDE_FIELDS

from .models import Address


class AddressSerializer(s.ModelSerializer):
    class Meta:
        model = Address
        exclude = COMMON_EXCLUDE_FIELDS
