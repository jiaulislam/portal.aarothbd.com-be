from django.db import models

from core.models import BaseModel
from core.storage_config import upload_product_image


class ProductImage(BaseModel):
    product = models.ForeignKey("product.Product", on_delete=models.PROTECT, related_name="images")
    sale_order = models.ForeignKey(
        "sale_order.PaikarSaleOrder",
        on_delete=models.CASCADE,
        related_name="images",
        null=True,
    )  # if there is sale_order then it must be company specific image
    image = models.ImageField(upload_to=upload_product_image)
    is_default = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.product.name} - Image({self.image.name})"

    class Meta:
        db_table = "product_product_image"
