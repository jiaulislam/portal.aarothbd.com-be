from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from core.models import BaseModel

from ..constants import DiscountPriceMode

__all__ = ["Offer"]


class Offer(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, null=True, blank=True, unique=True)
    company = models.ForeignKey("company.Company", on_delete=models.DO_NOTHING, related_name="offers")
    product = models.ForeignKey("product.Product", on_delete=models.DO_NOTHING, related_name="offers")
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    discount_mode = models.CharField(
        max_length=255,
        choices=DiscountPriceMode.choices,
        help_text="decide how the amount should deduct",
    )
    discount_amount = models.PositiveIntegerField(default=0)
    commission_mode = models.CharField(max_length=255, choices=DiscountPriceMode.choices, null=True, blank=True)
    comission_amount = models.IntegerField(default=0)
    min_qty = models.IntegerField(default=0)
    max_qty = models.IntegerField(default=0)
    uom = models.ForeignKey("uom.UoM", on_delete=models.DO_NOTHING, related_name="offers", null=True, blank=True)
    price = models.FloatField(default=0)
    offer_price = models.FloatField(default=0)  # auto calculated pre-save

    company_agreed = models.BooleanField(default=False)
    agreed_by = models.ForeignKey(
        "user.User",
        on_delete=models.DO_NOTHING,
        related_name="offers",
        null=True,
        blank=True,
    )
    agreed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "offer_offer"
        verbose_name = "Offer"
        verbose_name_plural = "Offers"


@receiver(pre_save, sender=Offer)
def generate_slug(sender, instance: Offer, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)
        counter = 1
        original_slug = instance.slug
        while Offer.objects.filter(slug=instance.slug).exists():
            instance.slug = f"{original_slug}-{counter}"
            counter += 1

    if instance.discount_mode == DiscountPriceMode.FIXED:
        instance.offer_price = instance.price - instance.discount_amount

    if instance.discount_mode == DiscountPriceMode.PERCENTAGE:
        instance.offer_price = instance.price * instance.offer_price // 100
