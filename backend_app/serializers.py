#  =========================================================================================================================================================================================================================================================================================
#  File Name: serializers.py
#  Description: Purpose of this file is to facilitate the serialization and deserialization of complex data types, such as Django models, querysets, and other Python objects, into a format that can be easily transmitted over the web, typically as part of API responses or requests.
#  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Master Dashboard
#  Author URL: https://whizhack.in

#  ==========================================================================================================================================================================================================================================================================================

from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password
from .postgresql_script import *
import json, boto3, botocore, random
from django.conf import settings
from django.core.files.storage import FileSystemStorage


class Organization_dataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization_data
        fields = ['organization_id','organization_name','organization_primary_email_id','organization_secondary_email_id',
        'organization_primary_contact_number','organization_secondary_contact_number',
        'organization_address','organization_city','organization_state',
        'organization_country','organization_pincode']

#------objective: updates encrypted password into DB along with other entered fields in dashboard----------------------
class DashboardAllFieldsSerializer(serializers.ModelSerializer):
    class Meta:

        model = Organization_data
        fields = ['organization_id','organization_name','organization_primary_email_id',
        'organization_secondary_email_id','organization_primary_contact_number',
        'organization_secondary_contact_number','organization_address','organization_city',
        'organization_state','organization_pincode', 'db_username', 'db_password']

class EncryptPasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model= Organization_data
        fields= ['organization_id','organization_name','organization_primary_email_id','organization_secondary_email_id','organization_primary_contact_number','organization_secondary_contact_number','organization_address','organization_city','organization_state','organization_pincode','plan_id','billing_id','country_id','timezone_id','customer_types','environment_type', 'trace_environment', 'wazuh_environment']


class Organization_withstatusSerializer(serializers.ModelSerializer):# has fields different than dashboard(working)
    plan_name = serializers.CharField(source="plan_id.plan_name", read_only=True)
    country_name = serializers.CharField(source="country_id.country_name", read_only=True)
    billing_types = serializers.CharField(source="billing_id.billing_types", read_only=True)
    class Meta:
        model = Organization_data
        fields = ['organization_id','organization_name','organization_primary_email_id','organization_secondary_email_id','organization_primary_contact_number','organization_secondary_contact_number','organization_address','organization_city','organization_state','organization_pincode', 'status_code', 'onboarding_timestamp','plan_name','country_name','billing_types','is_active']
    
#------objective: updates encrypted password into DB----------------------
class PasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model= Organization_data
        fields= ['db_username', 'db_password']
        validate_password = make_password('db_password')
   
    def update(self, instance, validated_data):
        validated_data['db_password'] = make_password(validated_data.get('db_password'))
        instance.db_password = validated_data['db_password']
        return super(PasswordSerializer, self).update(instance, validated_data)

#------objective:serializer for billing, plans---------------------
class Billings_Data_Serializer(serializers.ModelSerializer):# has fields different than dashboard
    
    class Meta:
        model = Billings_data
        fields = ['id','billing_types','billing_descriptions','billing_image']

class Plans_Data_Serializer(serializers.ModelSerializer):# has fields different than dashboard

    class Meta:
        model = Plans_data
        fields = ['id','plan_name','plan_descriptions','plan_image','plan_duration']  
        
#------objective: display Country table data----------------------
class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model= Country_data
        fields = '__all__'

#------objective: display Time_Zone table data----------------------
class TimeZoneSerializer(serializers.ModelSerializer):

    class Meta:
        model= Time_Zone_data
        fields = '__all__'

#------objective:serializer for billing, plans with date and time based on india---------------------
class Billings_Data_Serializer_Times(serializers.ModelSerializer):# has fields different than dashboard
    billing_creations_timestamp= serializers.DateTimeField(format=("%Y-%m-%d %H:%M:%S"))
    class Meta:
        model = Billings_data
        fields = ['id','billing_types','billing_descriptions','billing_image','billing_creations_timestamp']

class Plans_Data_Serializer_Times(serializers.ModelSerializer):# has fields different than dashboard
    plan_creations_timestamp= serializers.DateTimeField(format=("%Y-%m-%d %H:%M:%S"))

    class Meta:
        model = Plans_data
        fields = ['id','plan_name','plan_descriptions','plan_image','plan_creations_timestamp']

#------objective:serializer for store agent details with location in db ---------------------
class AgentSerializer(serializers.ModelSerializer):
   
    class Meta:
        model= Agent_data
        fields = ['id','org_location','db_username','db_password','attach_agent_group','attach_agent_network', 'attach_agent_key', 'organization_id', 'creation_timestamp', 'updation_timestamp','trace_attach_agent','wazuh_attach_agent']

