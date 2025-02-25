# Generated by Django 5.1.3 on 2024-12-11 12:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('object_id', models.PositiveIntegerField()),
                ('line_1', models.TextField(blank=True, null=True)),
                ('line_2', models.TextField(blank=True, null=True)),
                ('address_type', models.CharField(choices=[('default', 'Default Address'), ('delivery', 'Delivery Address'), ('contact', 'Contact Address'), ('general', 'General Address')], default='general', max_length=80)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Addresses',
                'db_table': 'address_address',
                'ordering': ['-id'],
            },
        ),
    ]
