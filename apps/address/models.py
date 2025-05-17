from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from core.models.base_model import BaseModel

from .types import AddressType


class Address(BaseModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    line_1 = models.TextField(null=True, blank=True)
    line_2 = models.TextField(null=True, blank=True)

    sub_district = models.ForeignKey(
        "sub_district.SubDistrict",
        on_delete=models.PROTECT,
        related_name="address_sub_districts",
        null=True,
        blank=True,
    )
    district = models.ForeignKey("district.District", on_delete=models.PROTECT, related_name="address_districts")
    division = models.ForeignKey("division.Division", on_delete=models.PROTECT, related_name="address_divisions")
    country = models.ForeignKey("country.Country", on_delete=models.PROTECT, related_name="address_countries")
    address_type = models.CharField(max_length=80, choices=AddressType.choices, default=AddressType.GENERAL)
    is_default = models.BooleanField(default=False)

    class Meta:
        db_table = "address_address"
        verbose_name_plural = "Addresses"
        verbose_name = "Address"
        ordering = ["-id"]
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def __str__(self) -> str:
        return f"{str(self.pk)} / {self.line_1} / {self.line_2}"