#------objective:serializer to display users( Priya Duggal ) ---------------------
class UserdisplaySerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source="organization_id.organization_name", read_only=True)
    country_name = serializers.CharField(source="country.country_name", read_only=True)
    location_branchcode = serializers.CharField(source="location_id.branchcode", read_only=True)
    location_city = serializers.CharField(source="location_id.city", read_only=True)
    location_state = serializers.CharField(source="location_id.state", read_only=True)
    location_pincode = serializers.CharField(source="location_id.pincode", read_only=True)
    class Meta:
        model= Client_data
        fields = ['id','user_type','location_id', 'organization_name', 'first_name', 'last_name', 'email', 'username','trading_name', 'registration_no', 'government_tax', 'company_type_id', 'profile_photo', 'contact_number', 'gender', 'address_1', 'address_2', 'city', 'state', 'zipcode', 'is_active', 'created_at', 'role_id_id', 'allow_MFA', 'first_config','country_name', 'location_branchcode', 'location_city', 'location_state', 'location_pincode']
       
#------objective:serializer for storing user details in db( Priya Duggal ) ---------------------
class UseraddSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(source="client_password", read_only=True)
    class Meta:
        model= Client_data
        fields = ['id', 'email', 'first_name', 'last_name', 'username', 'country','role_id','contact_number', 'organization_id', 'client_password', 'password','location_id']

    # def validate(self, data):
    #     fn = str(data.get('first_name'))
    #     ln = str(data.get('last_name'))
    #     if fn.isalpha() and ln.isalpha():
    #         return data 
    #     else:
    #         raise serializers.ValidationError("special_char_not_allowed_in_name")
       
#------objective:serializer for storing email config details in db ( Priya Duggal ) ---------------------
class emailConfigSerializer(serializers.ModelSerializer):
   
    class Meta:
        model= email_config_data
        fields = ['id','host','port', 'auth', 'auth_type', 'username', 'password']

#To get serializer with joining table fkey
class Joinfkey_Serializer(serializers.ModelSerializer):
    plan_name = serializers.CharField(source="plan_id.plan_name", read_only=True)
    billing_types = serializers.CharField(source="billing_id.billing_types", read_only=True)
    country_name = serializers.CharField(source="country_id.country_name", read_only=True)
    Time_Zone= serializers.CharField(source="timezone_id.Time_Zone", read_only=True)
    class Meta:
        model = Organization_data
        fields = ['organization_id','organization_name','organization_primary_email_id',
        'organization_secondary_email_id','organization_primary_contact_number',
        'organization_secondary_contact_number','organization_address',
        'organization_city','organization_state','organization_pincode',
        'status_code', 'db_username', 'db_password', 'onboarding_timestamp',
        'customer_types','plan_name','billing_types','country_name','Time_Zone']


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'name', 'role', 'ability']
        extra_kwargs = {
            'password' : {'write_only':True}
        }
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255)
    class Meta:
        model = User
        fields = ['email', 'password']
        

class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255)
    class Meta:
        model = User
        fields = ['id','email', 'name', 'role', 'ability']

class LogsSerializer(serializers.ModelSerializer):
    # date_time =  serializers.DateTimeField(format=("%Y-%m-%d %H:%M:%S"))
    class Meta:
        model= ApiLogs
        fields = '__all__'

        # ---------------------------------------------------------------------------------------------------------------------------

class Api__Client_LogsSerializer(serializers.ModelSerializer):# has fields different than dashboard
    master_name = serializers.CharField(source='master_id.name',read_only = True)
    email =  serializers.CharField(source='client_id.email',read_only = True)
    class Meta:
        model = ApiLogs
        fields = ['id','master_name','email','type','date_time','ip','browser_type','req_method','description']

class Api_Master_LogsSerializer(serializers.ModelSerializer):# has fields different than dashboard
    email = serializers.CharField(source='master_id.email',read_only = True)
    class Meta:
        model = ApiLogs
        fields = ['id','email','type','date_time','ip','browser_type','req_method','description']

#To get serializers apilogs of users
class ApiLogs_serializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='client_id.first_name',read_only = True)
    last_name = serializers.CharField(source='client_id.last_name',read_only = True)
    email = serializers.CharField(source='client_id.email',read_only = True)
    class Meta:        
            model = ApiLogs
            fields = ['type','date_time','ip','browser_type','req_method','description','first_name','last_name', 'email']

 
class Application_Serializer(serializers.ModelSerializer):
    class Meta:
        model= Applications
        fields = ['application_name','application_descriptions']   

