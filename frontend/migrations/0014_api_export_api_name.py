# Generated by Django 4.0.5 on 2022-12-09 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0013_organization_data_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='api_export',
            name='api_name',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]