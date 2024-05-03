# Generated by Django 4.2.11 on 2024-05-03 21:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_remove_currencyexchangerate_is_protected_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProviderModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('priority', models.IntegerField(default=100)),
                ('module_dir', models.CharField(max_length=300, unique=True)),
                ('module_name', models.CharField(max_length=300, unique=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
