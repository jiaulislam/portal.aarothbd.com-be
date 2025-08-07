from django.contrib import admin
from unfold.admin import TabularInline

from core.admin import BaseAdmin, InlineHelperAdmin
from core.constants.common import AUDIT_COLUMNS

from .models import PurchaseOrder, PurchaseOrderLine


@admin.register(PurchaseOrderLine)
class PurchaseOrderLineAdmin(BaseAdmin):
    list_display = ("purchase_order", "product", "quantity", "trade_price", "mrp")
    search_fields = ("purchase_order__order_number", "product__name")
    list_filter = ("purchase_order__order_date", "product")
    ordering = ("-purchase_order__order_date",)
    readonly_fields = ("created_at", "updated_at")
    exclude = AUDIT_COLUMNS

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("product", "purchase_order")


class PurchaseOrderLineInline(TabularInline, InlineHelperAdmin):
    model = PurchaseOrderLine
    extra = 0
    readonly_fields = ("created_at", "updated_at")
    fields = ("product", "quantity", "trade_price", "mrp")
    show_change_link = True


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(BaseAdmin):
    list_display = ("order_number", "supplier", "order_date", "total_trade_price", "total_margin_amount", "entry_type")
    search_fields = ("order_number", "supplier__name")
    list_filter = ("order_date", "supplier", "entry_type")
    ordering = ("-order_date",)
    readonly_fields = ("order_number",)
    inlines = [PurchaseOrderLineInline]
    exclude = AUDIT_COLUMNS

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("supplier").prefetch_related("order_lines__product")
