# Generated by Django 4.0.4 on 2022-10-11 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_app', '0006_api_export_add_foreignkey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='init_configs',
            name='severity_val',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='init_configs',
            name='time_interval_name',
            field=models.CharField(default=0, max_length=255),
        ),
    ]
