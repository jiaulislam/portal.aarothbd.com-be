from django.db import models

from core.models import BaseModel

from ..constants import OrderStatusChoice


class OrderDelivery(BaseModel):
    order = models.ForeignKey(
        "customer_order.Order",
        on_delete=models.CASCADE,
        related_name="deliveries",
    )
    quantity = models.PositiveIntegerField()
    delivery_date = models.DateField()
    delivery_address = models.TextField(null=True, blank=True)
    delivery_status = models.CharField(
        max_length=255,
        choices=OrderStatusChoice.choices,
        default=OrderStatusChoice.PENDING,
    )
    tracking_number = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
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
    order_line = models.ForeignKey("customer_order.OrderLine", on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    amount = models.FloatField(default=1)

    def __str__(self):
        return f"Delivery Line for {self.order_delivery.order.order_number} on {self.order_delivery.delivery_date}"

    class Meta:
        db_table = "customer_order_order_delivery_line"
        verbose_name = "Order Delivery Line"
        verbose_name_plural = "Order Delivery Lines"
        unique_togather = ("order_delivery", "order_line")


class OrderDeliveryBill(BaseModel):
    order_delivery = models.OneToOneField(
        "customer_order.OrderDelivery",
        on_delete=models.CASCADE,
        related_name="bill",
    )
    bill_number = models.CharField(max_length=255, unique=True)
    bill_date = models.DateField()
    total_amount = models.FloatField(default=0.0)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Bill {self.bill_number} for Delivery {self.order_delivery.order.order_number}"

    class Meta:
        db_table = "customer_order_order_delivery_bill"
        verbose_name = "Order Delivery Bill"
        verbose_name_plural = "Order Delivery Bills"
