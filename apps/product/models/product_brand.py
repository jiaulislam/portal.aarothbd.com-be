from django.db import models

from core.models import BaseModel


class ProductBrand(BaseModel):
    name = models.CharField(max_length=100)
    origin = models.ForeignKey("country.Country", on_delete=models.PROTECT, related_name="country_product_brands")

    class Meta:
        db_table = "product_product_brand"
