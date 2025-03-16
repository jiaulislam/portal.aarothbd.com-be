from django.db import models

from core.models import BaseModel
from core.storage_config import upload_logos


class BusinessPartner(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField(null=True, blank=True)
    logo = models.ImageField(upload_to=upload_logos)

    class Meta:
        db_table = "business_partner_business_partner"
        verbose_name = "Business Partner"
        verbose_name_plural = "Business Partners"

    def __str__(self):
        return self.name
