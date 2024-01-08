#  =========================================================================================================================================================================================================================================================================================
#  File Name: serializers.py
#  Description: Purpose of this file is to facilitate the serialization and deserialization of complex data types, such as Django models, querysets, and other Python objects, into a format that can be easily transmitted over the web, typically as part of API responses or requests.
#  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  ==========================================================================================================================================================================================================================================================================================


from urllib import request
from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth import password_validation
import re, json
import boto3, botocore
from django.conf import settings
from django.core.files.storage import FileSystemStorage



# validators
def password_validate_function(value):
    if len(value) < 8:
        raise serializers.ValidationError("Password must contain 8 characters")
    elif not re.findall('\d', value):
        raise serializers.ValidationError("Password must contain at least 1 digit, 0-9.")
    elif not re.findall('[A-Z]',value):
        raise serializers.ValidationError("Password must contain at least 1 uppercase letter, A-Z.")
    elif not re.findall('[a-z]', value):
        raise serializers.ValidationError("Password must contain at least 1 lowercase letter, a-z.")
    elif not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', value):
        raise serializers.ValidationError("Password must contain at least 1 symbol: ()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?")


class UserRegistrationSerializer(serializers.ModelSerializer):
    client_password = serializers.CharField(max_length=150,required=True)
    class Meta:
        model = Client_data
        fields = ['email', 'client_password', 'username','role_id']
        extra_kwargs = {
            'client_password' : {'write_only':True}
        }
    
    def create(self, validated_data):
        return Client_data.objects.create_user(**validated_data)

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255)
    
    def validate(self, data):
        try:
           verify_check = Client_data.objects.get(email = data.get('email'))
           org_obj = Organization_data.objects.get(organization_id = verify_check.organization_id)
           if (org_obj.is_active == False):
               raise serializers.ValidationError("organization_is_disabled")
           
           if(verify_check.first_config == 0):
                raise serializers.ValidationError("email_not_verify")

           if(verify_check.is_active == False):
                raise serializers.ValidationError("account_deactive")

           else:
                return data
        except Client_data.DoesNotExist:
            return data
        
    class Meta:
        model = Client_data
        fields = ['email', 'password']
       

class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255)
    role = serializers.CharField(source='role_id.role',read_only = True)
    ability = serializers.JSONField(source='role_id.ability',read_only = True)
    activated_plan_id = serializers.CharField(source='location_id.activated_plan_id.id',read_only = True)
   
    class Meta:
        model = Client_data
        fields = ['id' ,'email','first_name','profile_photo', 'username','role','ability','allow_MFA','organization_id','location_id', 'activated_plan_id']

# to change password
class ChangeCleintPasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    # new_password = serializers.CharField(required=True, validators = [password_validate_function])
    # confirm_password = serializers.CharField(required=True, validators = [password_validate_function])    
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)    
    u_id = serializers.CharField(required=True)    
    def validate(self, data):
            if data.get('new_password') != data.get('confirm_password'):
                raise serializers.ValidationError("pass_not_match")
            try:
                obj_user = Client_data.objects.get(id = data.get('u_id'))
                if obj_user.client_password == data.get('old_password'):
                    if obj_user.client_password != data.get('confirm_password'):
                        obj_user.password = make_password(data.get('new_password'))
                        obj_user.first_config = 1
                        obj_user.client_password = ""
                        obj_user.save()
                    else:
                        raise serializers.ValidationError("old_new_not_diff")
                else:
                    raise serializers.ValidationError("invalid_old_pass")               
                
            except Client_data.DoesNotExist:
                raise serializers.ValidationError("client_not_exist")
            return data
    class Meta:        
        model = Client_data
        fields = ('old_password', 'new_password', 'confirm_password','u_id')

class LogsSerializer(serializers.ModelSerializer):
    # date_time =  serializers.DateTimeField(format=("%Y-%m-%d %H:%M:%S"))
    class Meta:
        model= ApiLogs
        fields = '__all__'


class Api_LogsSerializer(serializers.ModelSerializer):# has fields different than dashboard
    client_name = serializers.CharField(source='client_id.username',read_only = True)
    class Meta:
        model = ApiLogs
        fields = ['id','client_name','type','date_time','ip','browser_type','req_method','description']

