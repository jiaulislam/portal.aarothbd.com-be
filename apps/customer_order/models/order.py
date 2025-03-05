from django.db import models
from django.utils import timezone

from core.models import BaseModel

from ..constants import OrderStatusChoice, PaymentStatusChoice, PaymodeChoice

__all__ = ["Order", "OrderPayment"]


class Order(BaseModel):
    order_number = models.CharField(max_length=255, unique=True, null=True, blank=True)
    order_date = models.DateField(default=timezone.now)

    shipping_method = models.CharField(max_length=255)

    customer_name = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=255)
    customer_email = models.EmailField(max_length=255, null=True, blank=True)
    shipping_address = models.TextField()
    paymode = models.CharField(max_length=255, choices=PaymodeChoice.choices, default=PaymodeChoice.CASH_ON_DELIVERY)

    notes = models.TextField(null=True, blank=True)

    order_status = models.CharField(
        max_length=255, choices=OrderStatusChoice.choices, default=OrderStatusChoice.PENDING
    )
    shipped_date = models.DateField(null=True, blank=True)
    delivered_date = models.DateField(null=True, blank=True)
    payment_status = models.CharField(
        max_length=255,
        choices=PaymentStatusChoice.choices,
        default=PaymentStatusChoice.UNPAID,
    )

    # fees
    shipping_fee = models.FloatField(default=0)
    tax = models.FloatField(default=0)
    discount_amount = models.FloatField(default=0)

    cupon_code = models.ForeignKey("offer.Cupon", on_delete=models.PROTECT, null=True, blank=True)
    order_total = models.FloatField(default=0)
    pay_amount = models.FloatField(default=0)

    paid_amount = models.FloatField(default=0)
    due_amount = models.FloatField(default=0)

    payments: models.QuerySet["OrderPayment"]

    class Meta:
        db_table = "customer_order_order"
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class OrderPayment(BaseModel):
    order = models.ForeignKey("customer_order.Order", on_delete=models.CASCADE, related_name="payments")
    paymode = models.CharField(max_length=255, choices=PaymodeChoice.choices, default=PaymodeChoice.CASH_ON_DELIVERY)
    payment_date = models.DateField(default=timezone.now)
    amount = models.FloatField()
    notes = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "customer_order_order_payment"
        verbose_name = "Order Payment"
        verbose_name_plural = "Order Payments"