class Application_Views_Serializer(serializers.ModelSerializer):
    application_steps = serializers.SerializerMethodField()
    # application_image = serializers.SerializerMethodField()
    class Meta:
        model= Applications
        fields = ['id','application_name','application_descriptions','created_at', 'application_steps','application_image']
    
    def get_application_steps(self, obj):
        steps = obj.application_steps
        steps_str = json.dumps(steps)
        application_steps = json.loads(steps_str)
        return application_steps
    
    # def get_application_image(self, obj):
    #     image = obj.application_image
    #     image_name = str(image)
    #     local_storage = FileSystemStorage()
    #     base_url = self.context.get('base_url')
    #     if not local_storage.exists(image_name):
    #         session = boto3.Session(aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    #         s3 = session.resource('s3')
    #         bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    #         try:
    #             s3.Bucket(bucket_name).download_file('applicationimages/'+image_name, 'static/image/'+image_name)
    #         except botocore.exceptions.ClientError as e:
    #             if e.response['Error']['Code'] == "404":
    #                 error = {"err":"The object does not exist on s3 bucket"}
    #                 raise serializers.ValidationError(error)
    #     updated_image = base_url+'image/'+str(image)
    #     return updated_image

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        image_name = str(instance.application_image)
        local_storage = FileSystemStorage()
        base_url = self.context.get('base_url')
        if not local_storage.exists(image_name):
            session = boto3.Session(aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
            s3 = session.resource('s3')
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            try:
                s3.Bucket(bucket_name).download_file('applicationimages/'+image_name, 'static/image/'+image_name)
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == "404":
                    error = {"err":"The object does not exist on s3 bucket"}
                    raise serializers.ValidationError(error)
        ret['application_image'] = base_url+'image/'+image_name
        return ret
        
#--------------------Agent table serialiser for organisation_id fkey----------------------#
class AgentfkeySerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source="organization_id.organization_name", read_only=True)
    class Meta:
        model = Agent_data
        fields = ['id','org_location','attach_agent_group','organization_name','creation_timestamp', 'attach_agent_network', 'wazuh_attach_agent','trace_attach_agent','creation_timestamp','attach_agent_key','hids_assets_agent','hids_assets_agent','hids_event_agent','hids_incident_agent','hids_alert_agent','nids_alert_agent','nids_assets_agent','nids_event_agent','nids_global_agent','nids_incident_agent','nids_nmap_agent','trace_alert_agent','trace_event_agent','trace_global_agent','trace_incident_agent', 'trace_dpi_agent','soar_agent','tps_agent','ess_agent','sbs_agent','tptf_agent','mm_agent','hc_agent','is_active']

#To get config serializers
class Config_Serializer(serializers.ModelSerializer):

    class Meta:        
            model = Init_Configs
            fields = '__all__'

#To get email config serializers
class Email_Config_Serializer(serializers.ModelSerializer):
    class Meta:        
            model = Init_Configs
            fields = ['id','trace_sensor','accuracy_val','severity_val','platform_val','email_ids','config_type']

#To create dashboard config init_config
class Platf_Severity_Serializer(serializers.ModelSerializer):
    class Meta:        
            model = Init_Configs
            fields = ['config_type','platform_val','severity_val','accuracy_val','org_id'] 

# To show organization how many come users
class OrgUserNumSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(read_only=True)

    def get_username(self, obj):
        return '{} {}'.format(obj.first_name, obj.last_name) 
    class Meta:
        model= Client_data
        fields = ['email', 'username','role_id','first_config','contact_number','created_at']
           
# To add data in app details table
class AppDetailsSerializer(serializers.ModelSerializer):
    class Meta:        
            model = Applications
            fields = ['application_name','integration_status','application_descriptions','application_steps', 'application_image']

# To get page permissions
class PagePermissionsSerializer(serializers.ModelSerializer):
    class Meta:        
            model = Page_Permissions
            fields = ['id','env_trace','org_id', 'env_wazuh']    

# To add page permissions
class AddPagePermissionsSerializer(serializers.ModelSerializer):
    class Meta:        
            model = Page_Permissions
            fields = ['id','env_trace','location_id','env_wazuh','env_hids','env_nids','default_page','xdr_live_map','env_hc','env_mm','env_tptf','env_sbs','env_ess','env_tps','env_soar','updated_plan_id']     

# # To add organization location(attach_location) working
class AddLocationStepOneSerializer(serializers.ModelSerializer):
    org_name = serializers.CharField(source="org_id.organization_name", read_only=True)
    
    class Meta:        
            model = Attach_Location
            fields = ['id','org_id','address','branchcode','city','state', 'pincode','country_id','pincode','timezone_id','billing_id','customer_types','environment_type','email','phone_number','fax_number','gst_id','tan_id','cin_id','pan_id','gst_image','tan_image','cin_image','pan_image','org_name']

    def create(self, validated_data):
        org_name = str(validated_data['org_id'].organization_name.strip(u'\u200b')).lower().replace(" ", "")[:3] #removing unicode if any and removing whitespaces from org_name
        city_name = validated_data['city'].strip(u'\u200b').lower().replace(" ", "")[:3]
        random_number = random.randint(1000, 9999)
        branchcode = f"{org_name}{city_name}{random_number}"
        validated_data['branchcode'] = branchcode
        return super().create(validated_data)
    
