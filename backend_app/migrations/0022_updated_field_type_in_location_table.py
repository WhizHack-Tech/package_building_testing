# Generated by Django 4.0.5 on 2023-01-13 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_app', '0021_added_location_foreignkey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attach_location',
            name='fax_number',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='attach_location',
            name='phone_number',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
