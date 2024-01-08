# Generated by Django 4.0.4 on 2023-12-14 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend_app', '0055_init_config_ransomware_noti_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportSchedulerTimeFormat',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('format_name', models.CharField(max_length=150)),
                ('interval_days', models.IntegerField(default=1)),
                ('last_send_notification_date', models.DateTimeField(blank=True)),
                ('notification_time', models.CharField(max_length=150, null=True)),
            ],
            options={
                'db_table': 'report_scheduler_time_format',
            },
        ),
        migrations.CreateModel(
            name='ReportSchedulerClientDetails',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('product_types', models.CharField(blank=True, max_length=150, null=True)),
                ('log_type', models.CharField(blank=True, max_length=150, null=True)),
                ('email_ids', models.CharField(blank=True, max_length=150)),
                ('is_active', models.BooleanField(default=False)),
                ('location_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend_app.attach_location')),
                ('org_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend_app.organization_data')),
                ('plan_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend_app.updated_plan_details')),
                ('report_format_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend_app.reportschedulertimeformat')),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend_app.client_data')),
            ],
            options={
                'db_table': 'report_scheduler_client_details',
            },
        ),
    ]
