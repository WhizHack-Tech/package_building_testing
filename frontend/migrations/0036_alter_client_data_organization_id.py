# Generated by Django 4.0.5 on 2023-09-06 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0035_alter_client_data_organization_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client_data',
            name='organization_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]