# Generated by Django 5.1.3 on 2025-02-18 17:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("offer", "0003_offer_comission_amount_offer_commission_mode_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="offer",
            old_name="commission_mode",
            new_name="comission_mode",
        ),
    ]
