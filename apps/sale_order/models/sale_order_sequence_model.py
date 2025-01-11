from django.db import models
from django.utils import timezone

from core.models import BaseModel

from ..constants import SaleOrderPrefixChoices


class SaleOrderSequence(BaseModel):
    prefix = models.CharField(max_length=10, choices=SaleOrderPrefixChoices.choices)
    sequence_date = models.DateField(default=timezone.now)
    counter = models.IntegerField(default=1)

    def __str__(self):
        return self.prefix

    class Meta:
        db_table = "sale_order_sale_order_sequence"
        unique_together = ("prefix", "sequence_date")
