from django.contrib import admin

from core.admin import BaseAdmin
from core.constants.serializer_constant import COMMON_EXCLUDE_FIELDS

from .models.product import Product, ProductDetail
from .models.product_brand import ProductBrand
from .models.product_category import ProductCategory


class ProductDetailInline(admin.TabularInline):
    model = ProductDetail
    extra = 0
    exclude = COMMON_EXCLUDE_FIELDS

@admin.register(ProductBrand)
class ProductBrandAdmin(BaseAdmin):
    list_display = ("name", "origin", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(ProductCategory)
class ProductCategoryAdmin(BaseAdmin):
    list_display = ("name", "parent", "is_active")
    list_filter = ("name", "parent__name", "is_active")
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(BaseAdmin):
    list_display = ("name", "sku_code", "uom", "category", "has_detail")
    list_filter = ("is_active", "uom", "uom__category__name")
    search_fields = ("name", )
    inlines = (ProductDetailInline,)
