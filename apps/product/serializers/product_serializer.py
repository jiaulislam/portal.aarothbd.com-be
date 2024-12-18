from rest_framework import serializers as s

from core.constants.serializer_constant import COMMON_EXCLUDE_FIELDS

from ..models.product_model import Product, ProductDetail
from ..serializers.product_brand_serializer import ProductBrandSerializer


class ProductDetailSerializer(s.ModelSerializer):
    class Meta:
        model = ProductDetail
        exclude = COMMON_EXCLUDE_FIELDS + ("product", "id")


class ProductSerializer(s.ModelSerializer):
    details = ProductDetailSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        exclude = COMMON_EXCLUDE_FIELDS


class ProductExtendedSerializer(s.ModelSerializer):
    brand = ProductBrandSerializer(read_only=True)
    details = ProductDetailSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        exclude = COMMON_EXCLUDE_FIELDS


class ProductCreateSerializer(s.ModelSerializer):
    details = ProductDetailSerializer(write_only=True, many=True)
    brand = ProductBrandSerializer(write_only=True)

    class Meta:
        model = Product
        exclude = COMMON_EXCLUDE_FIELDS


class ProductUpdateSerializer(s.ModelSerializer):
    details = ProductDetailSerializer(write_only=True, many=True)
    brand = ProductBrandSerializer(write_only=True)

    class Meta:
        model = Product
        exclude = COMMON_EXCLUDE_FIELDS
        read_only_fields = ("slug", "id", "sku_code")


class ProductUpdateStatusSerializer(s.ModelSerializer):
    class Meta:
        model = Product
        fields = ("is_active", "id")
