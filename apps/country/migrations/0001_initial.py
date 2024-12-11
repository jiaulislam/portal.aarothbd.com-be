# Generated by Django 5.1.3 on 2024-12-10 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('full_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Full Name')),
                ('country_code', models.CharField(max_length=2, unique=True, verbose_name='Country Code')),
                ('country_code_alpha3', models.CharField(max_length=3, unique=True, verbose_name='Country Code (Alpha-3)')),
                ('country_code_iso3', models.CharField(max_length=3, unique=True, verbose_name='Country Code (ISO-3)')),
                ('continent_code', models.CharField(max_length=2, verbose_name='Continent Code')),
                ('continent_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Continent Name')),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
                'db_table': 'country_country',
                'ordering': ('name',),
            },
        ),
    ]