# To display locations (from attach_location table)
class GetLocationSerializer(serializers.ModelSerializer): #get single object from location table
    db_username = serializers.SerializerMethodField()
    db_password = serializers.SerializerMethodField()
    db_host = serializers.SerializerMethodField()
    db_port = serializers.SerializerMethodField()
    organization_name = serializers.CharField(source="org_id.organization_name", read_only=True)
    organization_id = serializers.CharField(source="org_id.organization_id", read_only=True)
    plan_name = serializers.CharField(source="plan_id.plan_name", read_only=True)
    country_name = serializers.CharField(source="country_id.country_name", read_only=True)
    billing_types = serializers.CharField(source="billing_id.billing_types", read_only=True)
    plan_name = serializers.CharField(source="activated_plan_id.plan_name", read_only=True)
    plan_start_date = serializers.CharField(source="activated_plan_id.plan_start_date", read_only=True)
    plan_end_date = serializers.CharField(source="activated_plan_id.plan_end_date", read_only=True)

    class Meta:        
            model = Attach_Location
            fields = ['id','organization_id','organization_name','address','branchcode','city','state','country_name','pincode','timezone_id','plan_name','billing_types','customer_types','environment_type','email','phone_number','fax_number','gst_id','tan_id','cin_id','pan_id','gst_image','tan_image','cin_image','pan_image','is_active','created_at', 'activated_plan_id','db_username', 'db_password','db_host', 'db_port', 'plan_start_date', 'plan_end_date']
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        gst_image = str(instance.gst_image)
        tan_image = str(instance.tan_image)
        pan_image = str(instance.pan_image)
        cin_image = str(instance.cin_image)
        local_storage = FileSystemStorage()
        base_url = self.context.get('base_url')
        field_value = [gst_image, tan_image, pan_image, cin_image]
        for i,n in enumerate(field_value):
            if not local_storage.exists(n):
                session = boto3.Session(aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
                s3 = session.resource('s3')
                bucket_name = settings.AWS_STORAGE_BUCKET_NAME
                try:
                    s3.Bucket(bucket_name).download_file('company-credential-details/'+n, 'static/image/'+n)
                except botocore.exceptions.ClientError as e:
                    if e.response['Error']['Code'] == "404":
                        error = {"err":"The object does not exist on s3 bucket"}
                        raise serializers.ValidationError(error)
        ret['gst_image'] = base_url+'image/'+gst_image
        ret['tan_image'] = base_url+'image/'+tan_image
        ret['pan_image'] = base_url+'image/'+pan_image
        ret['cin_image'] = base_url+'image/'+cin_image
        return ret
    
    def get_db_username(self, obj):
        try:
            return obj.agent_data_set.values_list('db_username', flat=True)[0]
        except IndexError:
            return None

    def get_db_password(self, obj):
        try:
            return obj.agent_data_set.values_list('db_password', flat=True)[0]
        except IndexError:
            return None
    
    def get_db_host(self, obj):
        try:
            return obj.agent_data_set.values_list('db_host', flat=True)[0]
        except IndexError:
            return None

    def get_db_port(self, obj):
        try:
            return obj.agent_data_set.values_list('db_port', flat=True)[0]
        except IndexError:
            return None

# To get all data of nested json function
class DisplayAllOrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model= Organization_data
        fields = '__all__'

###used for bothstatus org details display from location table#######
class Org_User_Serializers(serializers.ModelSerializer):
    organization_name = serializers.CharField(source="organization_id.organization_name", read_only=True)
    role = serializers.CharField(source="role_id.role", read_only=True)
    class Meta:
        model= Client_data
        fields = ['username','email','contact_number','is_active','role','organization_name']
   
     
#get all location data within an organization #similar to bothstatus url
class GetLocationsInOrgSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Organization_data
        fields = ['organization_id','organization_name']

# get org-name in add location-step-1
class AddLocationGetOrgNameSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Organization_data
        fields = ['organization_id', 'organization_name']

#-----testing-------------------------
class ActivateLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page_Permissions
        fields = ['env_trace', 'env_wazuh','env_hids','env_nids','default_page', 'location_id', 'org_id','xdr_live_map','env_hc','env_mm','env_tptf','env_sbs','env_ess','env_tps','env_soar','updated_plan_id']

class LocationDetailsSerializer(serializers.ModelSerializer):        
    organization_name = serializers.CharField(source="org_id.organization_name", read_only=True)
    
   
    class Meta:
        model = Attach_Location
        fields = ['id','org_id' ,'organization_name','pan_id','tan_image','tan_id','gst_image','gst_id','fax_number','phone_number','email','cin_id','cin_image','address','branchcode','city','state','plan_id','billing_id','country_id','timezone_id','pincode','customer_types','environment_type','created_at','updated_at','is_active'] 

class  InitConfigsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Init_Configs
        fields = '__all__'



class  PagepermissionAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page_Permissions
        fields = '__all__'

class  AgentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent_data
        fields = '__all__'


#To create dashboard config init_config
class DahboardConfigSerializer(serializers.ModelSerializer):
    class Meta:        
            model = Init_Configs
            fields = ['config_type','platform_val','severity_val','accuracy_val','trace_sensor','location_id'] 

class EmailConfigSerializer(serializers.ModelSerializer):
    class Meta:        
            model = Init_Configs
            fields = ['config_type','platform_val','severity_val','accuracy_val','trace_sensor','location_id','email_ids']             

#To get notification config serializers
class NotificationConfigSerializer(serializers.ModelSerializer):
    class Meta:        
            model = Init_Configs
            fields =  fields = ['config_type','platform_val','severity_val','accuracy_val','trace_sensor','location_id','time_interval_val'] 

class AllagentDetailsSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source="organization_id.organization_name", read_only=True)
    # branchcode = serializers.CharField(source="org_location.branchcode", read_only=True)
    location_city = serializers.CharField(source="org_location.city", read_only=True)
    class Meta:        
            model = Agent_data
            fields = ['organization_name','location_city','org_location','organization_id','attach_agent_key','trace_incident_agent','nids_event_agent','nids_alert_agent','nids_incident_agent','nids_assets_agent','nids_nmap_agent','nids_global_agent','trace_event_agent','trace_alert_agent','trace_incident_agent','trace_global_agent','trace_dpi_agent','hids_event_agent','hids_alert_agent','hids_incident_agent','hids_assets_agent','is_active','soar_agent','tps_agent','ess_agent','sbs_agent','tptf_agent','mm_agent','hc_agent']