class MAFSerializer(serializers.ModelSerializer):
    allow_MFA = serializers.IntegerField(required=True)
     
    class Meta:
            model = Client_data
            fields = ["id","email","allow_MFA"]
            read_only_fields = ['id','email']

class MAFUpdate(serializers.ModelSerializer):
    otp_mail = serializers.CharField(required=True)
    MFA_token = serializers.CharField(required=True)
     
    class Meta:
            model = Client_data
            fields = ["id","email","otp_mail","MFA_token"]
            read_only_fields = ['id','email']

class ForgotPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255,required=True)

    def validate(self, data):
        try:
            objClient = Client_data.objects.get(email = data.get('email'))
            objClient.otp_mail = self.context.get("mail_otp")
            objClient.save()
            dataClient = dict({'username': objClient.first_name+" "+objClient.last_name,'email':objClient.email})
            return dataClient
        except Client_data.DoesNotExist:
            raise serializers.ValidationError({"email":"email_not_exist"})

    class Meta:
            model = Client_data
            fields = ["id","email","username"]
            read_only_fields = ['id','username','email']

class ForgotPasswordChangeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255,required=True)
    mail_otp = serializers.CharField(required=True)
    # new_password = serializers.CharField(required=True, validators = [password_validate_function])
    # confirm_password = serializers.CharField(required=True, validators = [password_validate_function])
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        if data.get('new_password') != data.get('confirm_password'):
            raise serializers.ValidationError({"msg":"pass_not_match"})
        try:
            objClient = Client_data.objects.get(email = data.get('email'), otp_mail = data.get("mail_otp"))
            mail_otp_vorwrite = data.get("mail_otp")
            objClient.otp_mail = f"{mail_otp_vorwrite}-expired"
            objClient.password = make_password(data.get('new_password'))
            objClient.save()
            return data
        except Client_data.DoesNotExist:
            raise serializers.ValidationError({"msg":"otp_invalide"})


    class Meta:
            model = Client_data
            fields = ["email","mail_otp","new_password","confirm_password"]
            read_only_fields = ['email']

class ResendMafSerializer(serializers.ModelSerializer):
    MFA_token = serializers.CharField(required=True)

    def validate(self, data):
        try:
            objClient = Client_data.objects.get(MFA_token = str(data.get('MFA_token')))
            objClient.otp_mail = self.context.get("mail_otp")
            objClient.save()
            return data
        except Client_data.DoesNotExist:
            raise serializers.ValidationError({"email":"email_not_exist"})
            
    class Meta:
            model = Client_data
            fields = ["id","MFA_token"]


#--------------serializers for country table------------------
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model= Country_data
        fields = '__all__'

#To users config detailts xdr
class UserRegistrationBySelfSerializers(serializers.ModelSerializer):
    class Meta:
            model = Client_data
            fields = ['id','email','username','first_name','last_name','country','role_id','contact_number','parent_client_id','organization_id','client_password','location_id']
            
    def validate(self, data):
        fn = data.get('first_name')
        ln = data.get('last_name')
        if fn.isalpha() and ln.isalpha():
            return data 
        else:
            raise serializers.ValidationError("special_char_not_allowed_in_name")

