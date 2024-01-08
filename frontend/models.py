#  ==================================================================================================
#  File Name: models.py
#  Description: File to define the data structure and database schema for web application.
#  ---------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  ====================================================================================================

import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class Role_ability(models.Model):
    role = models.CharField(blank=True, null=True, max_length=255)
    ability = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = "role_ability"


class Country_data(models.Model):
    country_code = models.CharField(max_length=255)
    country_name = models.CharField(max_length=255)

    class Meta:
        db_table = "country"


# overwright UserManager
class UserManager(BaseUserManager):
    def create_user(self, email, username, client_password, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            client_password=client_password,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password=None):
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )

        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class Organization_data(models.Model):
    organization_id = models.CharField(
        max_length=255, primary_key=True, default=uuid.uuid4, editable=False
    )
    organization_name = models.CharField(max_length=255)
    organization_primary_email_id = models.CharField(max_length=255)
    organization_secondary_email_id = models.CharField(max_length=255)
    organization_primary_contact_number = models.CharField(max_length=255)
    organization_secondary_contact_number = models.CharField(max_length=255)
    organization_address = models.CharField(max_length=255)
    organization_city = models.CharField(max_length=255)
    organization_state = models.CharField(max_length=255)
    organization_country = models.CharField(max_length=255)
    organization_pincode = models.CharField(max_length=255)
    onboarding_timestamp = models.DateTimeField(auto_now_add=True)
    status_code = models.IntegerField(default=0)
    customer_types = models.CharField(max_length=255, blank=True)
    environment_type = models.CharField(max_length=255, blank=True)
    trace_environment = models.BooleanField(default=False)
    wazuh_environment = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "organization_original_details"


# updated Plan details
class Updated_Plan_Details(models.Model):
    id = models.AutoField(primary_key=True)
    plan_name = models.CharField(max_length=150, blank=True)
    plan_descriptions = models.CharField(max_length=150, blank=True)
    plan_start_date = models.CharField(max_length=150, blank=True)
    plan_end_date = models.CharField(max_length=150, blank=True)
    plan_creations_timestamp = models.CharField(max_length=150, blank=True)
    plan_updations_timestamp = models.CharField(max_length=150, blank=True)
    plan_status = models.BooleanField(default=True)
    plan_key = models.CharField(max_length=150, blank=True)  # auto key generate

    class Meta:
        db_table = "updated_plan_details"


# Location table
class Attach_Location(models.Model):
    id = models.CharField(
        max_length=255, primary_key=True, default=uuid.uuid4, editable=False
    )
    email = models.EmailField(verbose_name="email", max_length=255)
    phone_number = models.CharField(max_length=255, blank=True)
    fax_number = models.CharField(max_length=255, blank=True)
    gst_id = models.CharField(max_length=255, blank=True)
    gst_image = models.ImageField()
    tan_id = models.CharField(max_length=255, blank=True)
    tan_image = models.ImageField()
    pan_id = models.CharField(max_length=255, blank=True)
    pan_image = models.ImageField()
    cin_id = models.CharField(max_length=255, blank=True)
    cin_image = models.ImageField()
    org_id = models.ForeignKey(
        Organization_data, on_delete=models.SET_NULL, null=True, blank=True
    )
    address = models.CharField(max_length=255, blank=True)
    branchcode = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    activated_plan_id = models.ForeignKey(
        Updated_Plan_Details,
        on_delete=models.SET_NULL,
        db_column="activated_plan_id",
        null=True,
        blank=True,
    )
    deactivated_plan_id = models.CharField(max_length=255)
    country_id = models.ForeignKey(
        "Country_data",
        on_delete=models.SET_NULL,
        db_column="country_id",
        null=True,
        blank=True,
    )
    pincode = models.IntegerField(null=True)
    customer_types = models.IntegerField(null=True)
    environment_type = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "organization_location"


