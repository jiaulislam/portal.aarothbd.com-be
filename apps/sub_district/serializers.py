from rest_framework import serializers as s

from .models import SubDistrict


class SubDistrictSerializer(s.ModelSerializer):
    class Meta:
        model = SubDistrict
        read_only_fields = ("id",)
        exclude = ("created_at", "updated_at", "created_by", "updated_by")
