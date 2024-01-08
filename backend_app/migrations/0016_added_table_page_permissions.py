# Generated by Django 4.0.4 on 2022-12-27 11:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend_app', '0015_applications_table_changed_steps_data_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page_Permissions',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('env_trace', models.BooleanField(default=False)),
                ('env_wazuh', models.BooleanField(default=False)),
                ('org_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend_app.organization_data')),
            ],
            options={
                'db_table': 'page_permissions',
            },
        ),
    ]