# To add page permissions
class UpdatePagePermissionsSerializer(serializers.ModelSerializer):
    class Meta:        
            model = Page_Permissions
            fields = ['id','env_trace','env_wazuh','env_hids','env_nids','default_page','xdr_live_map','env_hc','env_mm','env_tptf','env_sbs','env_ess','env_tps','env_soar']  

class UpdatePlanWithPagePermissionsSerializer(serializers.ModelSerializer):
    class Meta:        
            model = Updated_Plan_Details
            fields = ['env_trace','env_wazuh','env_hids','env_nids','default_page','xdr_live_map','env_hc','env_mm','env_tptf','env_sbs','env_ess','env_tps','env_soar']

class UpdateAllagentDetailsSerializer(serializers.ModelSerializer):
    class Meta:        
            model = Agent_data
            fields = ['is_active']

# To update opensearch connection credentials in agent table
class UpdateAgentDataSerializer(serializers.ModelSerializer):
    class Meta:        
            model = Agent_data
            fields = ['db_username', 'db_password', 'db_host', 'db_port']        

#To get email id from client data
class Clent_Email_Serializer(serializers.ModelSerializer):
    class Meta:
            model = Client_data
            fields = ['id','email']

# This class only return list format of sensor_name
class SensorNameListField(serializers.Field):
    def to_representation(self, obj):
        if obj:
            return [s.strip("'") for s in obj.strip("()").split(',')]
        return []

    def to_internal_value(self, data):
        if isinstance(data, list):
            return f"({' '.join([repr(s) for s in data])})"
        raise serializers.ValidationError("Invalid sensor_name format. Expected list.")
    

# # To add Trace_License_Management models
class GetTraceLicenseManagementSerializer(serializers.ModelSerializer):
    class Meta:        
            model = Trace_License_Management
            fields = ['control_server_domain','control_server_port','aggregator_domain','aggregator_port','sensor_key','sensor_type','registry_address','access_id','access_key','edition','sensor_name','location','client_city','client_latitude','client_longitude','client_country_code','client_country_name','xdr_trace_status','company_index_name','license_start_date','license_end_date','diss_status','diss_mode','data_sharing_mode','created_at','updated_at','updated_plan_id','operating_env','sensor_create_count','location','aws_default_region','sensor_active_count']  


# # To add Trace_License_Management models
class TraceLicenseManagementSerializer(serializers.ModelSerializer):
    class Meta:        
            model = Trace_License_Management 
            fields = ['control_server_domain','aggregator_domain','aggregator_port','sensor_type','registry_address','access_id','access_key','sensor_key','edition','sensor_name','location','client_city','client_latitude','client_longitude','client_country_code','client_country_name','xdr_trace_status','license_start_date','license_end_date','diss_status','diss_mode','data_sharing_mode','created_at','updated_at','updated_plan_id','operating_env','sensor_create_count','location','sensor_active_count','aws_default_region']  

# # To add Nids_License_Management models
class NidsLicenseManagementSerializer(serializers.ModelSerializer):
    class Meta:        
            model = Nids_License_Management
            fields = ['control_server_domain','aggregator_domain','aggregator_port','sensor_type','registry_address','access_id','access_key','edition','location','client_city','client_latitude','client_longitude','client_country_code','xdr_nids_status','company_index_name','license_start_date','license_end_date','data_sharing_mode','created_at','updated_at','aws_default_region','operating_env','updated_plan_id','sensor_key','sensor_create_count','sensor_active_count'] 

    def update(self, instance, validated_data):
    # Explicitly set sensor_create_count and sensor_active_count to the same value
        sensor_create_count = validated_data.get('sensor_create_count', instance.sensor_create_count)
        validated_data['sensor_create_count'] = sensor_create_count
        validated_data['sensor_active_count'] = sensor_create_count

        # Update the instance with the validated data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance    



# # To add Hids_License_Management models
class HidsLicenseManagementSerializer(serializers.ModelSerializer):
    class Meta:        
            model = Hids_License_Management
            fields = ['control_server_domain','aggregator_domain','aggregator_port','sensor_type','registry_address','access_id','access_key','edition','location','client_city','client_latitude','client_longitude','client_country_code','client_country_name','xdr_hids_manager_status','license_start_date','license_end_date','data_sharing_mode','created_at','updated_at','aws_default_region','operating_env','updated_plan_id','sensor_key','sensor_create_count','sensor_active_count']

    def update(self, instance, validated_data):
    # Explicitly set sensor_create_count and sensor_active_count to the same value
        sensor_create_count = validated_data.get('sensor_create_count', instance.sensor_create_count)
        validated_data['sensor_create_count'] = sensor_create_count
        validated_data['sensor_active_count'] = sensor_create_count

        # Update the instance with the validated data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance         


