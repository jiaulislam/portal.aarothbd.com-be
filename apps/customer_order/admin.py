from django.contrib import admin
from unfold.admin import TabularInline

from core.admin import BaseAdmin, InlineHelperAdmin
from core.constants import AUDIT_COLUMNS

from .models import Order, OrderLine, OrderPayment


class OrderLineInline(TabularInline, InlineHelperAdmin):
    model = OrderLine
    exclude = AUDIT_COLUMNS
    extra = 0
    verbose_name = "Order Line"
    verbose_name_plural = "Order Lines"


class OrderPaymentAdmin(TabularInline, InlineHelperAdmin):
    model = OrderPayment
    exclude = AUDIT_COLUMNS
    extra = 0
    verbose_name = "Payment"
    verbose_name_plural = "Payments"


@admin.register(Order)
class OrderAdmin(BaseAdmin):
    list_display = (
        "order_number",
        "order_date",
        "customer_name",
        "customer_phone",
        "order_total",
        "paid_amount",
        "due_amount",
        "order_status",
        "payment_status",
    )
    inlines = (OrderLineInline, OrderPaymentAdmin)
