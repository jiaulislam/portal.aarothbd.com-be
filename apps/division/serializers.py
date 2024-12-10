from rest_framework import serializers as s

from .models import Division


class DivisionSerializer(s.ModelSerializer):
    class Meta:
        model = Division
        read_only_fields = ("id",)
        exclude = ("created_at", "updated_at", "created_by", "updated_by")
