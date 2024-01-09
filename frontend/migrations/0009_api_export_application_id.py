# Generated by Django 4.0.5 on 2022-09-22 06:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0008_applications'),
    ]

    operations = [
        migrations.AddField(
            model_name='api_export',
            name='application_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='frontend.applications'),
        ),
    ]
