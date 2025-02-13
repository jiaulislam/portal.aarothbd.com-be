from django.contrib import admin
from unfold.admin import TabularInline

from core.admin import BaseAdmin, InlineHelperAdmin
from core.constants.common import AUDIT_COLUMNS

from .models import PaikarSaleOrder, PaikarSaleOrderLine


class PaikarSaleOrderDetailInline(TabularInline, InlineHelperAdmin):
    model = PaikarSaleOrderLine
    extra = 0
    exclude = AUDIT_COLUMNS
    show_change_link = True
    verbose_name = "Order Line"
    verbose_name_plural = "Order Lines"


@admin.register(PaikarSaleOrderLine)
class PaikarSaleOrderDetailAdmin(BaseAdmin):
    list_display = ("id", "uom", "quantity_slab", "rate")


@admin.register(PaikarSaleOrder)
class PaikarSaleOrderAdmin(BaseAdmin):
    list_display = (
        "order_number",
        "order_date",
        "product",
        "product_grade",
        "company",
        "validity_dates",
        "status",
    )
    list_filter = (
        "status",
        "company__name",
    )
    search_fields = ("order_number",)
    readonly_fields = AUDIT_COLUMNS
    inlines = (PaikarSaleOrderDetailInline,)
