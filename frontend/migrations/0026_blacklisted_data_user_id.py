# Generated by Django 4.0.5 on 2023-06-10 10:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0025_blacklisted_data_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='blacklisted_data',
            name='user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]