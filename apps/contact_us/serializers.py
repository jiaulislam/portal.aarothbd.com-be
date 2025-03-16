from rest_framework import serializers as s

from core.constants import AUDIT_COLUMNS

from .models import ContactUs


class ContactUsSerializer(s.ModelSerializer):
    class Meta:
        model = ContactUs
        exclude = AUDIT_COLUMNS
