# Generated by Django 5.1.3 on 2025-02-18 17:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("offer", "0002_offer_agreed_at_offer_agreed_by_offer_company_agreed"),
        ("uom", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="offer",
            name="comission_amount",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="offer",
            name="commission_mode",
            field=models.CharField(
                blank=True,
                choices=[("fixed", "Fixed"), ("percentage", "Percentage")],
                max_length=255,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="offer",
            name="uom",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="offers",
                to="uom.uom",
            ),
        ),
    ]