class Client_data(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email",
        max_length=255,
        unique=True,
    )

    INACTIVE = 0
    ACTIVE = 1
    STATUS = (
        (INACTIVE, _("Inactive")),
        (ACTIVE, _("Active")),
    )

    id = models.CharField(
        max_length=255, default=uuid.uuid4, primary_key=True, editable=False
    )
    role_id = models.ForeignKey(
        Role_ability, on_delete=models.SET_NULL, null=True, blank=True
    )
    user_type = models.CharField(max_length=255)
    organization_id = models.CharField(max_length=255, blank=True, null=True)
    location_id = models.ForeignKey(
        Attach_Location,
        on_delete=models.SET_NULL,
        db_column="location_id",
        null=True,
        blank=True,
    )
    password = models.CharField(max_length=150, default="initpasswork@123#?>123")
    client_password = models.CharField(
        max_length=150, blank=True
    )  # contains the randomly generated password (sent to first time created user on mail)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    trading_name = models.CharField(max_length=255)
    registration_no = models.CharField(max_length=255)
    government_tax = models.CharField(max_length=255)
    company_type_id = models.CharField(max_length=255)
    profile_photo = models.ImageField(upload_to="static")
    contact_number = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    address_1 = models.CharField(max_length=255)
    address_2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    country = models.ForeignKey(
        Country_data,
        on_delete=models.SET_NULL,
        db_column="country_id",
        null=True,
        blank=True,
    )
    allow_MFA = models.IntegerField(default=INACTIVE, choices=STATUS)
    otp_mail = models.CharField(max_length=15, blank=True, null=True)
    MFA_token = models.CharField(max_length=150, blank=True, null=True)
    first_config = models.IntegerField(
        default=INACTIVE, choices=STATUS
    )  # by default =0, changes to 1 when user modify password
    last_login = models.DateTimeField(auto_now_add=True, null=True)
    parent_client_id = models.CharField(max_length=150, blank=True, null=True)
    lang_type = models.CharField(max_length=10, default="en")

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        db_table = "client_data"


class ApiLogs(models.Model):
    client_id = models.ForeignKey(
        Client_data, on_delete=models.SET_NULL, null=True, blank=True
    )
    org_id = models.ForeignKey(
        Organization_data, on_delete=models.SET_NULL, null=True, blank=True
    )
    table_name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    date_time = models.DateTimeField()
    ip = models.CharField(max_length=20)
    browser_type = models.CharField(max_length=255)
    req_method = models.CharField(max_length=30)
    description = models.CharField(max_length=255)

    class Meta:
        db_table = "api_logs"


class Applications(models.Model):
    application_name = models.CharField(max_length=255, blank=True)
    application_descriptions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    application_steps = models.JSONField(blank=True)
    application_image = models.ImageField()
    integration_status = models.BooleanField(default=False)

    class Meta:
        db_table = "applications"


class Api_export(models.Model):
    client_id = models.ForeignKey(
        Client_data, on_delete=models.SET_NULL, null=True, blank=True
    )
    api_key = models.CharField(max_length=150, blank=True)
    api_key_status = models.BooleanField(default=False)
    appication_type = models.CharField(max_length=150, blank=True)
    api_type = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    application_id = models.ForeignKey(
        Applications, on_delete=models.SET_NULL, null=True, blank=True
    )
    api_name = models.CharField(max_length=150, blank=True)

    class Meta:
        db_table = "api_export"


