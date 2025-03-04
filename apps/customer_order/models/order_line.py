from django.db import models

from core.models import BaseModel

__all__ = ["OrderLine"]


class OrderLine(BaseModel):
    order = models.ForeignKey(
        "customer_order.Order",
        on_delete=models.CASCADE,
        related_name="order_lines",
    )
    sale_order = models.ForeignKey("sale_order.PaikarSaleOrder", on_delete=models.PROTECT, null=True, blank=True)
    sale_order_line = models.ForeignKey(
        "sale_order.PaikarSaleOrderLine", on_delete=models.PROTECT, null=True, blank=True
    )
    offer_sale_order = models.ForeignKey("offer.Offer", on_delete=models.PROTECT, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    discount_amount = models.FloatField(default=0)
    sub_total = models.FloatField(default=0)

    class Meta:
        db_table = "customer_order_order_line"
        verbose_name = "Order Line"
        verbose_name_plural = "Order Lines"
