from django_filters import filters

from core.constants.common import COMMON_EXCLUDE_FIELDS
from core.filter import BaseFilter

from .models.product_brand_model import ProductBrand
from .models.product_category_model import ProductCategory
from .models.product_model import Product


class ProductFilter(BaseFilter):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Product
        fields = ("sku_code", "uom", "category", "brand", "origin", "name")


class ProductBrandFilter(BaseFilter):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = ProductBrand
        exclude = COMMON_EXCLUDE_FIELDS


class ProductCategoryFilter(BaseFilter):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = ProductCategory
        exclude = COMMON_EXCLUDE_FIELDS + ("category_image",)


class ECommProductFilter(BaseFilter):
    category = filters.CharFilter(field_name="product__category__slug", lookup_expr="exact")
    brand = filters.CharFilter(field_name="product__brand__name", lookup_expr="exact")
    rate_min = filters.NumberFilter(field_name="orderlines__rate", lookup_expr="gte")
    rate_max = filters.NumberFilter(field_name="orderlines__rate", lookup_expr="lte")