class UserDataSelfSerializers(serializers.ModelSerializer):
    country = serializers.CharField(source='country.country_name',read_only = True)
    class Meta:
            model = Client_data
            fields = ['id','email','first_name','last_name','country','first_config','profile_photo','role_id_id','contact_number','address_1','address_2','gender','city','state','zipcode','is_active']
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        profile_photo = str(instance.profile_photo)
        local_storage = FileSystemStorage()
        base_url = self.context.get('base_url')
        if not local_storage.exists(profile_photo):
            session = boto3.Session(aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
            s3 = session.resource('s3')
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            try:
                s3.Bucket(bucket_name).download_file('userimages/'+profile_photo, profile_photo)
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == "404":
                    error = {"err":"The object does not exist on s3 bucket"}
                    raise serializers.ValidationError(error)
        if profile_photo == "":
            ret['profile_photo'] = None
        else:
            ret['profile_photo'] = base_url+'api/'+profile_photo
        return ret

class AccountManageSerializers(serializers.ModelSerializer):
    country = serializers.CharField(source='country.country_name',read_only = True)
    branchcode = serializers.CharField(source='location_id.branchcode',read_only = True)
 
    class Meta:
            model = Client_data
            fields = ['id','email','username','first_name','last_name','allow_MFA','country','contact_number','address_1','address_2','gender','profile_photo','city','state','zipcode','branchcode']


class GenIngoSerializer(serializers.ModelSerializer):
    class Meta:
            model = Client_data
            fields = ['first_name','last_name','username','profile_photo']


#To update information
class GeneralSerializer(serializers.ModelSerializer):
    class Meta:
            model = Client_data
            fields = ['address_1','address_2','state','city','zipcode']

class Api_LogsSerializer(serializers.ModelSerializer):# has fields different than dashboard
   
    username = serializers.CharField(source='client_id.first_name',read_only = True)
    email = serializers.CharField(source='client_id.email',read_only = True)
    class Meta:
        model = ApiLogs
        fields = ['id','username','type','date_time','ip','browser_type','req_method','description','email','org_id']

class Third_party_api_serializer(serializers.ModelSerializer):
 
    #appication_type = serializers.CharField(required=True)
 
    # appication_type = serializers.CharField(required=True)
 
    api_type = serializers.CharField(required=True)
    class Meta:
        model = Api_export
        fields = ['api_type','client_id','api_key','api_key_status','application_id', 'api_name']
    
class Api_Export_Third_Party_serializer(serializers.ModelSerializer):
    application_name = serializers.CharField(source='application_id.application_name',read_only = True)
    class Meta:
        model = Api_export
        fields = ['id','api_type','client_id','api_key','api_key_status','application_name','created_at','updated_at', 'api_name']

class Third_party_status_serializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    api_key_status = serializers.BooleanField(required=True)
    class Meta:        
            model = Api_export
            fields = ['id','api_key_status']

#To get serializers apilogs of users updated
class ApiLogs_serializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='client_id.first_name',read_only = True)
    last_name = serializers.CharField(source='client_id.last_name',read_only = True)
    email = serializers.CharField(source='client_id.email',read_only = True)
    class Meta:        
            model = ApiLogs
            fields = ['type','date_time','ip','browser_type','req_method','description','first_name','last_name','email']

#To get config serializers
class Config_Serializer(serializers.ModelSerializer):

    class Meta:        
            model = Init_Configs
            fields = '__all__'

#To get email config serializers
class Email_Config_Serializer(serializers.ModelSerializer):
    class Meta:        
            model = Init_Configs
            fields = ['id','email_ids','platform_val','time_interval_val','time_interval_name','severity_val','config_type','is_active', 'sensor_alert_client', 'sensor_alert_admin', 'ransomware_noti_epoch_val', 'ransomware_noti_is_active']

#To create dashboard config init_config
class Platform_Severity_Serializer(serializers.ModelSerializer):
    class Meta:        
            model = Init_Configs
            fields = ['config_type','platform_val','severity_val','accuracy_val','org_id','trace_sensor']            

#To get notification config serializers
class Notification_Config_Serializer(serializers.ModelSerializer):
    class Meta:        
            model = Init_Configs
            fields = ['config_type','severity_val','platform_val','org_id', "time_interval_val"]              

#To create serializers for activate and deactivate
class ActivateDeactivate_Serializer(serializers.ModelSerializer):   
    class Meta:
        model = Client_data
        fields = ['id','is_active']

class Application_views_serializer(serializers.ModelSerializer):
    application_steps = serializers.SerializerMethodField()
    
    class Meta:
        model= Applications
        fields = ['id','application_name','application_descriptions','created_at', 'application_steps','integration_status']
    
    def get_application_steps(self, obj):
        steps = obj.application_steps
        steps_str = json.dumps(steps)
        application_steps = json.loads(steps_str)
        return application_steps

