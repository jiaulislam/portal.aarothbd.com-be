from rest_framework import serializers as s

from core.constants.common import AUDIT_COLUMNS
from core.utils import get_serialized_data

from ..models import Offer

__all__ = [
    "OfferListSerializer",
    "OfferCreateUpdateSerializer",
    "OfferRetrieveSerializer",
    "OfferUpdateStatusSerializer",
    "OfferAgreementUpdateSerializer",
]


class OfferListSerializer(s.ModelSerializer):
    company = s.SerializerMethodField()
    product = s.SerializerMethodField()

    def get_company(self, obj: Offer):
        from apps.company.serializers import CompanySerializer

        data = get_serialized_data(CompanySerializer, obj, "company")
        return data

    def get_product(self, obj: Offer):
        from apps.product.serializers.product_serializer import ProductExtendedSerializer

        data = get_serialized_data(ProductExtendedSerializer, obj, "product")
        return data

    class Meta:
        model = Offer
        fields = [
            "id",
            "name",
            "slug",
            "company",
            "product",
            "start_at",
            "end_at",
            "price",
            "offer_price",
            "is_active",
            "company_agreed",
            "agreed_by",
            "agreed_at",
        ]


class OfferRetrieveSerializer(s.ModelSerializer):
    company = s.SerializerMethodField()
    product = s.SerializerMethodField()

    def get_company(self, obj: Offer):
        from apps.company.serializers import CompanySerializer

        data = get_serialized_data(CompanySerializer, obj, "company")
        return data

    def get_product(self, obj: Offer):
        from apps.product.serializers.product_serializer import ProductExtendedSerializer

        data = get_serialized_data(ProductExtendedSerializer, obj, "product")
        return data

    class Meta:
        model = Offer
        exclude = AUDIT_COLUMNS


class OfferCreateUpdateSerializer(s.ModelSerializer):
    id = s.ReadOnlyField()

    class Meta:
        model = Offer
        fields = [
            "id",
            "name",
            "slug",
            "company",
            "product",
            "start_at",
            "end_at",
            "discount_mode",
            "discount_amount",
            "min_qty",
            "max_qty",
            "price",
            "offer_price",
            "comission_mode",
            "comission_amount",
            "uom",
        ]


class OfferUpdateStatusSerializer(s.ModelSerializer):
    id = s.ReadOnlyField()

    class Meta:
        model = Offer
        fields = ["is_active", "id"]


class OfferAgreementUpdateSerializer(s.ModelSerializer):
    company_agreed = s.BooleanField(required=False)
    agreed_by = s.IntegerField(required=False)
    agreed_at = s.DateTimeField(required=False)

    class Meta:
        model = Offer
        fields = ["company_agreed", "agreed_by", "agreed_at"]
