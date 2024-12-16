from django.contrib import admin

from core.admin import BaseAdmin
from core.constants.serializer_constant import COMMON_EXCLUDE_FIELDS

from .models.product_brand_model import ProductBrand
from .models.product_category_model import ProductCategory
from .models.product_model import Product, ProductDetail


class ProductDetailInline(admin.TabularInline):
    model = ProductDetail
    extra = 0
    exclude = COMMON_EXCLUDE_FIELDS


@admin.register(ProductBrand)
class ProductBrandAdmin(BaseAdmin):
    list_display = ("name", "origin", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)
    list_editable = ("is_active",)
    list_per_page = 25


@admin.register(ProductCategory)
class ProductCategoryAdmin(BaseAdmin):
    list_display = ("name", "parent", "is_active")
    list_filter = ("name", "parent__name", "is_active")
    search_fields = ("name",)
    list_editable = ("is_active",)
    list_per_page = 25


@admin.register(Product)
class ProductAdmin(BaseAdmin):
    list_display = ("name", "slug", "sku_code", "uom", "category", "has_detail", "is_active")
    list_filter = ("is_active", "has_detail", "uom", "category")
    search_fields = (
        "name",
        "sku_code",
    )
    inlines = (ProductDetailInline,)
    list_per_page = 25
    list_editable = ("is_active",)
