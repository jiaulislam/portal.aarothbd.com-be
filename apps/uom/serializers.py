from rest_framework import serializers as s

from core.constants.serializer_constant import COMMON_EXCLUDE_FIELDS

from .models import UoM, UoMCategory


class UoMCategorySerializer(s.ModelSerializer):
    class Meta:
        model = UoMCategory
        exclude = COMMON_EXCLUDE_FIELDS


class UoMSerializer(s.ModelSerializer):
    class Meta:
        model = UoM
        exclude = COMMON_EXCLUDE_FIELDS
