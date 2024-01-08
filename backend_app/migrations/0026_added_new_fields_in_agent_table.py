# Generated by Django 4.0.5 on 2023-05-26 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_app', '0025_changed_host_url_and_db_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent_data',
            name='db_host',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='agent_data',
            name='db_port',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='agent_data',
            name='hids_alert_agent',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='agent_data',
            name='hids_assets_agent',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='agent_data',
            name='hids_event_agent',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='agent_data',
            name='hids_incident_agent',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='agent_data',
            name='nids_alert_agent',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='agent_data',
            name='nids_assets_agent',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='agent_data',
            name='nids_event_agent',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='agent_data',
            name='nids_global_agent',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='agent_data',
            name='nids_incident_agent',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='agent_data',
            name='nids_nmap_agent',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='agent_data',
            name='trace_alert_agent',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='agent_data',
            name='trace_event_agent',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='agent_data',
            name='trace_global_agent',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='agent_data',
            name='trace_incident_agent',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='init_configs',
            name='trace_sensor',
            field=models.CharField(blank=True, max_length=255, null=True),
        )
    ]
