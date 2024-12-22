from django_filters import filters

from core.filter import BaseFilter

from .models.product_model import Product


class ProductFilter(BaseFilter):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Product
        fields = ("sku_code", "uom", "category", "brand", "origin", "name")
