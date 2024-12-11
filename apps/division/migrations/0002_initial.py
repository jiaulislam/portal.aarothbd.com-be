# Generated by Django 5.1.3 on 2024-12-11 12:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('division', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='division',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)s_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='division',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)s_updated', to=settings.AUTH_USER_MODEL),
        ),
    ]
