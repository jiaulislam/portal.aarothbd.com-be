# Generated by Django 5.1.3 on 2025-02-17 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sale_order", "0004_alter_paikarsaleorder_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="paikarsaleorder",
            name="ecomm_identifier",
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
