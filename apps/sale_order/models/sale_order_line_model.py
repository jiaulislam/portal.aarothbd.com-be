from django.contrib.postgres.fields import IntegerRangeField
from django.db import models

from core.models import BaseModel


class DiscountTypeChoices(models.TextChoices):
    PERCENTAGE = "percentage", "Percentage"
    FIXED = "fixed", "Fixed"


class PaikarSaleOrderLine(BaseModel):
    paikar_sale_order = models.ForeignKey(
        "sale_order.PaikarSaleOrder",
        on_delete=models.CASCADE,
        related_name="orderlines",
    )
    uom = models.ForeignKey("uom.UoM", on_delete=models.PROTECT)
    quantity_slab = IntegerRangeField()

    rate = models.FloatField(default=0.0)  # rate per unit 80
    share_commission = models.FloatField(default=0.0)
    others_charge = models.FloatField(default=0.0)
    margin_amount = models.FloatField(default=0.0)  # per unit 10
    discount_type = models.CharField(
        max_length=50, choices=DiscountTypeChoices.choices, default=DiscountTypeChoices.PERCENTAGE
    )  # 100
    discount_amount = models.FloatField(default=0.0)
    # customer rate =  (rate + margin_amount) - discount_amount (upon discount type) 8900
    # aarothbd profit =  customer rate - rate 8900 - 8000 = 900

    remarks = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.paikar_sale_order.order_number

    class Meta:
        db_table = "sale_order_paikar_sale_order_line"
