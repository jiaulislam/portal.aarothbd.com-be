from rest_framework import serializers as s

from core.constants import COMMON_EXCLUDE_FIELDS

from ..models import CompanyConfiguration


class CompanyConfigurationCreateSerializer(s.ModelSerializer):
    class Meta:
        model = CompanyConfiguration
        exclude = COMMON_EXCLUDE_FIELDS + ("company", "created_at", "updated_at")
