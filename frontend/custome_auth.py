#  ==================================================================================================
#  File Name: custome_auth.py
#  Description: This file contains custom authentication classes.
#  ---------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  ====================================================================================================

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed,ValidationError
from django.contrib.auth.hashers import check_password
from .models import Client_data,Api_export, Organization_data,Updated_Api_export

class customeAuth(BaseAuthentication):
    def authenticate(self,request):

        v_token = request.data.get("v_token")
        mail_otp = request.data.get("mail_otp")
        
        if v_token is None:
            raise ValidationError({"message_type":"form_errors","param":"v_token"})
        
        if mail_otp is None:
            raise ValidationError({"message_type":"form_errors","param":"mail_otp"})            
        
        try:
            UserData = Client_data.objects.get(MFA_token =  v_token , otp_mail = mail_otp, allow_MFA = 1)
            UserData.MFA_token = f"{v_token}-expired"
            UserData.otp_mail = f"{mail_otp}-expired"
            UserData.save()           
        except Client_data.DoesNotExist:
            raise AuthenticationFailed({"message_type":"invalid_otp"})
        
        return (UserData, None)

class ApiWithKeyAuth(BaseAuthentication):
    def  authenticate(self,request):

        api_key_header = request.headers.get('Key')

        if api_key_header is None:
            raise ValidationError({"message_type":"key_empty","headers":"Key"})
        
        try:
            UserData = Api_export.objects.get(api_key = api_key_header)
            try:
                UserData = Api_export.objects.get(api_key_status = True, api_key = api_key_header)
            except Api_export.DoesNotExist:
                raise AuthenticationFailed({"message_type":"key_not_activated"})
        except Api_export.DoesNotExist:
            raise AuthenticationFailed({"message_type":"invalid_key"})
        
        return (UserData, None)

class UserAccountIsStatus(BaseAuthentication):
    def authenticate(self, request):
        password = str(request.data.get("password"))
        email_id = str(request.data.get("email"))
        user_id = str(request.data.get("user_id"))
        is_active_account = bool(request.data.get("is_active"))
       
        if user_id is None:
            raise ValidationError({"message_type":"key_empty","message":"user_id params is missing"})

        if password is None:
            raise ValidationError({"message_type":"key_empty","message":"password params is missing"})

        if email_id is None:
            raise ValidationError({"message_type":"key_empty","message":"email params is missing"})

        if is_active_account is None:
            raise ValidationError({"message_type":"key_empty","message":"is_active params is missing"})                          
       
        try:
            login_user_obj = Client_data.objects.get(email=email_id)#master user object-"jo disable karega"
            to_disable_user_obj = Client_data.objects.get(id = user_id)#user to be disabled
            org_obj = Organization_data.objects.get(organization_id = to_disable_user_obj.organization_id)
            if check_password(password,login_user_obj.password) and (org_obj.is_active == True):#verifying login details of master user
                try:
                    obj_active_user = Client_data.objects.get(id=user_id)
                    updated_obj = Client_data.objects.filter(id = obj_active_user.id, organization_id = org_obj.organization_id).update(is_active = is_active_account)
                except Client_data.DoesNotExist:
                    raise ValidationError({"message_type":"invalid_active_user","message":"invalid active User"})
            else:
                raise ValidationError({"message_type":"password_incorrect or org is disabled","message":"password is incorrect or org is disabled"})

        except (Organization_data.DoesNotExist,Client_data.DoesNotExist):
            raise ValidationError({"message_type":"invalid_user","message":"invalid User"})
        return (updated_obj,None)
    

# 
class UpdatedApiWithKeyAuth(BaseAuthentication):
    def  authenticate(self,request):

        api_key_header = request.headers.get('Key')

        if api_key_header is None:
            raise ValidationError({"message_type":"key_empty","headers":"Key"})
        
        try:
            UserData = Updated_Api_export.objects.get(api_key = api_key_header)
            try:
                UserData =  Updated_Api_export.objects.get(api_key_status = True, api_key = api_key_header)
            except  Updated_Api_export.DoesNotExist:
                raise AuthenticationFailed({"message_type":"key_not_activated"})
        except  Updated_Api_export.DoesNotExist:
            raise AuthenticationFailed({"message_type":"invalid_key"})
        
        return (UserData, None)    