from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from apps.address.models import Address
from core.models import BaseModel

__all__ = ["Company"]


class Company(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)
    bin_number = models.CharField(max_length=255, null=True, blank=True)
    tin_number = models.CharField(max_length=255, null=True, blank=True)
    theme_color = models.CharField(max_length=255, default="221.2 83.2% 53.3%")
    company_logo = models.ImageField(upload_to="media/company/logos", null=True, blank=True)
    company_favico = models.ImageField(upload_to="media/company/favicos", null=True, blank=True)
    addresses = GenericRelation(Address, related_query_name="company_addresses")

    notes = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "company_company"
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self) -> str:
        return self.name
