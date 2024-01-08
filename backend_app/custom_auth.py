#  ==================================================================================================
#  File Name: custome_auth.py
#  Description: This file contains custom authentication classes.
#  ---------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Master Dashboard
#  Author URL: https://whizhack.in

#  ====================================================================================================

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from .models import User,Organization_data,Client_data,Applications

class OrgAccountIsStatus(BaseAuthentication):
    def authenticate(self, request):
        password = str(request.data.get('password'))
        email_id = str(request.data.get('email'))#email of Master user jiske through disable ho rhi h organization disable
        org_id = str(request.data.get('org_id'))
        is_active_account = bool(request.data.get('is_active'))
       
        if org_id is None:
            raise ValidationError({"message_type":"key_empty","message":"org_id params is missing"})

        if password is None:
            raise ValidationError({"message_type":"key_empty","message":"password params is missing"})

        if email_id is None:
            raise ValidationError({"message_type":"key_empty","message":"email params is missing"})

        if is_active_account is None:
            raise ValidationError({"message_type":"key_empty","message":"is_active params is missing"})                          
       
        try:
            user_obj = User.objects.get(email=email_id)
            if check_password(password,user_obj.password):#verifying the entered password with master user password
                try:
                    updated_org_obj = Organization_data.objects.filter(organization_id = org_id).update(is_active = is_active_account)
                except User.DoesNotExist:
                    raise ValidationError({"message_type":"invalid_active_user","message":"invalid active User"})
            else:
                raise ValidationError({"message_type":"password_incorrect","message":"password is incorrect"})

        except User.DoesNotExist:
            raise ValidationError({"message_type":"invalid_user","message":"invalid User"})
        return (updated_org_obj,None)

class UserAccountIsStatus(BaseAuthentication):
    def authenticate(self, request):
        password = str(request.data.get('password'))
        email_id = str(request.data.get('email'))#Master email jiske through disable karna h
        user_id = str(request.data.get('user_id'))#user_id jisko disable karna h
        is_active_account = bool(request.data.get('is_active'))
       
        if user_id is None:
            raise ValidationError({"message_type":"key_empty","message":"user_id params is missing"})

        if password is None:
            raise ValidationError({"message_type":"key_empty","message":"password params is missing"})

        if email_id is None:
            raise ValidationError({"message_type":"key_empty","message":"email params is missing"})

        if is_active_account is None:
            raise ValidationError({"message_type":"key_empty","message":"is_active params is missing"})                          
       
        try:
            user_obj = User.objects.get(email=email_id)
            if check_password(password,user_obj.password):
                try:
                    updated_obj = Client_data.objects.filter(id = user_id).update(is_active = is_active_account)
                except User.DoesNotExist:
                    raise ValidationError({"message_type":"invalid_active_user","message":"invalid active User"})
            else:
                raise ValidationError({"message_type":"password_incorrect","message":"password is incorrect"})

        except User.DoesNotExist:
            raise ValidationError({"message_type":"invalid_user","message":"invalid User"})
        return (updated_obj,None)

# enable application status
class ApplicationIsStatus(BaseAuthentication):
    def authenticate(self, request):
        password = str(request.data.get('password'))
        email_id = str(request.data.get('email'))#Master email jiske through enable karna h application
        application_id = str(request.data.get('id'))#user_id jiske through enable karna h
        is_active_account = bool(request.data.get('is_active'))
       
        if application_id is None:
            raise ValidationError({"message_type":"key_empty","message":"user_id params is missing"})

        if password is None:
            raise ValidationError({"message_type":"key_empty","message":"password params is missing"})

        if email_id is None:
            raise ValidationError({"message_type":"key_empty","message":"email params is missing"})

        if is_active_account is None:
            raise ValidationError({"message_type":"key_empty","message":"is_active params is missing"})                          
       
        try:
            user_obj = User.objects.get(email=email_id)
            if check_password(password,user_obj.password):
                try:
                    updated_obj = Applications.objects.filter(id = application_id).update(integration_status = is_active_account)
                except Applications.DoesNotExist:
                    raise ValidationError({"message_type":"invalid_application_id","message":"invalid application"})
            else:
                raise ValidationError({"message_type":"password_incorrect","message":"password is incorrect"})

        except User.DoesNotExist:
            raise ValidationError({"message_type":"invalid_user","message":"invalid User"})
        return (updated_obj,None)