from rest_framework import serializers as s

from core.constants import AUDIT_COLUMNS

from .models import Division


class DivisionSerializer(s.ModelSerializer):
    class Meta:
        model = Division
        read_only_fields = ("id",)
        exclude = AUDIT_COLUMNS
