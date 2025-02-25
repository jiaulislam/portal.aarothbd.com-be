from django.contrib.postgres.fields import DateRangeField
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify

from core.models import BaseModel

from ..constants import SaleOrderStatusChoices


class PaikarSaleOrder(BaseModel):
    order_number = models.CharField(max_length=255, unique=True)
    order_date = models.DateField(default=timezone.now)

    product = models.ForeignKey(
        "product.Product",
        on_delete=models.PROTECT,
        related_name="paikar_sale_orders",
    )
    product_grade = models.CharField(max_length=88, null=True, blank=True)

    company = models.ForeignKey(
        "company.Company",
        on_delete=models.PROTECT,
        related_name="paikar_sale_orders",
    )

    validity_dates = DateRangeField(null=True, blank=True)

    has_vat = models.BooleanField(default=False)
    vat_ratio = models.FloatField(default=0.0, help_text="VAT ratio in percentage if has VAT")

    approved_on = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(
        "user.User",
        on_delete=models.PROTECT,
        related_name="paikar_sale_order_approved_set",
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=50,
        choices=SaleOrderStatusChoices.choices,
        default=SaleOrderStatusChoices.APPROVAL_PENDING,
    )

    remarks = models.CharField(max_length=255, null=True, blank=True)

    ecomm_identifier = models.CharField(null=True, blank=True, max_length=255, unique=True)

    def __str__(self):
        return self.order_number

    class Meta:
        db_table = "sale_order_paikar_sale_order"
        verbose_name = "Paikar Sale Order"
        verbose_name_plural = "Paikar Sale Orders"


@receiver(pre_save, sender=PaikarSaleOrder)
def generate_slug(sender, instance: PaikarSaleOrder, **kwargs):
    if not instance.ecomm_identifier:
        instance.ecomm_identifier = f"{instance.product.slug}-{slugify(instance.pk)}"
        counter = 1
        original_slug = instance.ecomm_identifier
        while PaikarSaleOrder.objects.filter(ecomm_identifier=instance.ecomm_identifier).exists():
            instance.ecomm_identifier = f"{original_slug}-{counter}"
            counter += 1
