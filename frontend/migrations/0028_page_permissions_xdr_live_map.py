# Generated by Django 4.0.5 on 2023-06-14 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0027_init_configs_location_id_init_configs_trace_sensor_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='page_permissions',
            name='xdr_live_map',
            field=models.BooleanField(default=False),
        ),
    ]