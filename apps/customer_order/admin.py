from django.contrib import admin
from unfold.admin import StackedInline, TabularInline

from core.admin import BaseAdmin, InlineHelperAdmin
from core.constants import AUDIT_COLUMNS

from .models import Order, OrderDelivery, OrderDeliveryBill, OrderDeliveryLine, OrderLine, OrderPayment


class OrderLineInline(StackedInline, InlineHelperAdmin):
    model = OrderLine
    exclude = AUDIT_COLUMNS
    extra = 0
    show_change_link = True
    verbose_name = "Order Line"
    verbose_name_plural = "Order Lines"


@admin.register(OrderLine)
class OrderLineAdmin(BaseAdmin):
    model = OrderLine
    exclude = AUDIT_COLUMNS
    extra = 0
    editable = True
    verbose_name = "Order Line"
    verbose_name_plural = "Order Lines"


class OrderPaymentInlineAdmin(TabularInline, InlineHelperAdmin):
    model = OrderPayment
    exclude = AUDIT_COLUMNS
    extra = 0
    show_change_link = True
    verbose_name = "Payment"
    verbose_name_plural = "Payments"


@admin.register(OrderPayment)
class OrderPaymentAdmin(BaseAdmin):
    model = OrderPayment
    exclude = AUDIT_COLUMNS
    extra = 0
    editable = True
    verbose_name = "Order Payment"
    verbose_name_plural = "Order Payments"


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
    inlines = (OrderLineInline, OrderPaymentInlineAdmin)


class OrderDeliveryLineInline(StackedInline, InlineHelperAdmin):
    model = OrderDeliveryLine
    exclude = AUDIT_COLUMNS
    extra = 0
    show_change_link = True
    verbose_name = "Delivery Line"
    verbose_name_plural = "Delivery Lines"


class OrderDeliveryBillInline(StackedInline, InlineHelperAdmin):
    model = OrderDeliveryBill
    exclude = AUDIT_COLUMNS
    extra = 0
    show_change_link = True
    verbose_name = "Delivery Bill"
    verbose_name_plural = "Delivery Bills"


@admin.register(OrderDelivery)
class OrderDeliveryAdmin(BaseAdmin):
    list_display = (
        "order",
        "delivery_date",
        "delivery_status",
        "tracking_number",
    )
    search_fields = ("order__order_number", "tracking_number")
    inlines = (OrderDeliveryLineInline, OrderDeliveryBillInline)
