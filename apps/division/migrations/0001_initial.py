# Generated by Django 5.1.3 on 2024-12-10 11:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('country', '0002_alter_country_options_alter_country_continent_code'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('bn_name', models.CharField(max_length=255)),
                ('lat', models.CharField(blank=True, max_length=20, null=True)),
                ('long', models.FloatField(blank=True, max_length=20, null=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='country_divisions', to='country.country')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)s_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'division',
                'verbose_name_plural': 'divisions',
                'db_table': 'division_division',
                'ordering': ('name',),
            },
        ),
    ]
