#  =======================================================================================================================================================================================
#  File Name: account_manage_view.py
#  Description: Includes all the views related to user account like: enable/disable organization account, enable/disable user account, activate/deactivate application status etc.

#  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Master Dashboard
#  Author URL: https://whizhack.in

#  =======================================================================================================================================================================================

from rest_framework.views import APIView
from .custom_auth import OrgAccountIsStatus, UserAccountIsStatus, ApplicationIsStatus
from .views import api_logs_make
from .models import User, Organization_data, Client_data, Applications
from rest_framework.response import Response
from .mail_to import send_email_from_app

class DisableOrgAccount(APIView):
    authentication_classes = [OrgAccountIsStatus]
    def post(self, request):
        org_id = str(request.data.get('org_id'))
        is_active_status = bool(request.data.get('is_active'))
        email_id = str(request.data.get('email'))       
        res = {"message_type":"s_is_w"}
        if request.user == 1:
            master_user_obj = User.objects.get(email = email_id)
            obj_org = Organization_data.objects.get(organization_id = org_id)
            request.user = master_user_obj
            
            if is_active_status:
                api_logs_make(request, "Org_account_activate", f"this org {obj_org.organization_name} acccount has been activated by this id: {master_user_obj}")
            else:
                api_logs_make(request, "Org_account_deactivate", f"this org {obj_org.organization_name} acccount has been deactivated by this id: {master_user_obj}")
            
            res =  {
                    "message_type":"success",
                    "message":"is_active updated successfully",
                    "is_status": is_active_status
                }
        return Response(res)

class DisableUserAccount(APIView):
    authentication_classes = [UserAccountIsStatus]
    def post(self, request):
        user_id = str(request.data.get('user_id'))
        is_active_status = bool(request.data.get('is_active'))
        email_id = str(request.data.get("email"))            
        res = {"message_type":"s_is_w"}
        if request.user == 1:            
            master_user_obj = User.objects.get(email = email_id)
            client_user_obj = Client_data.objects.get(id=user_id)
            request.user = master_user_obj
            
            template_context = {
                "user_email":client_user_obj.email,
                "name" :client_user_obj.first_name+" "+client_user_obj.last_name
                             }
            
            if is_active_status:
                template_context.update({"is_status" :"Your account has been Activated from XDR Portal"})
                api_logs_make(request, "account_activate", f"this user {client_user_obj.email} acccount has been activated by this id: {master_user_obj}")
            else:
                template_context.update({"is_status" :"Your account has been Deactivated from XDR Portal"})
                api_logs_make(request, "account_deactivate", f"this user {client_user_obj.email} acccount has been deactivated by this id: {master_user_obj}")
            
            send_email_from_app(client_user_obj.email,"User Account Status",template_context,"backend_app/user_login_enable_disable.html")
            res =  {
                    "message_type":"success",
                    "message":"is_active updated successfully",
                    "is_status": is_active_status
                }
        return Response(res)

class ApplicationStatus(APIView):
    authentication_classes = [ApplicationIsStatus]
    def post(self, request):
        application_id = str(request.data.get('id'))
        is_active_status = bool(request.data.get('is_active'))
        email_id = str(request.data.get('email'))       
        res = {"message_type":"s_is_w"}
        if request.user == 1:
            master_user_obj = User.objects.get(email = email_id)
            obj_application = Applications.objects.get(id = application_id)
            request.user = master_user_obj
            
            if is_active_status:
                api_logs_make(request, "application_activate", f"this application {obj_application.application_name} has been activated by this id: {master_user_obj}")
            else:
                api_logs_make(request, "application_deactivate", f"this application {obj_application.application_name} has been deactivated by this id: {master_user_obj}")
            
            res =  {
                    "message_type":"success",
                    "message":"is_active updated successfully",
                    "is_status": is_active_status
                }
        return Response(res)


