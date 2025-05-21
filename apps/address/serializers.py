from rest_framework import serializers as s

from apps.country.serializers import CountrySerializer
from apps.district.serializers import DistrictSerializer
from apps.division.serializers import DivisionSerializer
from apps.sub_district.serializers import SubDistrictSerializer
from core.constants.common import AUDIT_COLUMNS

from .models import Address


class AddressSerializer(s.ModelSerializer):
    class Meta:
        model = Address
        exclude = (
            "object_id",
            "content_type",
            "is_active",
        ) + AUDIT_COLUMNS
        read_only_fields = ("id", "is_active")


class AddressCreateSerializer(s.ModelSerializer):
    class Meta:
        model = Address
        exclude = (
            "object_id",
            "content_type",
            "is_active",
        ) + AUDIT_COLUMNS


class AddressRetrieveSerializer(s.ModelSerializer):
    sub_district = SubDistrictSerializer(read_only=True)
    district = DistrictSerializer(read_only=True)
    division = DivisionSerializer(read_only=True)
    country = CountrySerializer(read_only=True)

    class Meta:
        model = Address
        exclude = (
            "object_id",
            "content_type",
            "is_active",
        ) + AUDIT_COLUMNS
        read_only_fields = ("id", "is_active")
