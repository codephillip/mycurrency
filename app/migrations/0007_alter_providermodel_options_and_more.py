# Generated by Django 4.2.11 on 2024-05-04 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_providermodel'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='providermodel',
            options={'ordering': ['priority', 'created_at']},
        ),
        migrations.AlterField(
            model_name='providermodel',
            name='module_dir',
            field=models.CharField(max_length=300),
        ),
    ]
