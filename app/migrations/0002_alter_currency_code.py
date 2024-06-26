# Generated by Django 4.2.11 on 2024-05-01 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='code',
            field=models.CharField(choices=[('USD', 'US Dollar'), ('EUR', 'Euro'), ('CHF', 'Swiss Franc'), ('GBP', 'Great British Pound')], max_length=3, unique=True),
        ),
    ]
