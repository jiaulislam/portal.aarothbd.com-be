from rest_framework import serializers as s

from .models import Country


class CountrySerializer(s.ModelSerializer):

    class Meta:
        model = Country
        read_only_fields = ("id", "full_name", "created_at", "updated_at", "created_by", "updated_by")
        exclude = ("created_at", "updated_at", "created_by", "updated_by")
