# Generated by Django 5.1.3 on 2024-12-11 12:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('country', '0001_initial'),
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
            ],
            options={
                'verbose_name': 'division',
                'verbose_name_plural': 'divisions',
                'db_table': 'division_division',
                'ordering': ('name',),
            },
        ),
    ]
