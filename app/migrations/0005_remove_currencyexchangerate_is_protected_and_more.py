# Generated by Django 4.2.11 on 2024-05-01 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_currencyexchangerate_is_protected'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='currencyexchangerate',
            name='is_protected',
        ),
        migrations.AddField(
            model_name='currency',
            name='is_protected',
            field=models.BooleanField(default=True),
        ),
    ]