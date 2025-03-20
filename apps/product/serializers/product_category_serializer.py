from django.db.models import Prefetch
from rest_framework import serializers as s

from core.constants import AUDIT_COLUMNS

from ..models.product_category_model import ProductCategory


class ProductCategorySerializer(s.ModelSerializer):
    name = s.CharField()
    is_active = s.BooleanField()
    childrens = s.SerializerMethodField()

    def get_childrens(self, object: ProductCategory):
        childrens = object.child_product_categories.prefetch_related(
            Prefetch(
                "child_product_categories",
                queryset=object.child_product_categories.all(),
                to_attr="childrens",
            )
        )
        return ProductCategorySerializer(instance=childrens, many=True).data

    class Meta:
        model = ProductCategory
        exclude = AUDIT_COLUMNS
        read_only_fields = ["is_active", "id"]


class ProductCategoryCreateSerializer(s.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ("name", "parent", "category_image")


class ProductCategoryUpdateStatusSerializer(s.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ("id", "is_active")
