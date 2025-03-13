from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from core.models import BaseModel
from core.storage_config import upload_product_category_image


class ProductCategory(BaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="child_product_categories", null=True, blank=True
    )
    category_image = models.ImageField(
        upload_to=upload_product_category_image,
        null=True,
        blank=True,
        help_text="Product Category Image",
    )

    child_product_categories: models.QuerySet["ProductCategory"]

    class Meta:
        db_table = "product_product_category"
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"

    def __str__(self) -> str:
        return self.name


@receiver(pre_save, sender=ProductCategory)
def generate_slug(sender, instance: ProductCategory, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)
        counter = 1
        original_slug = instance.slug
        while ProductCategory.objects.filter(slug=instance.slug).exists():
            instance.slug = f"{original_slug}-{counter}"
            counter += 1
