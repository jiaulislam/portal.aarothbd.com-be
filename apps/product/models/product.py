from django.db import models

from core.models import BaseModel


class Product(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    sku_code = models.CharField(max_length=255, null=True, blank=True)
    uom = models.ForeignKey("uom.UoM", on_delete=models.PROTECT, related_name="uom_products")
    category = models.ForeignKey("product.ProductCategory", on_delete=models.PROTECT, related_name="category_products")
    has_detail = models.BooleanField(default=False)
    brand = models.ForeignKey("product.ProductBrand", on_delete=models.PROTECT, related_name="product_product_brands")
    origin = models.ForeignKey("country.Country", on_delete=models.PROTECT, related_name="country_products")

    attributes = models.JSONField(null=True, blank=True, help_text="Any other attributes")
    html = models.TextField(null=True, blank=True, help_text="HTML")

    default_image_1 = models.ImageField(null=True, blank=True, upload_to="products/")
    default_image_2 = models.ImageField(null=True, blank=True, upload_to="products/")
    default_image_3 = models.ImageField(null=True, blank=True, upload_to="products/")

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "product_product"
        verbose_name = "Product"
        verbose_name_plural = "Products"


class ProductDetail(BaseModel):
    product = models.ForeignKey("product.Product", on_delete=models.PROTECT)
    size_name = models.CharField(max_length=100)
    size_description = models.TextField(null=True, blank=True)
    attributes = models.JSONField(null=True, blank=True, help_text="Any other attributes")

    def __str__(self) -> str:
        return self.size_name
