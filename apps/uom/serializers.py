from rest_framework import serializers as s

from core.constants import AUDIT_COLUMNS

from .models import UoM, UoMCategory


class UoMCategorySerializer(s.ModelSerializer):
    class Meta:
        model = UoMCategory
        exclude = AUDIT_COLUMNS


class UoMSerializer(s.ModelSerializer):
    class Meta:
        model = UoM
        exclude = AUDIT_COLUMNS
