from django.db import models

from core.models import BaseModel

from ..constants import DiscountPriceMode

__all__ = ["Offer"]


class Offer(BaseModel):
    name = models.CharField(max_length=255)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    discount_mode = models.CharField(
        max_length=255,
        choices=DiscountPriceMode.choices,
        help_text="decide how the amount should deduct",
    )
    discount_amount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "offer_offer"
        verbose_name = "Offer"
        verbose_name_plural = "Offers"