class Init_Configs(models.Model):
    config_type = models.CharField(max_length=150, blank=True)
    updated_plan_id = models.ForeignKey(
        Updated_Plan_Details,
        on_delete=models.SET_NULL,
        db_column="updated_plan_id",
        null=True,
        blank=True,
    )
    org_id = models.ForeignKey(
        Organization_data, on_delete=models.SET_NULL, null=True, blank=True
    )
    email_ids = models.CharField(max_length=150, blank=True)
    email_name = models.CharField(max_length=100, blank=True)
    platform_name = models.CharField(max_length=50, blank=True)
    platform_val = models.CharField(max_length=50, blank=True, null=True)
    severity_name = models.CharField(max_length=100, blank=True)  # remove
    severity_val = models.CharField(max_length=50, blank=True)  # remove
    accuracy_name = models.CharField(max_length=255, blank=True)
    accuracy_val = models.IntegerField(null=True)
    time_interval_name = models.CharField(
        max_length=255, default=0
    )  # future epoch time (eg. if time_interval_val is 5 min then we find out epoch time after 5 min and update it in this column)
    time_interval_val = models.CharField(
        max_length=255, null=True, blank=True
    )  # email notification time value
    default_config = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    trace_sensor = models.CharField(max_length=255, null=True, blank=True)
    location_id = models.ForeignKey(
        Attach_Location,
        on_delete=models.SET_NULL,
        db_column="location_id",
        null=True,
        blank=True,
    )
    sensor_alert_client = models.EmailField(
        max_length=255, null=True, blank=True
    )  # healthcheck sensor alert notifications would be sent on this email_id for client
    sensor_alert_admin = models.EmailField(
        max_length=255, null=True, blank=True
    )  # healthcheck sensor alert notifications would be sent on this email_id for admin
    ransomware_noti_epoch_val = models.CharField(
        max_length=255, default=0
    )  # future epoch time for ransomware email noti (eg. default ransomware_time_val is 3 min, we find out epoch time after 3 min and update it in this column)
    ransomware_noti_is_active = models.BooleanField(
        default=False
    )  # to turn ransomware email noti on/off (if True = on and if False then noti would be off)

    class Meta:
        db_table = "init_config"


# To create a models page_permissions table
class Page_Permissions(models.Model):
    id = models.AutoField(primary_key=True)
    updated_plan_id = models.ForeignKey(
        Updated_Plan_Details,
        on_delete=models.SET_NULL,
        db_column="updated_plan_id",
        null=True,
        blank=True,
    )
    org_id = models.ForeignKey(
        Organization_data, on_delete=models.SET_NULL, null=True, blank=True
    )
    location_id = models.ForeignKey(
        Attach_Location,
        on_delete=models.SET_NULL,
        db_column="location_id",
        null=True,
        blank=True,
    )
    env_trace = models.BooleanField(default=False)
    env_wazuh = models.BooleanField(default=False)
    env_hids = models.BooleanField(default=False)
    env_nids = models.BooleanField(default=False)
    env_soar = models.BooleanField(default=False)
    env_tps = models.BooleanField(default=False)  # TP Source Feeds
    env_ess = models.BooleanField(default=False)  # ESS Feeds
    env_sbs = models.BooleanField(default=False)  # SandBox Feeds
    env_tptf = models.BooleanField(default=False)  # TP Threat Feeds
    env_mm = models.BooleanField(default=False)  # Media Management Feeds
    env_hc = models.BooleanField(default=False)  # Health Check Feeds
    xdr_live_map = models.BooleanField(default=False)
    default_page = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = "page_permissions"


# Blacklisted Table containing info about blacklisted threat classes,blacklisted IP
class blacklisted_data(models.Model):
    blacklisted_id = models.CharField(
        max_length=255, primary_key=True, default=uuid.uuid4, editable=False
    )
    blacklisted_class = models.CharField(max_length=255, null=True, blank=True)
    blacklisted_ip = models.CharField(max_length=255, null=True, blank=True)
    org_id = models.ForeignKey(
        Organization_data, on_delete=models.SET_NULL, null=True, blank=True
    )
    location_id = models.ForeignKey(
        Attach_Location, on_delete=models.SET_NULL, null=True, blank=True
    )
    user_id = models.ForeignKey(
        Client_data, on_delete=models.SET_NULL, null=True, blank=True
    )
    updated_plan_id = models.ForeignKey(
        Updated_Plan_Details,
        on_delete=models.SET_NULL,
        db_column="updated_plan_id",
        null=True,
        blank=True,
    )
    created_at = models.CharField(max_length=100, blank=True, null=True)
    updated_at = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "blacklisted_details"


