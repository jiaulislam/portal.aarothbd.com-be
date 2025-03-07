from rest_framework import serializers as s

from ..models import ProductImage

__all__ = ["ProductImageSerializer"]


class ProductImageSerializer(s.ModelSerializer):
    id = s.ReadOnlyField()

    class Meta:
        model = ProductImage
        fields = (
            "id",
            "product",
            "sale_order",
            "image",
            "is_default",
        )
