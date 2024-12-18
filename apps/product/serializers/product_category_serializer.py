from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers as s

from core.constants.serializer_constant import COMMON_EXCLUDE_FIELDS

from ..models.product_category_model import ProductCategory


class ProductCategorySerializer(s.ModelSerializer):
    name = s.CharField()
    is_active = s.BooleanField()
    parent = s.PrimaryKeyRelatedField(
        queryset=ProductCategory.objects.all(),
    )  # type: ignore
    sub_categories = s.SerializerMethodField()

    @extend_schema_field(s.ListField(child=s.DictField()))
    def get_sub_categories(self, object: ProductCategory):
        childs = object.child_product_categories.select_related("parent").all()
        return self.__class__(instance=childs, many=True).data

    class Meta:
        model = ProductCategory
        exclude = COMMON_EXCLUDE_FIELDS
        read_only_fields = ["is_active", "id"]


class ProductCategoryUpdateStatusSerializer(s.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ("id", "is_active")
