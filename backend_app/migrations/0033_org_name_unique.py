# Generated by Django 4.0.5 on 2023-06-06 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_app', '0032_char_fileds_time_interval_val_init_config_models'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization_data',
            name='organization_name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
