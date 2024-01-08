# Generated by Django 4.0.5 on 2023-06-08 09:48

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0023_alter_page_permissions_default_page'),
    ]

    operations = [
        migrations.CreateModel(
            name='blacklisted_data',
            fields=[
                ('blacklisted_id', models.CharField(default=uuid.uuid4, editable=False, max_length=255, primary_key=True, serialize=False)),
                ('blacklisted_class', models.CharField(blank=True, max_length=255, null=True)),
                ('blacklisted_ip', models.CharField(blank=True, max_length=255, null=True)),
                ('location_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='frontend.attach_location')),
                ('org_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='frontend.organization_data')),
            ],
            options={
                'db_table': 'blacklisted_details',
            },
        ),
    ]