# To add Soar_License_Management models
class SoarSensorDetailsSerializer(serializers.ModelSerializer):
    class Meta:        
            model = Soar_License_Management
            fields = ['control_server_domain','aggregator_domain','aggregator_port','sensor_type','registry_address','access_id','access_key','edition','location','client_city','client_latitude','client_longitude','client_country_code','client_country_name','xdr_soar_status','license_start_date','license_end_date','created_at','updated_at','aws_default_region','operating_env','soar_sensor_host_url','updated_plan_id','sensor_key','sensor_create_count','sensor_active_count','backend_port','frontend_port','frontend_port_https','shuffle_default_username','shuffle_default_password','shuffle_default_apikey'] 

    def update(self, instance, validated_data):
    # Explicitly set sensor_create_count and sensor_active_count to the same value
        sensor_create_count = validated_data.get('sensor_create_count', instance.sensor_create_count)
        validated_data['sensor_create_count'] = sensor_create_count
        validated_data['sensor_active_count'] = sensor_create_count

        # Update the instance with the validated data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance         


# health check sensor alert client_email_id, admin_email_id
class HealthCheckSensorAlertEmailSerializer(serializers.ModelSerializer):
     class Meta:
          model = Init_Configs
          fields = ['sensor_alert_client', 'sensor_alert_admin']


# add updated plan step-one
class AddPlanStepOneSerializer(serializers.ModelSerializer):
     id = serializers.CharField(read_only=True)

     class Meta:
          model = Updated_Plan_Details
          fields = ['id', 'plan_name', 'plan_start_date', 'plan_end_date', 'plan_descriptions', 'plan_creations_timestamp', 'plan_key']


# add updated plan step-two
class AddPlanStepTwoSerializer(serializers.ModelSerializer):
     id = serializers.CharField(read_only=True)
     
     class Meta:
          model = Updated_Plan_Details
          fields = ['id', 'default_page', 'env_trace', 'env_nids', 'env_hids', 'env_soar', 'xdr_live_map', 'env_hc', 'env_mm', 'env_tptf', 'env_sbs', 'env_ess', 'env_tps']

# add updated plan step-three for Trace License
class AddTraceLicensePlanStepThreeSerializer(serializers.ModelSerializer):
     class Meta:
          model = Trace_License_Management
          fields = ['control_server_domain', 'aggregator_port', 'aggregator_domain', 'sensor_type', 'registry_address', 'access_id', 'access_key', 'edition', 'sensor_name', 'location', 'client_city', 'client_latitude', 'client_longitude', 'client_country_code', 'client_country_name', 'license_start_date', 'license_end_date', 'xdr_trace_status', 'diss_status', 'diss_mode', 'data_sharing_mode', 'operating_env', 'sensor_create_count', 'sensor_active_count', 'aws_default_region', 'created_at', 'updated_plan_id', 'sensor_key']


# add updated plan step-three for NIDS License
class AddNidsLicensePlanStepThreeSerializer(serializers.ModelSerializer):
     class Meta:
          model = Nids_License_Management
          fields = ['control_server_domain', 'aggregator_port', 'aggregator_domain', 'sensor_type', 'registry_address', 'access_id', 'access_key', 'edition', 'location', 'client_city', 'client_latitude', 'client_longitude', 'client_country_code', 'client_country_name', 'license_start_date', 'license_end_date', 'xdr_nids_status', 'aws_default_region', 'data_sharing_mode', 'operating_env', 'sensor_create_count', 'sensor_active_count', 'created_at', 'updated_plan_id', 'sensor_key']


# add updated plan step-three for HIDS License
class AddHidsLicensePlanStepThreeSerializer(serializers.ModelSerializer):
     class Meta:
          model = Hids_License_Management
          fields = ['xdr_hids_manager_status', 'sensor_create_count', 'sensor_active_count', 'created_at', 'control_server_domain', 'aggregator_port', 'aggregator_domain', 'sensor_type', 'registry_address', 'access_id', 'access_key', 'edition', 'location', 'client_city', 'client_latitude', 'client_longitude', 'client_country_code', 'client_country_name', 'license_start_date', 'license_end_date', 'aws_default_region', 'data_sharing_mode', 'operating_env', 'updated_plan_id', 'sensor_key']


# add updated plan step-three for Soar
class AddSoarLicensePlanStepThreeSerializer(serializers.ModelSerializer):
     class Meta:
          model = Soar_License_Management
          fields = ['sensor_create_count', 'sensor_active_count', 'created_at', 'xdr_soar_status', 'control_server_domain', 'aggregator_port', 'aggregator_domain', 'sensor_type', 'registry_address', 'access_id', 'access_key', 'edition', 'location', 'client_city', 'client_latitude', 'client_longitude', 'client_country_code', 'client_country_name', 'license_start_date', 'license_end_date', 'aws_default_region', 'operating_env', 'soar_sensor_host_url','backend_port',' frontend_port','frontend_port_https','shuffle_default_username','shuffle_default_password','shuffle_default_apikey', 'updated_plan_id', 'sensor_key']

# get updated plans
class DisplayUpdatedPlanSerializer(serializers.ModelSerializer):
     class Meta:
          model = Updated_Plan_Details
          fields = '__all__'

