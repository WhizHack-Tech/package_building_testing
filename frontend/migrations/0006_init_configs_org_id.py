# Generated by Django 4.0.4 on 2022-09-16 07:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0005_init_configs_accuracy_name_init_configs_accuracy_val'),
    ]

    operations = [
        migrations.AddField(
            model_name='init_configs',
            name='org_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='frontend.organization_data'),
        ),
    ]