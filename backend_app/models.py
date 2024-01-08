#  ==================================================================================================
#  File Name: models.py
#  Description: File to define the data structure and database schema for django project.
#  ---------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Master Dashboard
#  Author URL: https://whizhack.in

#  ====================================================================================================

# Create your models here.
from distutils.command.config import config
import email
from email.policy import default
from platform import platform
from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date, timedelta
import uuid, random, string
from .auto_pass_generator import rand_pass
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

#overwright UserManager
class UserManager(BaseUserManager):
    def create_user(self, email, name, role, ability, password=None):
        """
        Creates and saves a User with the given email, name, tc, role, ability date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            role=role,
            ability=ability
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name,  password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            password=password,
        )
        
        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)
        return user

#creat custome master user
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )

    name = models.CharField(max_length=200)
    role = models.CharField(max_length=100,null=True)
    ability = models.JSONField(blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

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

#------------------model for "organization_original_details" table---------
class Organization_data(models.Model):
    organization_id = models.CharField(max_length=255, primary_key=True, default=uuid.uuid4, editable=False)
    organization_name=models.CharField(max_length=255, unique= True)
    organization_primary_email_id=models.CharField(max_length=255)
    organization_secondary_email_id=models.CharField(max_length=255)
    organization_primary_contact_number = models.CharField(max_length=255)
    organization_secondary_contact_number = models.CharField(max_length=255)
    organization_address=models.CharField(max_length=255)
    organization_city=models.CharField(max_length=255)
    organization_state=models.CharField(max_length=255)
    organization_country=models.CharField(max_length=255)
    organization_pincode=models.CharField(max_length=255)
    onboarding_timestamp=models.DateTimeField(auto_now_add=True)
    status_code=models.IntegerField(default=0)#default=0 sets status automatically=0
    plan_id = models.ForeignKey('Plans_data',on_delete=models.SET_NULL, db_column='plan_id', null=True, blank=True)
    billing_id = models.ForeignKey('Billings_data',on_delete=models.SET_NULL, db_column='billing_id', null=True, blank=True)
    country_id = models.ForeignKey('Country_data',on_delete=models.SET_NULL, db_column='country_id', null=True, blank=True)
    timezone_id = models.ForeignKey('Time_Zone_data',on_delete=models.SET_NULL, db_column='timezone_id', null=True, blank=True)
    customer_types = models.CharField(max_length=255,blank=True)
    environment_type = models.CharField(max_length=255,blank=True)
    trace_environment = models.BooleanField(default=False)
    wazuh_environment = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
   
    class Meta:
        db_table ='organization_original_details'
    
#---------------------model for "plans" table-------------
class Plans_data(models.Model):        
    id = models.AutoField(primary_key=True)
    plan_name=models.CharField(max_length=255)
    plan_descriptions=models.CharField(max_length=255)
    plan_creations_timestamp = models.DateTimeField(auto_now=True)
    plan_image =  models.ImageField()
    plan_duration = models.IntegerField()
    plan_name_duration = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        concat = self.plan_name +"_"+ str(self.plan_duration)+"_months"
        self.plan_name_duration = concat 
        super().save(*args, **kwargs)
    class Meta:
        db_table ='plans'


#---------------------model for "billings" table-------------
class Billings_data(models.Model):    
    id = models.AutoField(primary_key=True)
    billing_types=models.CharField(max_length=255)
    billing_descriptions=models.CharField(max_length=255)
    billing_creations_timestamp = models.DateTimeField(auto_now=True)
    billing_image =  models.ImageField()
   
    class Meta:
        db_table ='billings'
        
#-----------------model for "Country" table----------------------------------------------       
class Country_data(models.Model):
    id = models.BigIntegerField(primary_key = True)
    country_code = models.CharField(max_length=255)
    country_name = models.CharField(max_length=255)
    
    class Meta:
        db_table ='country'


#-----------------model for "Time_Zone" table----------------------------------------------
class Time_Zone_data(models.Model):
    Time_Zone = models.CharField(max_length=255)
    GMT_Offset = models.CharField(max_length=255)
    
    class Meta:
        db_table ='time_zone'



class Role_ability(models.Model):    
    role = models.CharField(blank=True, null=True,max_length=255)
    ability = models.JSONField(blank=True, null=True)
    class Meta:
        db_table ='role_ability'


# updated plan details models (08-09-23)
class Updated_Plan_Details(models.Model):
    id  = models.AutoField(primary_key=True)
    plan_name = models.CharField(max_length=150,blank=True)
    org_id = models.ForeignKey(Organization_data, on_delete=models.SET_NULL, null=True, blank=True)
    plan_descriptions = models.CharField(max_length=150,blank=True)
    plan_start_date = models.CharField(max_length=150,blank=True)
    plan_end_date = models.CharField(max_length=150,blank=True)
    plan_creations_timestamp = models.CharField(max_length=150,blank=True)
    plan_updations_timestamp = models.CharField(max_length=150,blank=True)
    plan_status = models.BooleanField(default=True)
    plan_key = models.CharField(max_length=150,blank=True) # auto key generate
    env_trace = models.BooleanField(default=False)
    env_wazuh = models.BooleanField(default=False)
    env_hids = models.BooleanField(default=False)  
    env_nids = models.BooleanField(default=False)
    env_soar = models.BooleanField(default=False)
    env_tps = models.BooleanField(default=False) #TP Source Feeds
    env_ess = models.BooleanField(default=False) #ESS Feeds
    env_sbs = models.BooleanField(default=False) #SandBox Feeds
    env_tptf = models.BooleanField(default=False) #TP Threat Feeds
    env_mm = models.BooleanField(default=False) #Media Management Feeds
    env_hc = models.BooleanField(default=False) #Health Check Feeds
    xdr_live_map = models.BooleanField(default=False)
    default_page = models.CharField(max_length=50,blank=True,null=True)

    class Meta:
        db_table ='updated_plan_details'          


#To create a models location Attach table
class Attach_Location(models.Model): 
    id = models.CharField(max_length=255, primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(verbose_name='email',max_length=255)
    phone_number = models.CharField(max_length=255,blank=True)
    fax_number = models.CharField(max_length=255,blank=True)
    gst_id = models.CharField(max_length=255,blank=True)
    gst_image =  models.ImageField()
    tan_id = models.CharField(max_length=255,blank=True)
    tan_image =  models.ImageField()
    pan_id = models.CharField(max_length=255,blank=True)
    pan_image =  models.ImageField()
    cin_id = models.CharField(max_length=255,blank=True)
    cin_image =  models.ImageField()
    org_id = models.ForeignKey(Organization_data, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=255,blank=True)
    branchcode = models.CharField(max_length=255,blank=True) 
    city=models.CharField(max_length=255,blank=True) 
    state=models.CharField(max_length=255,blank=True) 
    activated_plan_id = models.ForeignKey(Updated_Plan_Details, on_delete=models.SET_NULL, db_column='activated_plan_id', null=True, blank=True) # updated
    deactivated_plan_id = models.CharField(max_length=255) # updated
    billing_id = models.ForeignKey('Billings_data',on_delete=models.SET_NULL, db_column='billing_id', null=True, blank=True)
    country_id = models.ForeignKey('Country_data',on_delete=models.SET_NULL, db_column='country_id', null=True, blank=True)
    timezone_id = models.ForeignKey('Time_Zone_data',on_delete=models.SET_NULL, db_column='timezone_id', null=True, blank=True)
    pincode=models.IntegerField(null=True)
    customer_types=models.IntegerField(null=True)
    environment_type=models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table ='organization_location'  



#---------------------model for "Client_data" table ( Priya Duggal )-------------
class Client_data(models.Model):
    
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    
    INACTIVE = 0
    ACTIVE = 1
    STATUS = (
        (INACTIVE, _('Inactive')),
        (ACTIVE, _('Active')),
    )
     
    id = models.CharField(max_length=255, default=uuid.uuid4, primary_key=True, editable=False)
    role_id = models.ForeignKey(Role_ability, on_delete=models.SET_NULL,null=True, blank=True)
    organization_id = models.ForeignKey(Organization_data, on_delete=models.SET_NULL, db_column='organization_id', null=True, blank=True)
    location_id = models.ForeignKey(Attach_Location, on_delete=models.SET_NULL, db_column='location_id', null = True, blank = True)
    user_type = models.CharField(max_length=255)
    password = models.CharField(max_length=150,default="initpasswork@123#?>123")
    client_password = models.CharField(max_length=150,blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    trading_name = models.CharField(max_length=255)
    registration_no = models.CharField(max_length=255)
    government_tax = models.CharField(max_length=255)
    company_type_id = models.CharField(max_length=255)
    profile_photo = models.ImageField(upload_to = 'static')
    contact_number = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    address_1 = models.CharField(max_length=255)
    address_2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    country = models.ForeignKey(Country_data, on_delete=models.SET_NULL, db_column='country_id', null=True, blank=True)    
    allow_MFA = models.IntegerField(default=INACTIVE, choices=STATUS)
    otp_mail = models.CharField(max_length=15,blank=True)
    first_config = models.IntegerField(default=INACTIVE, choices=STATUS)
    last_login = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    lang_type = models.CharField(max_length=10, default='en')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
        
    class Meta:
        db_table ='client_data'




#---------------------model for "email_config" table ( Priya Duggal )-------------
class email_config_data(models.Model):        
    id = models.AutoField(primary_key=True)
    host = models.CharField(max_length=255)
    port = models.CharField(max_length=255)
    auth = models.CharField(max_length=255)
    auth_type = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)#sets field value by default=0

    class Meta:
        db_table ='email_config'

class ApiLogs(models.Model):
    master_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    client_id = models.ForeignKey(Client_data, on_delete=models.SET_NULL, null=True, blank=True)
    table_name = models.CharField(max_length = 255,blank=True)   
    type = models.CharField(max_length = 255)
    date_time = models.DateTimeField()
    ip = models.CharField(max_length = 20)
    browser_type = models.CharField(max_length = 255)
    req_method = models.CharField(max_length = 30)
    description = models.CharField(max_length = 255)
    class Meta:
        db_table ='api_logs'

class Applications(models.Model):        
    application_name=models.CharField(max_length=255,blank=True)
    application_descriptions=models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    application_steps = models.JSONField(blank=True)
    application_image =  models.ImageField(blank = True)
    integration_status = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table ='applications'

class Api_export(models.Model):
    client_id = models.ForeignKey(Client_data, on_delete=models.SET_NULL,null=True, blank=True)
    api_key = models.CharField(max_length=150,blank=True)
    api_key_status = models.BooleanField(default=False)
    appication_type = models.CharField(max_length=150,blank=True)
    api_type = models.CharField(max_length=150,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    application_id = models.ForeignKey(Applications, on_delete=models.SET_NULL,null=True, blank=True)
    api_name = models.CharField(max_length=150,blank=True)

    class Meta:
        db_table ='api_export'

                 

#To create a models init_config table
class Init_Configs(models.Model):        
    config_type=models.CharField(max_length=150,blank=True)
    updated_plan_id = models.ForeignKey(Updated_Plan_Details, on_delete=models.SET_NULL, db_column='updated_plan_id', null=True, blank=True) # updated new coloumn
    org_id = models.ForeignKey(Organization_data, on_delete=models.SET_NULL, null=True, blank=True)
    email_ids=models.CharField(max_length=150,blank=True)
    email_name=models.CharField(max_length=100,blank=True)
    platform_name = models.CharField(max_length=50,blank=True)
    platform_val = models.CharField(max_length=50,blank=True,null=True,)
    severity_name = models.CharField(max_length=100,blank=True)#remove
    severity_val = models.CharField(max_length = 50, blank=True)#remove
    accuracy_name = models.CharField(max_length=255,blank=True)
    time_interval_val = models.CharField(max_length=255, null=True, blank=True)
    accuracy_val = models.IntegerField(null=True)
    time_interval_name = models.CharField(max_length=255,default=0)
    default_config = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    trace_sensor = models.CharField(max_length=255,null=True,blank=True)
    location_id = models.ForeignKey(Attach_Location, on_delete=models.SET_NULL, db_column='location_id', null = True, blank = True)
    sensor_alert_client = models.EmailField(max_length=255, null=True, blank=True) #healthcheck sensor alert notifications would be sent on this email_id for client
    sensor_alert_admin = models.EmailField(max_length=255, null=True, blank=True) #healthcheck sensor alert notifications would be sent on this email_id for admin
    ransomware_noti_epoch_val = models.CharField(max_length=255,default=0)#future epoch time for ransomware email noti (eg. default ransomware_time_val is 3 min, we find out epoch time after 3 min and update it in this column)
    ransomware_noti_is_active = models.BooleanField(default=False) # to turn ransomware email noti on/off (if True = on and if False then noti would be off)

    class Meta:
        db_table ='init_config'

#To create a models page_permissions table
class Page_Permissions(models.Model): 
    id = models.AutoField(primary_key=True)
    updated_plan_id = models.ForeignKey(Updated_Plan_Details, on_delete=models.SET_NULL, db_column='updated_plan_id', null=True, blank=True) # updated new coloumn
    org_id = models.ForeignKey(Organization_data, on_delete=models.SET_NULL, null=True, blank=True)
    location_id = models.ForeignKey(Attach_Location, on_delete=models.SET_NULL, db_column='location_id', null = True, blank = True)
    env_trace = models.BooleanField(default=False)
    env_wazuh = models.BooleanField(default=False) 
    env_hids = models.BooleanField(default=False)  
    env_nids = models.BooleanField(default=False)
    env_soar = models.BooleanField(default=False)
    env_tps = models.BooleanField(default=False) #TP Source Feeds
    env_ess = models.BooleanField(default=False) #ESS Feeds
    env_sbs = models.BooleanField(default=False) #SandBox Feeds
    env_tptf = models.BooleanField(default=False) #TP Threat Feeds
    env_mm = models.BooleanField(default=False) #Media Management Feeds
    env_hc = models.BooleanField(default=False) #Health Check Feeds
    xdr_live_map = models.BooleanField(default=False) 
    default_page = models.CharField(max_length=50,blank=True,null=True)  

    class Meta:
        db_table ='page_permissions'    


#---------------------model for "Agent_details" table ( Priya Duggal )-------------
class Agent_data(models.Model):
    attach_agent_group = models.CharField(max_length=255)#remove
    attach_agent_network = models.CharField(max_length=255,null=True,blank=True)#remove
    organization_id = models.ForeignKey(Organization_data, on_delete=models.SET_NULL, db_column='organization_id', null=True, blank=True)
    updated_plan_id = models.ForeignKey(Updated_Plan_Details, on_delete=models.SET_NULL, db_column='updated_plan_id', null=True, blank=True) # updated new coloumn
    platform_type = models.CharField(max_length=255)#remove
    creation_timestamp = models.DateTimeField(auto_now=True)
    updation_timestamp = models.DateTimeField(auto_now=True)
    attach_agent_key = models.CharField(max_length=255)
    trace_attach_agent = models.CharField(max_length=255,null=True,blank=True)#remove
    wazuh_attach_agent = models.CharField(max_length=255,null=True,blank=True)#remove
    db_username = models.CharField(max_length=255,null=True,blank=True)
    db_password = models.CharField(max_length=255,null=True,blank=True)
    org_location = models.ForeignKey(Attach_Location, on_delete=models.SET_NULL, null=True, blank=True)
    db_host = models.CharField(max_length=255,null=True,blank=True)
    db_port = models.CharField(max_length=255,null=True,blank=True)
    nids_event_agent = models.CharField(max_length=255,null=True,blank=True)
    nids_alert_agent = models.CharField(max_length=255,null=True,blank=True)
    nids_incident_agent = models.CharField(max_length=255,null=True,blank=True)
    nids_assets_agent = models.CharField(max_length=255,null=True,blank=True)
    nids_nmap_agent = models.CharField(max_length=255,null=True,blank=True)
    nids_global_agent = models.CharField(max_length=255,null=True,blank=True)
    trace_event_agent = models.CharField(max_length=255,null=True,blank=True)
    trace_alert_agent = models.CharField(max_length=255,null=True,blank=True)
    trace_incident_agent = models.CharField(max_length=255,null=True,blank=True)
    trace_global_agent = models.CharField(max_length=255,null=True,blank=True)
    trace_dpi_agent = models.CharField(max_length=255,null=True,blank=True)
    hids_event_agent = models.CharField(max_length=255,null=True,blank=True)
    hids_alert_agent = models.CharField(max_length=255,null=True,blank=True)
    hids_incident_agent = models.CharField(max_length=255,null=True,blank=True)
    hids_assets_agent = models.CharField(max_length=255,null=True,blank=True)
    soar_agent = models.CharField(max_length=255,null=True,blank=True)
    tps_agent = models.CharField(max_length=255,null=True,blank=True) #TP Source Feeds
    ess_agent = models.CharField(max_length=255,null=True,blank=True) #ESS Feeds
    sbs_agent = models.CharField(max_length=255,null=True,blank=True) #SandBox Feeds
    tptf_agent = models.CharField(max_length=255,null=True,blank=True) #TP Threat Feeds
    mm_agent = models.CharField(max_length=255,null=True,blank=True) #Media Management Feeds
    hc_agent = models.CharField(max_length=255,null=True,blank=True) #Health Check Feeds
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table ='agent_details'

# Blacklisted Table containing info about blacklisted threat classes,blacklisted IP
class blacklisted_data(models.Model):
    blacklisted_id = models.CharField(max_length=255, primary_key=True, default=uuid.uuid4, editable=False)
    blacklisted_class = models.CharField(max_length=255,null=True,blank=True)
    blacklisted_ip = models.CharField(max_length=255,null=True,blank=True)
    org_id = models.ForeignKey(Organization_data, on_delete=models.SET_NULL, null=True, blank=True)
    location_id = models.ForeignKey(Attach_Location, on_delete=models.SET_NULL, null=True, blank=True)
    user_id = models.ForeignKey(Client_data, on_delete=models.SET_NULL, null=True, blank=True)
    updated_plan_id = models.ForeignKey(Updated_Plan_Details, on_delete=models.SET_NULL, db_column='updated_plan_id', null=True, blank=True) # updated new coloumn
    created_at = models.CharField(max_length=100, blank=True, null=True)
    updated_at = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        db_table ='blacklisted_details'


class Updated_Api_export(models.Model):
    client_id = models.ForeignKey(Client_data, on_delete=models.SET_NULL,null=True, blank=True)
    api_key = models.CharField(max_length=150,blank=True)
    api_key_status = models.BooleanField(default=False)
    product_logs_name = models.CharField(max_length=150,blank=True)
    api_type = models.CharField(max_length=150,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    product_name = models.CharField(max_length=150,blank=True)

    class Meta:
        db_table ='updated_api_export'   


# Trace License_Management table added
class Trace_License_Management(models.Model):
    id = models.AutoField(primary_key=True)
    updated_plan_id = models.ForeignKey(Updated_Plan_Details, on_delete=models.SET_NULL, db_column='updated_plan_id', null=True, blank=True) # updated new coloumn
    control_server_domain  = models.CharField(max_length=250,blank=True)
    control_server_port  = models.CharField(max_length=250,blank=True)
    aggregator_domain  = models.CharField(max_length=250,blank=True)
    aggregator_port = models.CharField(max_length=250,blank=True)
    sensor_type =  models.CharField(max_length=250,blank=True)
    registry_address  = models.CharField(max_length=250,blank=True) # registry_server(column name updated in place)
    access_id =models.CharField(max_length=250,blank=True)
    access_key =  models.CharField(max_length=250,blank=True)
    sensor_key =  models.CharField(max_length=250,blank=True) # auto generated key (sensor_access_id,sensor_password)
    edition  = models.CharField(max_length=250,blank=True)
    company_index_name  = models.CharField(max_length=250,blank=True)
    sensor_name =  models.CharField(max_length=250,blank=True)
    location = models.CharField(max_length=250,blank=True)
    client_city = models.CharField(max_length=250,blank=True)
    client_latitude =  models.CharField(max_length=250,blank=True)
    client_longitude  = models.CharField(max_length=250,blank=True)
    client_country_code  = models.CharField(max_length=250,blank=True)
    client_country_name = models.CharField(max_length=250,blank=True)
    operating_env = models.CharField(max_length=250,blank=True)
    xdr_trace_status  = models.CharField(max_length=250,blank=True)
    license_start_date = models.CharField(max_length=250,blank=True)
    license_end_date = models.CharField(max_length=250,blank=True)
    diss_status = models.CharField(max_length=250,blank=True)
    diss_mode = models.CharField(max_length=250,blank=True)
    data_sharing_mode = models.CharField(max_length=250,blank=True)
    created_at = models.CharField(max_length=250,blank=True)
    updated_at = models.CharField(max_length=250,blank=True)
    sensor_create_count = models.CharField(max_length=150,blank=True)
    sensor_active_count = models.CharField(max_length=150,blank=True)
    aws_default_region = models.CharField(max_length=250,blank=True)

    class Meta:
        db_table ='trace_license_management'   


# Nids License_Management table added
class Nids_License_Management(models.Model):
    id = models.AutoField(primary_key=True)
    updated_plan_id = models.ForeignKey(Updated_Plan_Details, on_delete=models.SET_NULL, db_column='updated_plan_id', null=True, blank=True) # updated new coloumn
    control_server_domain  = models.CharField(max_length=250,blank=True)
    control_server_port  = models.CharField(max_length=250,blank=True)
    aggregator_domain  = models.CharField(max_length=250,blank=True)
    aggregator_port = models.CharField(max_length=250,blank=True)
    sensor_type =  models.CharField(max_length=250,blank=True)
    registry_address  = models.CharField(max_length=250,blank=True)
    sensor_key =  models.CharField(max_length=250,blank=True) # auto generated key (sensor_access_id,sensor_password)
    access_id =models.CharField(max_length=250,blank=True)
    access_key =  models.CharField(max_length=250,blank=True)
    edition  = models.CharField(max_length=250,blank=True)
    company_index_name  = models.CharField(max_length=250,blank=True)
    aws_default_region = models.CharField(max_length=250,blank=True)
    location = models.CharField(max_length=250,blank=True)
    client_city = models.CharField(max_length=250,blank=True)
    client_latitude =  models.CharField(max_length=250,blank=True)
    client_longitude  = models.CharField(max_length=250,blank=True)
    client_country_code  = models.CharField(max_length=250,blank=True)
    client_country_name = models.CharField(max_length=250,blank=True)
    xdr_nids_status  =  models.CharField(max_length=250,blank=True)
    license_start_date = models.CharField(max_length=250,blank=True)
    license_end_date = models.CharField(max_length=250,blank=True)
    operating_env = models.CharField(max_length=250,blank=True)
    data_sharing_mode = models.CharField(max_length=250,blank=True) # data type true and false
    created_at = models.CharField(max_length=250,blank=True)
    updated_at = models.CharField(max_length=250,blank=True)
    sensor_create_count = models.CharField(max_length=150,blank=True)
    sensor_active_count = models.CharField(max_length=150,blank=True)

    class Meta:
        db_table ='nids_license_management'

# Hids License_Management table added
class Hids_License_Management(models.Model):
    id = models.AutoField(primary_key=True)
    updated_plan_id = models.ForeignKey(Updated_Plan_Details, on_delete=models.SET_NULL, db_column='updated_plan_id', null=True, blank=True) # updated new coloumn
    control_server_domain  = models.CharField(max_length=250,blank=True)
    control_server_port  = models.CharField(max_length=250,blank=True)
    aggregator_domain  = models.CharField(max_length=250,blank=True)
    aggregator_port = models.CharField(max_length=250,blank=True)
    sensor_key =  models.CharField(max_length=250,blank=True) # auto generated key inplace of this columns (sensor_access_id,sensor_password)
    sensor_type =  models.CharField(max_length=250,blank=True)
    registry_address  = models.CharField(max_length=250,blank=True)
    access_id =models.CharField(max_length=250,blank=True)
    access_key =  models.CharField(max_length=250,blank=True)
    edition  = models.CharField(max_length=250,blank=True)
    company_index_name  = models.CharField(max_length=250,blank=True)
    aws_default_region = models.CharField(max_length=250,blank=True)
    location = models.CharField(max_length=250,blank=True)
    client_city = models.CharField(max_length=250,blank=True)
    client_latitude =  models.CharField(max_length=250,blank=True)
    client_longitude  = models.CharField(max_length=250,blank=True)
    client_country_code  = models.CharField(max_length=250,blank=True)
    client_country_name = models.CharField(max_length=250,blank=True)
    xdr_hids_manager_status  = models.CharField(max_length=250,blank=True)
    license_start_date = models.CharField(max_length=250,blank=True)
    license_end_date = models.CharField(max_length=250,blank=True)
    operating_env = models.CharField(max_length=250,blank=True)
    data_sharing_mode = models.CharField(max_length=250,blank=True)
    created_at = models.CharField(max_length=250,blank=True)
    updated_at = models.CharField(max_length=250,blank=True)
    sensor_create_count = models.CharField(max_length=150,blank=True)
    sensor_active_count = models.CharField(max_length=150,blank=True)

    class Meta:
        db_table ='hids_license_management'

# Soar License_Management table added
class Soar_License_Management(models.Model):
    id = models.AutoField(primary_key=True)
    updated_plan_id = models.ForeignKey(Updated_Plan_Details, on_delete=models.SET_NULL, db_column='updated_plan_id', null=True, blank=True) # updated new coloumn
    control_server_domain  = models.CharField(max_length=250,blank=True)
    aggregator_domain  = models.CharField(max_length=250,blank=True)
    aggregator_port = models.CharField(max_length=250,blank=True)
    sensor_type =  models.CharField(max_length=250,blank=True)
    registry_address  = models.CharField(max_length=250,blank=True)
    sensor_key =  models.CharField(max_length=250,blank=True) # auto generated key (sensor_access_id,sensor_password)
    access_id =models.CharField(max_length=250,blank=True)
    access_key =  models.CharField(max_length=250,blank=True)
    edition  = models.CharField(max_length=250,blank=True)
    company_index_name  = models.CharField(max_length=250,blank=True)
    aws_default_region = models.CharField(max_length=250,blank=True)
    location = models.CharField(max_length=250,blank=True)
    client_city = models.CharField(max_length=250,blank=True)
    client_latitude =  models.CharField(max_length=250,blank=True)
    client_longitude  = models.CharField(max_length=250,blank=True)
    client_country_code  = models.CharField(max_length=250,blank=True)
    client_country_name = models.CharField(max_length=250,blank=True)
    xdr_soar_status  = models.CharField(max_length=250,blank=True)
    soar_sensor_host_url = models.CharField(max_length=250,blank=True)
    backend_port = models.CharField(max_length=250,blank=True) 
    frontend_port = models.CharField(max_length=250,blank=True) 
    frontend_port_https = models.CharField(max_length=250,blank=True)
    shuffle_default_username = models.CharField(max_length=250,blank=True)
    shuffle_default_password = models.CharField(max_length=250,blank=True)
    shuffle_default_apikey = models.CharField(max_length=250,blank=True)
    license_start_date = models.CharField(max_length=250,blank=True)
    license_end_date = models.CharField(max_length=250,blank=True)
    operating_env = models.CharField(max_length=250,blank=True)
    created_at = models.CharField(max_length=250,blank=True)
    updated_at = models.CharField(max_length=250,blank=True)
    sensor_create_count = models.CharField(max_length=150,blank=True)
    sensor_active_count = models.CharField(max_length=150,blank=True)

    class Meta:
        db_table = 'soar_license_management' 

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