from rest_framework import serializers as s

from core.constants import AUDIT_COLUMNS

from .models import SubDistrict


class SubDistrictSerializer(s.ModelSerializer):
    class Meta:
        model = SubDistrict
        read_only_fields = ("id",)
        exclude = AUDIT_COLUMNS
