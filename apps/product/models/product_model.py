from django.db import models

from core.models import BaseModel


class Product(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(verbose_name="Slug", max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    sku_code = models.CharField(verbose_name="SKU", max_length=255, null=True, blank=True, unique=True)
    uom = models.ForeignKey("uom.UoM", on_delete=models.PROTECT, related_name="uom_products", verbose_name="UOM")
    purchase_uom = models.ForeignKey(
        "uom.UoM",
        on_delete=models.PROTECT,
        related_name="uom_purchase_products",
        verbose_name="Purchase UOM",
        null=True,
        blank=True,
    )
    category = models.ForeignKey("product.ProductCategory", on_delete=models.PROTECT, related_name="category_products")
    has_detail = models.BooleanField(default=False)
    brand = models.ForeignKey(
        "product.ProductBrand", on_delete=models.PROTECT, related_name="product_product_brands", null=True, blank=True
    )
    origin = models.ForeignKey(
        "country.Country", on_delete=models.PROTECT, related_name="country_products", null=True, blank=True
    )

    attributes = models.JSONField(blank=True, help_text="Any other attributes", default=dict)
    html = models.TextField(null=True, blank=True, help_text="HTML")
    details: models.QuerySet["ProductDetail"]

    default_image_1 = models.ImageField(null=True, blank=True, upload_to="products/")
    default_image_2 = models.ImageField(null=True, blank=True, upload_to="products/")
    default_image_3 = models.ImageField(null=True, blank=True, upload_to="products/")

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "product_product"
        verbose_name = "Product"
        verbose_name_plural = "Products"
        indexes = [
            models.Index(fields=["slug"], name="product_slug_idx"),
        ]


class ProductDetail(BaseModel):
    product = models.ForeignKey("product.Product", on_delete=models.PROTECT, related_name="details")
    size_name = models.CharField(max_length=100)
    size_description = models.TextField(null=True, blank=True)
    attributes = models.JSONField(blank=True, help_text="Any other attributes", default=dict)

    def __str__(self) -> str:
        return f"{self.product.name} - Size({self.size_name})"