# serialiser for application-shop page
class Application_shop_serializer(serializers.ModelSerializer):
    application_steps = serializers.SerializerMethodField()
    application_image = serializers.SerializerMethodField()
    
    class Meta:
        model= Applications
        fields = ['id','application_name','application_descriptions','created_at', 'application_steps','integration_status', 'application_image']
    
    def get_application_steps(self, obj):
        steps = obj.application_steps
        steps_str = json.dumps(steps)
        application_steps = json.loads(steps_str)
        return application_steps
    
    def get_application_image(self, obj):
        image = obj.application_image
        image_name = str(image)
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
            updated_image = base_url+'api/static/image/'+str(image)
        return updated_image 

#To get email id from client data
class Clent_Email_Serializer(serializers.ModelSerializer):
    class Meta:
            model = Client_data
            fields = ['id','email']

#To get lang_type from client data
class Client_Language_Serializer(serializers.ModelSerializer):
    class Meta:
            model = Client_data
            fields = ['lang_type']

# To display page permissions
class PagePermissionsSerializer(serializers.ModelSerializer):
    class Meta:        
            model = Page_Permissions
            fields = ['id','env_trace','org_id', 'location_id', 'env_wazuh', 'env_hids', 'env_nids', 'default_page','xdr_live_map','env_hc','env_mm','env_tptf','env_sbs','env_ess','env_tps','env_soar']  

# To display blacklisted details
class GetBlacklistedDetailsSerializer(serializers.ModelSerializer):
    class Meta:        
            model = blacklisted_data
            fields = '__all__'

# To add blacklisted data
class AddBlacklistedDetailsSerializer(serializers.ModelSerializer):
    class Meta:        
            model = blacklisted_data
            fields = ['blacklisted_class', 'blacklisted_ip', 'org_id', 'location_id', 'user_id', 'updated_plan_id', 'created_at', 'updated_at']


#To create dashboard config init_config
class DahboardConfigSerializer(serializers.ModelSerializer):
    class Meta:        
            model = Init_Configs
            fields = ['config_type','platform_val','severity_val','accuracy_val','location_id'] 

# To get env type in  page permissions
class AgentPermissionsSerializer(serializers.ModelSerializer):
    class Meta:        
            model = Page_Permissions
            fields = ['id','org_id','location_id','env_hids','default_page']  


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




# updated serializers to create api key
class create_api_serializer(serializers.ModelSerializer):
    class Meta:
        model = Updated_Api_export
        fields = ['api_type','client_id','api_key','api_key_status','product_name','product_logs_name']

class all_create_api_serializer(serializers.ModelSerializer):
    class Meta:
        model = Updated_Api_export
        fields = '__all__'

class network_map_serializer(serializers.ModelSerializer):
    class Meta:
        model = Agent_data
        fields = ['attach_agent_network']   

class allfileds_create_api_serializer(serializers.ModelSerializer):
    class Meta:
        model = Updated_Api_export
        fields = '__all__'       


class SoarLicenseUrlsPlanStepThreeSerializer(serializers.ModelSerializer):
     class Meta:
          model = Soar_License_Management
          fields = ['soar_sensor_host_url']  


# Used hids for report config serialiers
class RpoertAlldataAgentPermissionsSerializer(serializers.ModelSerializer):
    class Meta:        
            model = Agent_data
            fields = ['hids_alert_agent','hids_incident_agent']

# Used nids for report config serialiers
class ReportNidsAlldataAgentPermissionsSerializer(serializers.ModelSerializer):
    class Meta:        
            model = Agent_data
            fields = ['nids_alert_agent','nids_incident_agent']

# Used trace for report config serialiers
class ReportTraceAlldataAgentPermissionsSerializer(serializers.ModelSerializer):
    class Meta:        
            model = Agent_data
            fields = ['trace_alert_agent','trace_incident_agent']  

# mail: -
class PdfMailDetailsSerializer(serializers.ModelSerializer):
     class Meta:
          model = ReportSchedulerClientDetails
          fields = '__all__'        
class SaveDateSerializer(serializers.ModelSerializer):
     class Meta:
          model = ReportSchedulerTimeFormat
          fields = ['format_name']                      


class AllDetailsSaveDateSerializer(serializers.ModelSerializer):
     class Meta:
          model = ReportSchedulerTimeFormat
          fields = '__all__'                    
