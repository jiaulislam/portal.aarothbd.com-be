from rest_framework import serializers as s

from core.constants import AUDIT_COLUMNS

from .models import AboutUs


class AboutUsSerializer(s.ModelSerializer):
    class Meta:
        model = AboutUs
        exclude = AUDIT_COLUMNS
