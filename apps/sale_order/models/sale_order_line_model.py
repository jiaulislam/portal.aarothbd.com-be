from django.contrib.postgres.fields import IntegerRangeField
from django.db import models

from core.models import BaseModel


class PaikarSaleOrderLine(BaseModel):
    paikar_sale_order = models.ForeignKey("sale_order.PaikarSaleOrder", on_delete=models.CASCADE)
    uom = models.ForeignKey("uom.UoM", on_delete=models.PROTECT)
    quantity_slab = IntegerRangeField()

    rate = models.FloatField(default=0.0)
    share_commission = models.FloatField(default=0.0)
    others_charge = models.FloatField(default=0.0)

    remarks = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.paikar_sale_order.order_number

    class Meta:
        db_table = "sale_order_paikar_sale_order_line"
