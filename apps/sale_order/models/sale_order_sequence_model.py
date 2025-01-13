from django.db import models
from django.utils import timezone

from core.models import BaseModel

from ..constants import SaleOrderPrefixChoices


class SaleOrderSequence(BaseModel):
    prefix = models.CharField(max_length=10, choices=SaleOrderPrefixChoices.choices)
    sequence_date = models.DateField(default=timezone.now)
    counter = models.IntegerField(default=0)

    def __str__(self):
        return self.prefix

    def get_order_number(self):
        return f"{self.prefix}{self.sequence_date.strftime('%Y%m%d')}{self.counter:04d}"

    class Meta:
        db_table = "sale_order_sale_order_sequence"
        unique_together = ("prefix", "sequence_date")
