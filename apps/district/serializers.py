from rest_framework import serializers as s

from .models import District


class DistrictSerializer(s.ModelSerializer):
    class Meta:
        model = District
        exclude = ("created_at", "updated_at", "created_by", "updated_by")
