from rest_framework import serializers as s

from core.constants import AUDIT_COLUMNS

from .models import Banner


class BannerSerializer(s.ModelSerializer):
    class Meta:
        model = Banner
        exclude = AUDIT_COLUMNS
