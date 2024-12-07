from rest_framework import serializers as s

from core.constants.serializer_constant import COMMON_EXCLUDE_FIELDS

from ..models import CompanyConfiguration

__all__ = ["CompanyConfigurationSerializer"]


class CompanyConfigurationSerializer(s.ModelSerializer):
    class Meta:
        model = CompanyConfiguration
        exclude = COMMON_EXCLUDE_FIELDS + ("company", "created_at", "updated_at")