# ---------------------model for "Agent_details" table -------------
class Agent_data(models.Model):
    attach_agent_group = models.CharField(max_length=255)  # remove
    attach_agent_network = models.CharField(
        max_length=255, null=True, blank=True
    )  # remove
    organization_id = models.ForeignKey(
        Organization_data,
        on_delete=models.SET_NULL,
        db_column="organization_id",
        null=True,
        blank=True,
    )
    updated_plan_id = models.ForeignKey(
        Updated_Plan_Details,
        on_delete=models.SET_NULL,
        db_column="updated_plan_id",
        null=True,
        blank=True,
    )
    platform_type = models.CharField(max_length=255)  # remove
    creation_timestamp = models.DateTimeField(auto_now=True)
    updation_timestamp = models.DateTimeField(auto_now=True)
    attach_agent_key = models.CharField(max_length=255)
    trace_attach_agent = models.CharField(
        max_length=255, null=True, blank=True
    )  # remove
    wazuh_attach_agent = models.CharField(
        max_length=255, null=True, blank=True
    )  # remove
    db_username = models.CharField(max_length=255, null=True, blank=True)
    db_password = models.CharField(max_length=255, null=True, blank=True)
    org_location = models.ForeignKey(
        Attach_Location, on_delete=models.SET_NULL, null=True, blank=True
    )
    db_host = models.CharField(max_length=255, null=True, blank=True)
    db_port = models.CharField(max_length=255, null=True, blank=True)
    nids_event_agent = models.CharField(max_length=255, null=True, blank=True)
    nids_alert_agent = models.CharField(max_length=255, null=True, blank=True)
    nids_incident_agent = models.CharField(max_length=255, null=True, blank=True)
    nids_assets_agent = models.CharField(max_length=255, null=True, blank=True)
    nids_nmap_agent = models.CharField(max_length=255, null=True, blank=True)
    nids_global_agent = models.CharField(max_length=255, null=True, blank=True)
    trace_event_agent = models.CharField(max_length=255, null=True, blank=True)
    trace_alert_agent = models.CharField(max_length=255, null=True, blank=True)
    trace_incident_agent = models.CharField(max_length=255, null=True, blank=True)
    trace_global_agent = models.CharField(max_length=255, null=True, blank=True)
    trace_dpi_agent = models.CharField(max_length=255, null=True, blank=True)
    hids_event_agent = models.CharField(max_length=255, null=True, blank=True)
    hids_alert_agent = models.CharField(max_length=255, null=True, blank=True)
    hids_incident_agent = models.CharField(max_length=255, null=True, blank=True)
    hids_assets_agent = models.CharField(max_length=255, null=True, blank=True)
    soar_agent = models.CharField(max_length=255, null=True, blank=True)
    tps_agent = models.CharField(
        max_length=255, null=True, blank=True
    )  # TP Source Feeds
    ess_agent = models.CharField(max_length=255, null=True, blank=True)  # ESS Feeds
    sbs_agent = models.CharField(max_length=255, null=True, blank=True)  # SandBox Feeds
    tptf_agent = models.CharField(
        max_length=255, null=True, blank=True
    )  # TP Threat Feeds
    mm_agent = models.CharField(
        max_length=255, null=True, blank=True
    )  # Media Management Feeds
    hc_agent = models.CharField(
        max_length=255, null=True, blank=True
    )  # Health Check Feeds
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = "agent_details"


class Updated_Api_export(models.Model):
    client_id = models.ForeignKey(
        Client_data, on_delete=models.SET_NULL, null=True, blank=True
    )
    api_key = models.CharField(max_length=150, blank=True)
    api_key_status = models.BooleanField(default=False)
    product_logs_name = models.CharField(max_length=150, blank=True)
    api_type = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    product_name = models.CharField(max_length=150, blank=True)

    class Meta:
        db_table = "updated_api_export"


