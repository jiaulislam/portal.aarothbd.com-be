from rest_framework import serializers as s
from rest_framework.exceptions import ValidationError

from apps.address.serializers import AddressCreateSerializer, AddressSerializer
from apps.product.models.product_model import Product
from apps.product.serializers.product_serializer import ProductSerializer
from core.constants import COMMON_EXCLUDE_FIELDS, STATUS_SERIALIZER_FIELDS

from ..models import Company
from ..serializers.company_configuration_serializer_v1 import CompanyConfigurationCreateSerializer


class CompanySerializer(s.ModelSerializer):
    slug = s.SlugField(
        allow_null=True,
        allow_blank=True,
        help_text="Backend will create it on null.",
        trim_whitespace=True,
        max_length=255,
    )
    configuration = CompanyConfigurationCreateSerializer(read_only=True)

    class Meta:
        model = Company
        exclude = COMMON_EXCLUDE_FIELDS
        read_only_fields = ("slug", "is_active")


class CompanyCreateSerializer(s.ModelSerializer):
    configuration = CompanyConfigurationCreateSerializer(write_only=True, required=False)
    addresses = AddressCreateSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = Company
        exclude = COMMON_EXCLUDE_FIELDS
        read_only_fields = ("id", "slug", "is_active")


class CompanyUpdateSerializer(s.ModelSerializer):
    allowed_products = s.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True)

    class Meta:
        model = Company
        exclude = COMMON_EXCLUDE_FIELDS
        read_only_fields = ("id", "slug", "is_active")


class CompanyDetailSerializer(s.ModelSerializer):
    addresses = s.SerializerMethodField()
    allowed_products = s.SerializerMethodField()

    def get_allowed_products(self, obj: Company):
        return ProductSerializer(obj.allowed_products.all(), many=True).data

    def get_addresses(self, obj):
        return AddressSerializer(instance=obj.addresses.filter(is_active=True), many=True).data

    class Meta:
        model = Company
        exclude = COMMON_EXCLUDE_FIELDS


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
