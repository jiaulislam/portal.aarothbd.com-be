# Generated by Django 5.1.3 on 2024-12-16 13:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("country", "0002_initial"),
        ("product", "0005_remove_product_companies"),
        ("uom", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="slug",
            field=models.SlugField(
                default="<function now at 0x105b5ca40>",
                max_length=255,
                unique=True,
                verbose_name="Slug",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="product",
            name="sku_code",
            field=models.CharField(
                blank=True, max_length=255, null=True, unique=True, verbose_name="SKU"
            ),
        ),
        migrations.AddIndex(
            model_name="product",
            index=models.Index(fields=["slug"], name="product_slug_idx"),
        ),
    ]
