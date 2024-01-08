#  ===============================================================================================================================================================
#  File Name: account_manage_view.py
#  Description: Includes all the views related to user account like: enable/disable MFA for user, disable user account, update genral information of user etc.

#  ---------------------------------------------------------------------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  ===============================================================================================================================================================

from rest_framework.decorators import api_view,permission_classes,parser_classes
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .custome_auth import customeAuth, UserAccountIsStatus
from rest_framework_simplejwt.tokens import RefreshToken
import uuid,random
from .mail_to import send_email_from_app
from django.utils.crypto import get_random_string
from .helpers import api_logs_make
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .custome_auth import UserAccountIsStatus
from .url_for_new_user import BaseUrl

# To enable/disable MFA for user
class AccountSettingMFA(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,*args, **kwargs):
        modelObj = Client_data.objects.get(email = str(request.user), location_id = request.user.location_id)
        modelObj.allow_MFA = request.data.get('allow_MFA')
        if modelObj.allow_MFA == 0:
            status_var = "Deactivated"
        elif modelObj.allow_MFA == 1:
            status_var = "Activated"
        objSeri = MAFSerializer(modelObj,data=request.data)
        res = {}
        if objSeri.is_valid():
            modelObj.save()
            api_logs_make(request,"MFA",f"MFA Setting {status_var}")
            res = {
                "message_type":"allow_mfa_update",
                "data":objSeri.data.get("allow_MFA"),
            }
        else:
            res = {
            "message_type":"s_is_w",
            "errors":objSeri.errors
           }

        return Response(res)

#auto generate token for user #START
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
#auto generate token for user #END

class MFA_veriryOtp(APIView):    
    authentication_classes = [customeAuth]
    def post(self,request,format=None):
        res = {"message_type":"s_is_w"}
        if request.user is not None:
            userDataProfile = UserProfileSerializer(request.user)        
            res =  {
                    "message_type":"login_success",
                    "message":"Login Successfully.",
                    "bk_data":userDataProfile.data,
                    "token": get_tokens_for_user(request.user)
                    }
            return Response(res)
        else:
            return Response(res)

class ForgotPassword(APIView):
    def post(self,request):
        if request.data.get("action") == "RESET_PASS":
            serializer = ForgotPasswordChangeSerializer(data=request.data)
            if serializer.is_valid():
                res = {"message_type":"success"}
                return Response(res, status=status.HTTP_200_OK)
            else:
                res = {"message_type":"form_error","errors":serializer.errors}
                return Response(res, status=status.HTTP_400_BAD_REQUEST)
        else:
            otp = {"mail_otp": random.randrange(100000, 1000000, 6)}
            ip = request.META.get('HTTP_X_FORWARDED_FOR')
            if ip:
                ip = ip.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')

            serializer = ForgotPasswordSerializer(data=request.data,context = otp)
            if serializer.is_valid():
                template_context = {
                            "ip" : ip,
                            "otp": otp.get("mail_otp"),
                            "name" :serializer.data.get("username")
                        }
                send = send_email_from_app(str(serializer.data.get("email")),"Forgot Password",template_context,"frontend/two_step_verification.html")
                if send:
                    res = {"message_type":"otp_send_on_mail"}
                else:
                    res = {"message_type":"s_is_w","message":"mail sending error"}
                return Response(res)
            else:
                res = {"message_type":"form_error","errors":serializer.errors}
                return Response(res)

class Resend_otp(APIView):
    def post(self,request):
        otp = {"mail_otp": random.randrange(100000, 1000000, 6)}
        ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip:
            ip = ip.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        if request.data.get("action") == "MAF_RESEND":
            serializer = ResendMafSerializer(data=request.data,context = otp)
            if serializer.is_valid():
                objClient = Client_data.objects.get(MFA_token = str(serializer.data.get('MFA_token')))
                template_context = {
                            "ip" : ip,
                            "otp": otp.get("mail_otp"),
                            "name" :objClient.first_name+" "+objClient.last_name
                        }
                send = send_email_from_app(objClient.email,"MFA OTP",template_context,"frontend/two_step_verification.html")
                if send:
                    res = {"message_type":"otp_resend_on_mail"}
                else:
                    res = {"message_type":"s_is_w","message":"mail sending error"}
                return Response(res)
            else:
                res = {"message_type":"form_error","errors":serializer.errors}
                return Response(res)
        if request.data.get("action") == "FORGOT_RESEND":
            serializer = ForgotPasswordSerializer(data=request.data,context = otp)
            if serializer.is_valid():
                template_context = {
                            "ip" : ip,
                            "otp": otp.get("mail_otp"),
                            "name" :serializer.data.get("username")
                        }
                send = send_email_from_app(str(serializer.data.get("email")),"Forgot Password",template_context,"frontend/two_step_verification.html")
                if send:
                    res = {"message_type":"otp_send_on_mail"}
                else:
                    res = {"message_type":"s_is_w","message":"mail sending error"}
                return Response(res)
            else:
                res = {"message_type":"form_error","errors":serializer.errors}
                return Response(res)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def UserRegistateView(request): 
        loc_id = request.user.location_id    
        request.data._mutable = True
        generate_pass = str(get_random_string(length=10))
        contextData = {
            'parent_client_id' : request.user.id,
            'organization_id' : request.user.organization_id,
            'client_password' : generate_pass,
            'username' :  str(request.data.get("first_name")) + " " + str(request.data.get("last_name")),
            'location_id' : loc_id.id

        }
        request.data.update(contextData)
        serializer = UserRegistrationBySelfSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            link = BaseUrl+"/generate-new-password/"+str(serializer.data.get("id"))

            template_context = dict({
                                "link":link,
                                "temp_pass" :generate_pass,
                                "name" :str(serializer.data.get("username")),
                                "email" :str(serializer.data.get("email"))
                                })

            send = send_email_from_app(str(serializer.data.get("email")),"XDR Registration",template_context,"frontend/welcome_password.html")
            if send:
                res = {"message_type":"sub_client_created"}
            else:
                res = {"message_type":"s_is_w","message":"mail sending error"}
            return Response(res)
        else:
            res = serializer.errors
            if res.get("email") != None:
                if(res.get("email")[0] == "client_data with this email already exists."):
                    res = dict({"email":"already_exists"})

            return Response({"message_type":"form_error","errors":res}, status=status.HTTP_400_BAD_REQUEST)

