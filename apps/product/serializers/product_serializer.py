from typing import Any

from rest_framework import serializers as s

from apps.sale_order.models import PaikarSaleOrder
from apps.sale_order.serializers.sale_order_serializer import DateRangeField
from core.constants import AUDIT_COLUMNS

from ..models.product_model import Product, ProductDetail
from .product_brand_serializer import ProductBrandSerializer


def get_related_serializer_data(serializer_class, obj, key, many=False):
    object_key = getattr(obj, key)
    serializer = serializer_class(object_key, many=many)
    return serializer.data


class ProductDetailSerializer(s.ModelSerializer):
    class Meta:
        model = ProductDetail
        exclude = AUDIT_COLUMNS + ("product", "id")


class ProductSerializer(s.ModelSerializer):
    details = ProductDetailSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        exclude = AUDIT_COLUMNS


class ProductExtendedSerializer(s.ModelSerializer):
    brand = ProductBrandSerializer(read_only=True)
    details = ProductDetailSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        exclude = AUDIT_COLUMNS


class ProductCreateSerializer(s.ModelSerializer):
    details = ProductDetailSerializer(write_only=True, many=True)
    brand = ProductBrandSerializer(write_only=True)

    def to_representation(self, instance: "Product") -> dict[str, Any]:
        response = super().to_representation(instance)
        response["uom"] = instance.uom.name
        response["category"] = instance.category.name
        response["brand"] = instance.brand.name if instance.brand else None
        response["origin"] = instance.origin.name if instance.origin else None
        return response

    class Meta:
        model = Product
        exclude = AUDIT_COLUMNS


class ProductUpdateSerializer(s.ModelSerializer):
    details = ProductDetailSerializer(write_only=True, many=True)
    brand = ProductBrandSerializer(write_only=True)

    class Meta:
        model = Product
        exclude = AUDIT_COLUMNS
        read_only_fields = ("slug", "id", "sku_code")


class ProductUpdateStatusSerializer(s.ModelSerializer):
    class Meta:
        model = Product
        fields = ("is_active", "id")


class ProductEcomSerializer(s.ModelSerializer):
    product = ProductSerializer(read_only=True)
    company = s.SerializerMethodField()
    validity_dates = DateRangeField()
    orderlines = s.SerializerMethodField()


    def get_orderlines(self, obj):
        from apps.sale_order.serializers import SaleOrderLineSerializer

        return get_related_serializer_data(SaleOrderLineSerializer, obj, "orderlines", many=True)

    def get_company(self, obj):
        from apps.company.serializers.company_serializer_v1 import CompanySerializer

        return get_related_serializer_data(CompanySerializer, obj, "company")

    class Meta:
        model = PaikarSaleOrder
        exclude = AUDIT_COLUMNS
