from django.contrib.postgres.fields import DateRangeField
from django.db import models
from django.utils import timezone

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

    def __str__(self):
        return self.order_number

    class Meta:
        db_table = "sale_order_paikar_sale_order"
        verbose_name = "Paikar Sale Order"
        verbose_name_plural = "Paikar Sale Orders"
