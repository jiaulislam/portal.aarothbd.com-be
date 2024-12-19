from rest_framework import serializers as s

from core.constants import AUDIT_COLUMNS

from .models import District


class DistrictSerializer(s.ModelSerializer):
    class Meta:
        model = District
        exclude = AUDIT_COLUMNS
