from django.db import models

from core.models import BaseModel


class ProductCategory(BaseModel):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="child_product_categories", null=True, blank=True
    )
    category_image = models.ImageField(upload_to="product_category", null=True, blank=True)

    child_product_categories: models.QuerySet["ProductCategory"]

    class Meta:
        db_table = "product_product_category"
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"

    def __str__(self) -> str:
        return self.name