# Soar License_Management table added
class Soar_License_Management(models.Model):
    id = models.AutoField(primary_key=True)
    updated_plan_id = models.ForeignKey(
        Updated_Plan_Details,
        on_delete=models.SET_NULL,
        db_column="updated_plan_id",
        null=True,
        blank=True,
    )  # updated new coloumn
    control_server_domain = models.CharField(max_length=250, blank=True)
    aggregator_domain = models.CharField(max_length=250, blank=True)
    aggregator_port = models.CharField(max_length=250, blank=True)
    sensor_type = models.CharField(max_length=250, blank=True)
    registry_address = models.CharField(max_length=250, blank=True)
    sensor_key = models.CharField(
        max_length=250, blank=True
    )  # auto generated key (sensor_access_id,sensor_password)
    access_id = models.CharField(max_length=250, blank=True)
    access_key = models.CharField(max_length=250, blank=True)
    edition = models.CharField(max_length=250, blank=True)
    company_index_name = models.CharField(max_length=250, blank=True)
    aws_default_region = models.CharField(max_length=250, blank=True)
    location = models.CharField(max_length=250, blank=True)
    client_city = models.CharField(max_length=250, blank=True)
    client_latitude = models.CharField(max_length=250, blank=True)
    client_longitude = models.CharField(max_length=250, blank=True)
    client_country_code = models.CharField(max_length=250, blank=True)
    client_country_name = models.CharField(max_length=250, blank=True)
    xdr_soar_status = models.CharField(max_length=250, blank=True)
    soar_sensor_host_url = models.CharField(max_length=250, blank=True)
    backend_port = models.CharField(max_length=250, blank=True)
    frontend_port = models.CharField(max_length=250, blank=True)
    frontend_port_https = models.CharField(max_length=250, blank=True)
    shuffle_default_username = models.CharField(max_length=250, blank=True)
    shuffle_default_password = models.CharField(max_length=250, blank=True)
    shuffle_default_apikey = models.CharField(max_length=250, blank=True)
    license_start_date = models.CharField(max_length=250, blank=True)
    license_end_date = models.CharField(max_length=250, blank=True)
    operating_env = models.CharField(max_length=250, blank=True)
    created_at = models.CharField(max_length=250, blank=True)
    updated_at = models.CharField(max_length=250, blank=True)
    sensor_create_count = models.CharField(max_length=150, blank=True)
    sensor_active_count = models.CharField(max_length=150, blank=True)

    class Meta:
        db_table = "soar_license_management"


class ReportSchedulerTimeFormat(models.Model):
    id = models.AutoField(primary_key=True)
    format_name = models.CharField(max_length=150, blank=False)
    interval_days = models.IntegerField(blank=False, default=1)
    last_send_notification_date = models.DateTimeField(blank=True)
    notification_time = models.CharField(max_length=150, null=True, blank=False)

    class Meta:
        db_table = "report_scheduler_time_format"


class ReportSchedulerClientDetails(models.Model):
    id = models.AutoField(primary_key=True)
    org_id = models.ForeignKey(Organization_data, on_delete=models.SET_NULL, null=True, blank=True)
    location_id = models.ForeignKey(Attach_Location, on_delete=models.SET_NULL, null=True, blank=True)
    user_id = models.ForeignKey(Client_data, on_delete=models.SET_NULL, null=True, blank=True)
    report_format_id = models.ForeignKey(ReportSchedulerTimeFormat, on_delete=models.SET_NULL, null=True, blank=True)
    product_types = models.CharField(max_length=150, null=True, blank=True)
    log_type = models.CharField(max_length=150, null=True, blank=True)
    plan_id = models.ForeignKey(Updated_Plan_Details, on_delete=models.SET_NULL, null=True, blank=True)
    email_ids = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = "report_scheduler_client_details"
