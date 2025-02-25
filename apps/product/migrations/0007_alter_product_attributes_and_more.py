# Generated by Django 5.1.3 on 2024-12-21 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0006_product_slug_alter_product_sku_code_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="attributes",
            field=models.JSONField(
                blank=True, default=dict, help_text="Any other attributes"
            ),
        ),
        migrations.AlterField(
            model_name="productdetail",
            name="attributes",
            field=models.JSONField(
                blank=True, default=dict, help_text="Any other attributes"
            ),
        ),
    ]
