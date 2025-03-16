from rest_framework import serializers as s

from core.constants import AUDIT_COLUMNS

from .models import BusinessPartner


class BusinessPartnerSerializer(s.ModelSerializer):
    class Meta:
        model = BusinessPartner
        exclude = AUDIT_COLUMNS
