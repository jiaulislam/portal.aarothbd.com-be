# Generated by Django 5.1.3 on 2024-12-09 05:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_user_user_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'User Profile', 'verbose_name_plural': 'User Profiles'},
        ),
    ]