class SubClientView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request,format=None):
        clientObj = Client_data.objects.filter(organization_id = str(request.user.organization_id)).exclude(id__exact = request.user.id)
        base_url =  "{0}://{1}/".format(request.scheme, request.get_host())
        serializers = UserDataSelfSerializers(clientObj,many=True, context = {"base_url":base_url})
        
        return Response(serializers.data)

    def get(self,request,format=None):
        base_url =  "{0}://{1}/".format(request.scheme, request.get_host())
        clientObj = Client_data.objects.get(id = str(request.GET.get("id")))
        serializers = UserDataSelfSerializers(clientObj, context = {"base_url":base_url})
        return Response(serializers.data)
        
class AccountManageView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        clientObj = Client_data.objects.get(id = str(request.user.id))
        loc_id = clientObj.location_id # location_id from getting client data models
        plan_id = loc_id.activated_plan_id.id
        location_query = Attach_Location.objects.get(id=loc_id.id, activated_plan_id = plan_id)
        if isinstance(location_query.org_id, Organization_data):
                org_name = location_query.org_id.organization_name                
        else:
            raise("org_id is not a valid instance of Organization_data")

        base_url =  "{0}://{1}/".format(request.scheme, request.get_host())        
        
        photo_name = clientObj.profile_photo
        photo_name = str(photo_name)
        local_storage = FileSystemStorage()
        if not local_storage.exists(photo_name):
            session = boto3.Session(aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
            s3 = session.resource('s3')
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            try:
                s3.Bucket(bucket_name).download_file('userimages/'+photo_name, photo_name)
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == "404":
                    return Response({"err":"The object does not exist on s3 bucket."})
        full_profile_path = base_url+'api/'+photo_name       
        serializers = AccountManageSerializers(clientObj)
        new_serializer = {"profile_photo_path":full_profile_path, "organization_name":org_name}
        new_serializer.update(serializers.data)
        return Response(new_serializer)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def Update_Genral_Information(request):
    clientObj = Client_data.objects.get(email = request.user, location_id = request.user.location_id)    
    serializer = GenIngoSerializer(clientObj, data=request.data, partial=True)
    json_res = {}
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    client_s3 = boto3.client('s3',aws_access_key_id = settings.AWS_ACCESS_KEY_ID,aws_secret_access_key= settings.AWS_SECRET_ACCESS_KEY)
    base_url = "{0}://{1}/".format(request.scheme, request.get_host())+'api'
    if serializer.is_valid():
        serializer.save()  
        api_logs_make(request,"client_update","profile section updated")    
        photo = serializer.data.get('profile_photo')
        full_profile_path = None
        if photo is not None:
            photo_name = str(photo)
            bucket_key = 'userimages'+photo_name#location in s3 bucket where i want to upload image
            file_location = str(photo).replace('/static/', 'static/')#location of image on my local directory
            client_s3.upload_file(file_location, bucket_name, bucket_key, ExtraArgs={'ContentType': 'image/jpeg'})# upload image to s3 bucket
            full_profile_path = base_url+str(photo)

        new_serializer = {'profile_photo_path':full_profile_path}
        new_serializer.update(serializer.data)
        json_res = {"message_type":"updated","data":new_serializer}
    else:
        json_res = { "message_type":"form_errors","errors":serializer.errors }
    
    return Response(json_res, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def UpdateInformation(request):
    clientObj = Client_data.objects.get(email = request.user, location_id = request.user.location_id.id)          
    serializer = GeneralSerializer(clientObj, data=request.data)
    if serializer.is_valid():
        serializer.save()
        api_logs_make(request,"information_update","client information section updated")
        return Response({"message_type":"updated"}, status=status.HTTP_200_OK)
    else:
        return Response({"message_type":"form_errors","errors":serializer.errors}, status=status.HTTP_200_OK)

class DisableUserAccount(APIView):
    authentication_classes = [UserAccountIsStatus]
    def post(self, request):
        user_id = str(request.data.get('user_id'))
        is_active_status = bool(request.data.get('is_active'))
        email_id = str(request.data.get('email'))          
        res = {"message_type":"s_is_w"}
        if request.user == 1:          
            obj_user = Client_data.objects.get(id = user_id)
            request.user = obj_user

            template_context = {
                "user_email":obj_user.email,
                "name" :obj_user.first_name+" "+obj_user.last_name
                             }
            if is_active_status:
                template_context.update({"is_status" :"Your account has been Activated from XDR Portal"})
                api_logs_make(request, "account_activate", f"this user {obj_user.email} account has been activated by this id: {email_id}")
            else:
                template_context.update({"is_status" :"Your account has been Deactivated from XDR Portal"})
                api_logs_make(request, "account_deactivate", f"this user {obj_user.email} account has been deactivated by this id: {email_id}")
            
            send_email_from_app(obj_user.email,"User Account Status",template_context,"frontend/user_login_enable_disable.html")
            res =  {
                    "message_type":"success",
                    "message":"is_active updated successfully",
                    "is_status": is_active_status
                }
        return Response(res)
