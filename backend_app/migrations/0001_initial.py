# Generated by Django 4.0.4 on 2022-08-30 10:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email')),
                ('name', models.CharField(max_length=200)),
                ('role', models.CharField(max_length=100, null=True)),
                ('ability', models.JSONField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Agent_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attach_agent_group', models.CharField(max_length=255)),
                ('organization_id', models.CharField(max_length=255)),
                ('platform_type', models.CharField(max_length=255)),
                ('creation_timestamp', models.DateTimeField(auto_now=True)),
                ('updation_timestamp', models.DateTimeField(auto_now=True)),
                ('attach_agent_key', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'agent_details',
            },
        ),
        migrations.CreateModel(
            name='Billings_data',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('billing_types', models.CharField(max_length=255)),
                ('billing_descriptions', models.CharField(max_length=255)),
                ('billing_creations_timestamp', models.DateTimeField(auto_now=True)),
                ('billing_image', models.ImageField(upload_to='')),
            ],
            options={
                'db_table': 'billings',
            },
        ),
        migrations.CreateModel(
            name='Country_data',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('Country_Code', models.CharField(max_length=255)),
                ('Country_Name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'country',
            },
        ),
        migrations.CreateModel(
            name='email_config_data',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('host', models.CharField(max_length=255)),
                ('port', models.CharField(max_length=255)),
                ('auth', models.CharField(max_length=255)),
                ('auth_type', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'email_config',
            },
        ),
        migrations.CreateModel(
            name='Plans_data',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('plan_name', models.CharField(max_length=255)),
                ('plan_descriptions', models.CharField(max_length=255)),
                ('plan_creations_timestamp', models.DateTimeField(auto_now=True)),
                ('plan_image', models.ImageField(upload_to='')),
                ('plan_duration', models.IntegerField()),
                ('plan_name_duration', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'plans',
            },
        ),
        migrations.CreateModel(
            name='Role_ability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(blank=True, max_length=255, null=True)),
                ('ability', models.JSONField(blank=True, null=True)),
            ],
            options={
                'db_table': 'role_ability',
            },
        ),
        migrations.CreateModel(
            name='Time_Zone_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Time_Zone', models.CharField(max_length=255)),
                ('GMT_Offset', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'time_zone',
            },
        ),
        migrations.CreateModel(
            name='Organization_data',
            fields=[
                ('organization_id', models.CharField(default=uuid.uuid4, editable=False, max_length=255, primary_key=True, serialize=False)),
                ('organization_name', models.CharField(max_length=255)),
                ('organization_primary_email_id', models.CharField(max_length=255)),
                ('organization_secondary_email_id', models.CharField(max_length=255)),
                ('organization_primary_contact_number', models.CharField(max_length=255)),
                ('organization_secondary_contact_number', models.CharField(max_length=255)),
                ('organization_address', models.CharField(max_length=255)),
                ('organization_city', models.CharField(max_length=255)),
                ('organization_state', models.CharField(max_length=255)),
                ('organization_country', models.CharField(max_length=255)),
                ('organization_pincode', models.CharField(max_length=255)),
                ('onboarding_timestamp', models.DateTimeField(auto_now_add=True)),
                ('status_code', models.IntegerField(default=0)),
                ('customer_types', models.CharField(blank=True, max_length=255)),
                ('environment_type', models.CharField(blank=True, max_length=255)),
                ('billing_id', models.ForeignKey(blank=True, db_column='billing_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend_app.billings_data')),
                ('country_id', models.ForeignKey(blank=True, db_column='country_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend_app.country_data')),
                ('plan_id', models.ForeignKey(blank=True, db_column='plan_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend_app.plans_data')),
                ('timezone_id', models.ForeignKey(blank=True, db_column='timezone_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend_app.time_zone_data')),
            ],
            options={
                'db_table': 'organization_original_details',
            },
        ),
        migrations.CreateModel(
            name='Client_data',
            fields=[
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email')),
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=255, primary_key=True, serialize=False)),
                ('user_type', models.CharField(max_length=255)),
                ('password', models.CharField(default='initpasswork@123#?>123', max_length=150)),
                ('client_password', models.CharField(blank=True, max_length=150)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255)),
                ('trading_name', models.CharField(max_length=255)),
                ('registration_no', models.CharField(max_length=255)),
                ('government_tax', models.CharField(max_length=255)),
                ('company_type_id', models.CharField(max_length=255)),
                ('profile_photo', models.ImageField(upload_to='static')),
                ('contact_number', models.CharField(max_length=255)),
                ('gender', models.CharField(max_length=255)),
                ('address_1', models.CharField(max_length=255)),
                ('address_2', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('zipcode', models.CharField(max_length=255)),
                ('allow_MFA', models.IntegerField(choices=[(0, 'Inactive'), (1, 'Active')], default=0)),
                ('otp_mail', models.CharField(blank=True, max_length=15, null=True)),
                ('MFA_token', models.CharField(blank=True, max_length=150, null=True)),
                ('first_config', models.IntegerField(choices=[(0, 'Inactive'), (1, 'Active')], default=0)),
                ('last_login', models.DateTimeField(auto_now_add=True, null=True)),
                ('parent_client_id', models.CharField(blank=True, max_length=150, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', models.ForeignKey(blank=True, db_column='country_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend_app.country_data')),
                ('organization_id', models.ForeignKey(blank=True, db_column='organization_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend_app.organization_data')),
                ('role_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend_app.role_ability')),
            ],
            options={
                'db_table': 'client_data',
            },
        ),
        migrations.CreateModel(
            name='ApiLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_name', models.CharField(blank=True, max_length=255)),
                ('type', models.CharField(max_length=255)),
                ('date_time', models.DateTimeField()),
                ('ip', models.CharField(max_length=20)),
                ('browser_type', models.CharField(max_length=255)),
                ('req_method', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=255)),
                ('client_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend_app.client_data')),
                ('master_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('org_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend_app.organization_data')),
            ],
            options={
                'db_table': 'api_logs',
            },
        ),
        migrations.CreateModel(
            name='Api_export',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_key', models.CharField(blank=True, max_length=150)),
                ('api_key_status', models.BooleanField(default=False)),
                ('appication_type', models.CharField(blank=True, max_length=150)),
                ('api_type', models.CharField(blank=True, max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend_app.client_data')),
            ],
            options={
                'db_table': 'api_export',
            },
        ),
    ]
