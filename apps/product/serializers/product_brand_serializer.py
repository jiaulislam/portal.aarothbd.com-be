from rest_framework import serializers as s

from core.constants import AUDIT_COLUMNS

from ..models.product_brand_model import ProductBrand


class ProductBrandSerializer(s.ModelSerializer):
    class Meta:
        model = ProductBrand
        exclude = AUDIT_COLUMNS
