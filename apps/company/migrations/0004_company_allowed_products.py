# Generated by Django 5.1.3 on 2024-12-16 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("company", "0003_remove_company_company_favico_and_more"),
        ("product", "0005_remove_product_companies"),
    ]

    operations = [
        migrations.AddField(
            model_name="company",
            name="allowed_products",
            field=models.ManyToManyField(
                related_name="companies", to="product.product"
            ),
        ),
    ]
