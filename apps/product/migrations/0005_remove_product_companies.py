# Generated by Django 5.1.3 on 2024-12-16 03:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0004_product_purchase_uom_alter_product_origin_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="companies",
        ),
    ]
