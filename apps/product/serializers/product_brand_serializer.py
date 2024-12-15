from rest_framework import serializers as s

from core.constants.serializer_constant import COMMON_EXCLUDE_FIELDS

from ..models.product_brand_model import ProductBrand


class ProductBrandSerializer(s.ModelSerializer):
    class Meta:
        model = ProductBrand
        exclude = COMMON_EXCLUDE_FIELDS
