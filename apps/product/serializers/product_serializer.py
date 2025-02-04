from typing import Any

from rest_framework import serializers as s

from core.constants import AUDIT_COLUMNS

from ..models.product_model import Product, ProductDetail
from .product_brand_serializer import ProductBrandSerializer
from .product_category_serializer import ProductCategorySerializer


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
    brand = ProductBrandSerializer(read_only=True)
    details = ProductDetailSerializer(read_only=True, many=True)
    uom = s.SerializerMethodField()
    category = ProductCategorySerializer(read_only=True)
    origin = s.SerializerMethodField()
    sale_orders = s.SerializerMethodField()

    def get_sale_orders(self, obj):
        from apps.sale_order.serializers.sale_order_serializer import (
            PaikarSaleOrderDetailSerializer,
        )

        return get_related_serializer_data(PaikarSaleOrderDetailSerializer, obj, "paikar_sale_order_product", many=True)

    def get_uom(self, obj):
        from apps.uom.serializers import UoMSerializer

        return get_related_serializer_data(UoMSerializer, obj, "uom")

    def get_category(self, obj):
        from .product_category_serializer import ProductCategorySerializer

        return get_related_serializer_data(ProductCategorySerializer, obj, "category")

    def get_origin(self, obj):
        from apps.country.serializers import CountrySerializer

        return get_related_serializer_data(CountrySerializer, obj, "origin")

    class Meta:
        model = Product
        exclude = AUDIT_COLUMNS