# get single plan on basis of plan_id
class DisplayTraceLicenseSerializer(serializers.ModelSerializer):
    class Meta:
          model = Trace_License_Management
          fields = '__all__'
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        sensor_name = str(instance.sensor_name)

        # Remove all spaces, parentheses, and single quotes
        sensor_name = sensor_name.replace(' ', '').strip('()').replace("'", "")
        
        ret['sensor_name'] = sensor_name
        return ret



class DisplayNidsLicenseSerializer(serializers.ModelSerializer):
     class Meta:
          model = Nids_License_Management
          fields = '__all__'

class DisplayHidsLicenseSerializer(serializers.ModelSerializer):
     class Meta:
          model = Hids_License_Management
          fields = '__all__'

class DisplaySoarLicenseSerializer(serializers.ModelSerializer):
     class Meta:
          model = Soar_License_Management
          fields = '__all__'

# # To add Nids_License_Management models
class DecreaseNidsLicenseManagementSerializer(serializers.ModelSerializer):
    class Meta:        
            model = Nids_License_Management
            fields = ['control_server_domain','aggregator_domain','aggregator_port','sensor_type','registry_address','access_id','access_key','edition','location','client_city','client_latitude','client_longitude','client_country_code','client_country_name','xdr_nids_status','company_index_name','license_start_date','license_end_date','data_sharing_mode','aws_default_region','operating_env','updated_plan_id','sensor_key','sensor_create_count','sensor_active_count','aws_default_region']                                          


class DecreaseTraceLicenseManagementSerializer(serializers.ModelSerializer):
    sensor_name = serializers.CharField()
   
    class Meta:        
            model = Trace_License_Management
            fields = ['control_server_domain','aggregator_domain','aggregator_port','sensor_type','registry_address','access_id','access_key','sensor_key','edition','sensor_name','location','client_city','client_latitude','client_longitude','client_country_code','client_country_name','xdr_trace_status','company_index_name','license_start_date','license_end_date','diss_status','diss_mode','data_sharing_mode','updated_plan_id','operating_env','sensor_create_count','sensor_active_count','location','aws_default_region']

# # To add Hids_License_Management models
class DecreaseHidsLicenseManagementSerializer(serializers.ModelSerializer):
    xdr_hids_status = serializers.SerializerMethodField()
    class Meta:        
            model = Hids_License_Management
            fields = ['control_server_domain','aggregator_domain','aggregator_port','sensor_type','registry_address','access_id','access_key','edition','location','client_city','client_latitude','client_longitude','client_country_code','client_country_name','company_index_name','license_start_date','license_end_date','data_sharing_mode','aws_default_region','operating_env','updated_plan_id','sensor_key','sensor_create_count','sensor_active_count','xdr_hids_status']
    def get_xdr_hids_status(self, obj):
        # Here, you can define how to calculate or transform the xdr_hids_status field
        # For example, if xdr_hids_manager_status exists in the model, you can simply return its value
        return obj.xdr_hids_manager_status

# To add Hids_License_Management models
class DecreaseSoarLicenseManagementSerializer(serializers.ModelSerializer):
    class Meta:        
            model = Soar_License_Management
            fields = ['control_server_domain','aggregator_domain','aggregator_port','sensor_type','registry_address','access_id','access_key','edition','location','client_city','client_latitude','client_longitude','client_country_code','client_country_name','xdr_soar_status','company_index_name','license_start_date','license_end_date','backend_port','frontend_port','frontend_port_https','shuffle_default_username','shuffle_default_password','shuffle_default_apikey','aws_default_region','operating_env','soar_sensor_host_url','updated_plan_id','sensor_key','sensor_create_count','sensor_active_count'] 

class HealthCheckSensorAlertEmailSerializer(serializers.ModelSerializer):
     class Meta:
          model = Init_Configs
          fields = ['sensor_alert_client', 'sensor_alert_admin']


# To get all hids data behalf of env type
class AlldataAgentPermissionsSerializer(serializers.ModelSerializer):
    class Meta:        
            model = Agent_data
            fields = ['hids_event_agent','hids_alert_agent','hids_incident_agent','hids_assets_agent']

# To get all hids data behalf of env type
class AlldataAgentPermissionsSerializer(serializers.ModelSerializer):
    class Meta:        
            model = Agent_data
            fields = ['hids_event_agent','hids_alert_agent','hids_incident_agent','hids_assets_agent']

# To get all nids behalf of env type
class NidsAlldataAgentPermissionsSerializer(serializers.ModelSerializer):
    class Meta:        
            model = Agent_data
            fields = ['nids_event_agent','nids_alert_agent','nids_incident_agent','nids_assets_agent','nids_nmap_agent']

# To get all trace data behalf of env type
class TraceAlldataAgentPermissionsSerializer(serializers.ModelSerializer):
    class Meta:        
            model = Agent_data
            fields = ['trace_event_agent','trace_alert_agent','trace_incident_agent','trace_global_agent','trace_dpi_agent']

# To get all wazuh data behalf of env type
class WazuhAlldataAgentPermissionsSerializer(serializers.ModelSerializer):
    class Meta:        
            model = Agent_data
            fields = ['wazuh_attach_agent']

