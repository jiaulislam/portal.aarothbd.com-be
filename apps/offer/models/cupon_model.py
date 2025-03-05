from django.db import models

from core.models import BaseModel

from ..constants import DiscountPriceMode

__all__ = ["Cupon"]


class Cupon(BaseModel):
    cupon_code = models.CharField(max_length=255)
    discount_mode = models.CharField(
        max_length=255,
        choices=DiscountPriceMode.choices,
        help_text="decide how the amount should deduct",
    )
    discount_amount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.cupon_code

    def save(self, *args, **kwargs):
        # overriding the django default save method to properly capitalize the cupon code
        self.cupon_code = self.cupon_code.upper()
        super().save(*args, **kwargs)

    def get_discount_amount(self, total_amount: float) -> float:
        if self.discount_mode == DiscountPriceMode.FIXED:
            return self.discount_amount
        return (self.discount_amount / 100) * total_amount

    class Meta:
        db_table = "offer_cupon"
        verbose_name = "Cupon"
        verbose_name_plural = "Cupons"
