from django.contrib import admin
from unfold.admin import TabularInline

from core.admin import BaseAdmin, InlineHelperAdmin
from core.constants import AUDIT_COLUMNS

from .models import ProductImage
from .models.product_brand_model import ProductBrand
from .models.product_category_model import ProductCategory
from .models.product_model import Product, ProductDetail


class ProductDetailInline(TabularInline, InlineHelperAdmin):  # type: ignore
    model = ProductDetail
    extra = 0
    exclude = AUDIT_COLUMNS
    max_num = 1
    show_change_link = True


class ProductImageInline(TabularInline, InlineHelperAdmin):  # type: ignore
    model = ProductImage
    extra = 0
    exclude = AUDIT_COLUMNS
    show_change_link = True


class ProductCategoryInline(TabularInline, InlineHelperAdmin):  # type: ignore
    model = ProductCategory
    extra = 0
    exclude = AUDIT_COLUMNS
    show_change_link = True
    fk_name = "parent"


@admin.register(ProductDetail)
class ProductDetailAdmin(BaseAdmin):
    pass


@admin.register(ProductBrand)
class ProductBrandAdmin(BaseAdmin):
    list_display = ("name", "origin", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)
    list_editable = ("is_active",)
    readonly_fields = AUDIT_COLUMNS


@admin.register(ProductCategory)
class ProductCategoryAdmin(BaseAdmin):
    list_display = ("name", "parent", "is_active")
    list_filter = ("name", "parent__name", "is_active")
    search_fields = ("name",)
    list_editable = ("is_active",)
    readonly_fields = AUDIT_COLUMNS
    inlines = (ProductCategoryInline,)


@admin.register(Product)
class ProductAdmin(BaseAdmin):
    list_display = ("name", "slug", "sku_code", "uom", "category", "has_detail", "is_active")
    list_filter = ("is_active", "has_detail", "uom", "category")
    search_fields = (
        "name",
        "sku_code",
    )
    inlines = (ProductDetailInline, ProductImageInline)
    list_editable = ("is_active",)
    readonly_fields = AUDIT_COLUMNS