# To get all health check serializers data behalf of env type
class HealthCheckAlldataAgentPermissionsSerializer(serializers.ModelSerializer):
    class Meta:        
            model = Agent_data
            fields = ['hc_agent']            

# To get all soar env check serializers data behalf of env type
class SoarAlldataAgentPermissionsSerializer(serializers.ModelSerializer):
    class Meta:        
            model = Agent_data
            fields = ['soar_agent']  

# To get all ess_agent env check serializers data behalf of env type
class EssAgentAlldataAgentPermissionsSerializer(serializers.ModelSerializer):
    class Meta:        
            model = Agent_data
            fields = ['ess_agent']    

# To get all ess_agent env check serializers data behalf of env type
class TpsAgentAlldataAgentPermissionsSerializer(serializers.ModelSerializer):
    class Meta:        
            model = Agent_data
            fields = ['tps_agent']  

# To get all sbs_agent env check serializers data behalf of env type
class SbsAgentAlldataAgentPermissionsSerializer(serializers.ModelSerializer):
    class Meta:        
            model = Agent_data
            fields = ['sbs_agent']      

# To get all tptf_agent env check serializers data behalf of env type
class TptfAgentAlldataAgentPermissionsSerializer(serializers.ModelSerializer):
    class Meta:        
            model = Agent_data
            fields = ['tptf_agent']  

# To get all tptf_agent env check serializers data behalf of env type
class MmAgentAlldataAgentPermissionsSerializer(serializers.ModelSerializer):
    class Meta:        
            model = Agent_data
            fields = ['mm_agent'] 


 # Upgrade plan2 details api
class Plan2DetailsSerializer(serializers.ModelSerializer):
    class Meta:        
            model = Updated_Plan_Details
            fields = ['plan_name','plan_descriptions','plan_start_date','plan_end_date','plan_creations_timestamp','plan_updations_timestamp'] 
           
# Upgrade plan2 details           
# add updated plan step-three for Trace License
class UpgradeTraceLicensePlanStepThreeSerializer(serializers.ModelSerializer):
     class Meta:
          model = Trace_License_Management
          fields = ['control_server_domain', 'aggregator_port', 'aggregator_domain', 'sensor_type', 'registry_address', 'access_id', 'access_key', 'edition', 'sensor_name', 'location', 'client_city', 'client_latitude', 'client_longitude', 'client_country_code', 'client_country_name', 'license_start_date', 'license_end_date', 'xdr_trace_status', 'diss_status', 'diss_mode', 'data_sharing_mode', 'operating_env', 'sensor_create_count', 'aws_default_region', 'created_at','updated_at','sensor_create_count','sensor_active_count','sensor_key']


# add updated plan step-three for NIDS License
class UpgradeNidsLicensePlanStepThreeSerializer(serializers.ModelSerializer):
     class Meta:
          model = Nids_License_Management
          fields = ['control_server_domain', 'aggregator_port', 'aggregator_domain', 'sensor_type', 'registry_address', 'access_id', 'access_key', 'edition', 'location', 'client_city', 'client_latitude', 'client_longitude', 'client_country_code', 'client_country_name', 'license_start_date', 'license_end_date', 'xdr_nids_status', 'aws_default_region', 'data_sharing_mode', 'operating_env', 'sensor_create_count','created_at','updated_at','sensor_create_count','sensor_active_count','sensor_key']


# add updated plan step-three for HIDS License
class UpgradeHidsLicensePlanStepThreeSerializer(serializers.ModelSerializer):
     class Meta:
          model = Hids_License_Management
          fields = ['xdr_hids_manager_status','sensor_active_count', 'created_at', 'control_server_domain', 'aggregator_port', 'aggregator_domain', 'sensor_type', 'registry_address', 'access_id', 'access_key', 'edition', 'location', 'client_city', 'client_latitude', 'client_longitude', 'client_country_code', 'client_country_name', 'license_start_date', 'license_end_date', 'aws_default_region', 'data_sharing_mode', 'operating_env','updated_at','sensor_create_count','sensor_active_count','sensor_key']



class UpgradeSoarLicensePlanStepThreeSerializer(serializers.ModelSerializer):
     class Meta:
          model = Soar_License_Management
          fields = ['sensor_create_count','created_at','xdr_soar_status', 'control_server_domain', 'aggregator_port', 'aggregator_domain', 'sensor_type', 'registry_address', 'access_id', 'access_key', 'edition', 'location', 'client_city', 'client_latitude', 'client_longitude', 'client_country_code', 'client_country_name', 'license_start_date', 'license_end_date', 'aws_default_region', 'operating_env', 'soar_sensor_host_url','backend_port','frontend_port','frontend_port_https','shuffle_default_username','shuffle_default_password','shuffle_default_apikey','updated_at','sensor_create_count','sensor_active_count','sensor_key']  

class UpgradePlan2teLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Updated_Plan_Details
        fields = ['env_trace','env_wazuh','env_hids','env_nids','default_page','xdr_live_map','env_hc','env_mm','env_tptf','env_sbs','env_ess','env_tps','env_soar']                 