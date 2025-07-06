from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from django.db import models

from core.models import BaseModel

from ..constants import OrderStatusChoice

if TYPE_CHECKING:
    from apps.company.models import Company
    from apps.customer_order.models import Order, OrderLine


__all__ = ["OrderDelivery", "OrderDeliveryLine", "OrderDeliveryBill"]


class OrderDelivery(BaseModel):
    order: Order = models.ForeignKey(
        "customer_order.Order",
        on_delete=models.CASCADE,
        related_name="deliveries",
    )
    quantity: int = models.PositiveIntegerField()
    delivery_date: models.DateField = models.DateField()
    delivery_address: Optional[str] = models.TextField(null=True, blank=True)
    delivery_status: str = models.CharField(
        max_length=255,
        choices=OrderStatusChoice.choices,
        default=OrderStatusChoice.PENDING,
    )
    tracking_number: Optional[str] = models.CharField(max_length=255, null=True, blank=True)
    return_for_delivery: models.QuerySet[OrderDelivery] = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="return_deliveries"
    )
    delivery_lines: models.QuerySet[OrderDeliveryLine]
    bill: OrderDeliveryBill

    def __str__(self) -> str:
        return f"Delivery for {self.order.order_number} on {self.delivery_date}"

    class Meta:
        db_table = "customer_order_order_delivery"
        verbose_name = "Order Delivery"
        verbose_name_plural = "Order Deliveries"
        unique_together = ("order", "tracking_number")


class OrderDeliveryLine(BaseModel):
    order_delivery = models.ForeignKey(
        "customer_order.OrderDelivery",
        on_delete=models.CASCADE,
        related_name="delivery_lines",
    )
    order_line: OrderLine = models.ForeignKey(
        "customer_order.OrderLine", on_delete=models.PROTECT, related_name="delivery_lines"
    )
    quantity: int = models.PositiveIntegerField(default=1)
    company: Company = models.ForeignKey(
        "company.Company", on_delete=models.PROTECT, related_name="order_delivery_lines"
    )
    rate: float = models.FloatField(default=0)
    margin_amount: float = models.FloatField(default=0)
    customer_price: float = models.FloatField(default=0)
    profit_margin: float = models.FloatField(default=0)
    total_amount: float = models.FloatField(default=1)

    def __str__(self) -> str:
        return f"Delivery Line for {self.order_delivery.order.order_number} on {self.order_delivery.delivery_date}"

    class Meta:
        db_table = "customer_order_order_delivery_line"
        verbose_name = "Order Delivery Line"
        verbose_name_plural = "Order Delivery Lines"
        unique_together = ("order_delivery", "order_line")


class OrderDeliveryBill(BaseModel):
    order_delivery: OrderDelivery = models.OneToOneField(
        "customer_order.OrderDelivery",
        on_delete=models.CASCADE,
        related_name="bill",
    )
    bill_number: str = models.CharField(max_length=255, unique=True)
    bill_date: models.DateField = models.DateField()
    total_amount: float = models.FloatField(default=0.0)
    notes: Optional[str] = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f"Bill {self.bill_number} for Delivery {self.order_delivery.order.order_number}"

    class Meta:
        db_table = "customer_order_order_delivery_bill"
        verbose_name = "Order Delivery Bill"
        verbose_name_plural = "Order Delivery Bills"
