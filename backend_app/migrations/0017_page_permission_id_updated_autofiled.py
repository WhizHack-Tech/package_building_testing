# Generated by Django 4.0.4 on 2022-12-27 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_app', '0016_added_table_page_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page_permissions',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
