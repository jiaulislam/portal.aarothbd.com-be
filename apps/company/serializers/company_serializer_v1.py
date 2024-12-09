from rest_framework import serializers as s
from rest_framework.exceptions import ValidationError

from core.constants.serializer_constant import COMMON_EXCLUDE_FIELDS, STATUS_SERIALIZER_FIELDS

from ..models import Company
from ..serializers.company_configuration_serializer_v1 import CompanyConfigurationSerializer

__all__ = ["CompanySerializer", "CompanyUpdateStatusSerializer"]


class CompanySerializer(s.ModelSerializer):
    slug = s.SlugField(
        allow_null=True,
        allow_blank=True,
        help_text="Backend will create it on null.",
        trim_whitespace=True,
        max_length=255,
    )
    configuration = CompanyConfigurationSerializer(read_only=True)

    class Meta:
        model = Company
        exclude = COMMON_EXCLUDE_FIELDS
        read_only_fields = ("slug", "is_active")


class CompanyUpdateStatusSerializer(s.ModelSerializer):
    class Meta:
        model = Company
        fields = STATUS_SERIALIZER_FIELDS

    def validate(self, data):
        try:
            _ = data["is_active"]
        except KeyError as _:
            raise ValidationError({"is_active": "'is_active' field is required !"}, code="client_error")
        return data
