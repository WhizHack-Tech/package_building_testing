# Generated by Django 4.0.4 on 2022-09-14 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0004_alter_init_configs_platform_val_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='init_configs',
            name='accuracy_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='init_configs',
            name='accuracy_val',
            field=models.IntegerField(null=True),
        ),
    ]
