#  =====================================================================================================================================================================================
#  File Name: views.py
#  Description: This file contains most of the code for important functionalities like: user registration, user login, add organiation, display location, add location, display location, add plan, upgrade plan etc.

#  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Master Dashboard
#  Author URL: https://whizhack.in

#  ======================================================================================================================================================================================

from unittest import result
from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.decorators import api_view,permission_classes,parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from .postgresql_script import *
from .products import products
from rest_framework import generics
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import get_template
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from time import gmtime, strftime
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg, Count
from ._connection import *
from django.core.exceptions import ValidationError
import boto3, botocore, json, uuid
from django.core.files.storage import FileSystemStorage
from .mail_to import send_multiple_mail
from .url_for_new_user import BaseUrl
import ast
import time
from datetime import date,datetime,timezone, timedelta
import pytz, dateutil.parser
from django.db.models import F
from django.db import transaction
from django.utils import timezone
from django.contrib.auth.hashers import make_password, PBKDF2PasswordHasher


# to display frontend dashboard
def index(request):
    return render(request, 'build/index.html')


#auto generate token for user #START
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
#auto generate token for user #END

#master user registration #START
class UserRegistrationView(APIView):
    def post(self,request,format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            api_logs_make(request,"Master user registration","client registractions")
            responst_json = {
                "message_type":"register_success",
                "message":"Registration Successfully."
            }
            return Response(responst_json,status.HTTP_200_OK)

        responst_json = {
            "message_type":"form_errors",
            "message":"Required param not pass.",
            "errors":serializer.errors
        }
        return Response(responst_json,status.HTTP_400_BAD_REQUEST)
#master user registration #END

#master user login #START
class UserLoginView(APIView):
    def post(self,request,format=None):
        serializer = UserLoginSerializer(data=request.data)        
        if serializer.is_valid():            
            password = serializer.data.get("password")
            email = serializer.data.get("email")
            userCheck = authenticate(email=email,password=password)
            if userCheck is not None:                
                userDataS = UserProfileSerializer(userCheck)
                request.user = userCheck
                api_logs_make(request,"login","user login in api")
                responst_json = {
                    "message_type":"login_success",
                    "message":"Login Successfully.",
                    "bk_data":userDataS.data,
                    "token": get_tokens_for_user(userCheck)
                }                
                return Response(responst_json,status.HTTP_200_OK)
            else:
                responst_json = {
                    "message_type":"user_not_exist",
                    "message":"User not exist in record."
                }
                return Response(responst_json,status.HTTP_404_NOT_FOUND)
        responst_json = {
            "message_type":"form_errors",
            "message":"Required param not pass.",
            "errors":serializer.errors
        }
        return Response(responst_json,status.HTTP_400_BAD_REQUEST)
#master user login #END

#master user profile #START
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,format=None):
        serializer = UserProfileSerializer(request.user)
        responst_json = {
            "message_type":"profile_data",
            "message":"show profile data",
            "data":serializer.data,
        }
        return Response(responst_json,status.HTTP_200_OK)

#master user profile #END
# #-----------view objective: add new Organization (organization_detail table)
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def Create_data(request):
    if request.method=="POST":
        context_data = {

            'organization_name': request.data["organization_name"].strip(u'\u200b'),
            'organization_primary_email_id': request.data["organization_primary_email_id"].strip(),
            'organization_secondary_email_id' : request.data["organization_secondary_email_id"].strip(),
            'organization_primary_contact_number' : request.data["organization_primary_contact_number"],
            'organization_secondary_contact_number' : request.data["organization_secondary_contact_number"],
            'organization_city' : request.data["organization_city"],
            'organization_state' : request.data["organization_state"],
            'timezone_id' : request.data["timezone_id"],
            'country_id' : request.data["country_id"],
            'organization_pincode' : request.data["organization_pincode"],
            'organization_address' : request.data["organization_address"],
        }

        serializer_variable = EncryptPasswordSerializer(data=context_data)
        if serializer_variable.is_valid():
            serializer_variable.save()
            api_logs_make(request,"organization add","new organization added")
            return Response({"message_type":"successfully_inserted","message":"Successfull inserted data in org"}, status=status.HTTP_200_OK)
        else:
            return Response({"message_type":"unsuccessfully","message":"Data was not inserted","errors":serializer_variable.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class updateOrg(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self,pk):
        try:
            return Organization_data.objects.get(pk=pk)
        except Organization_data.DoesNotExist:
            return Response(Organization_dataSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
    def get(self, request, pk):
        orgobj=self.get_object(pk)
        serialiseobj=Organization_dataSerializer(orgobj)
        return Response(serialiseobj.data)
   
    def put(self, request, pk):
        orgobj=self.get_object(pk)
        serialiseobj=Organization_dataSerializer(orgobj, data=request.data)
        if serialiseobj.is_valid():
            serialiseobj.save()
            
            return Response(serialiseobj.data, pk)
        return Response(serialiseobj.errors, status=status.HTTP_400_BAD_REQUEST)


#delete the data by id        
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def Delete_data(request,pk):
    if request.method=="GET":
        results=Organization_data.objects.get(id=pk)
        results.delete()
        serializer=Organization_dataSerializer(instance=results,data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    return Response("Deleted Successfully",safe=False)


# display all the data in table organization_detail
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def show(request):
    if request.method == 'GET':
        results= Organization_data.objects.all().order_by('onboarding_timestamp')
        serialize = Organization_dataSerializer(results,many=True)
        return Response(serialize.data)

#-----------view objective: display organizations which have status code=0----------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Displayall_org_with_0status(request):
    if request.method=='GET':
        narrowed_query = Organization_data.objects.filter(status_code=0)
        serializer = Organization_withstatusSerializer(narrowed_query,many=True)
        return Response(serializer.data)

#-----------view objective: display organizations which have status code=1----------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Displayall_org_with_1status(request):
    if request.method=='GET':
        narrowed_query = Organization_data.objects.filter(status_code=1)
        serializer = Organization_withstatusSerializer(narrowed_query,many=True)
        return Response(serializer.data)

#-----------view objective: display organizations which have both status code=0,1----------
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def Displayall_org_with_bothstatus(request):
    try:
        org_obj = Organization_data.objects.filter(is_active=False).values('organization_id')#filtering organizations which are disabled
        query = Organization_data.objects.all().exclude(organization_id__in=org_obj).order_by('-onboarding_timestamp')
        serializer = Organization_withstatusSerializer(query,many=True)
        Dict_org_ids = []
        for i, n in enumerate(serializer.data):
            id = n.get('organization_id')
            organization_name = n.get('organization_name')
            Dict_org_ids.append(id)
            location = list(Attach_Location.objects.values('org_id','id','city','branchcode').filter(org_id = id))
            for j,m in enumerate(location):
                branchcode_city = '{}-{}'.format(organization_name, m['branchcode'])
                m['sensor_name'] = branchcode_city
                m['org_name'] = organization_name
                n['location'] = location
        msg = {"message_type":"data_found","data":serializer.data}
    except ObjectDoesNotExist:
        msg = {"message_type":"d_not_f"}
    return Response(msg)

#-----------view objective: display organizations which have both status code=0,1----------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Displayall_org_with_bothstatus2(request, pk):
    try:       
        query = Organization_data.objects.get(organization_id = pk)
        query_client = Client_data.objects.filter(organization_id = pk)
        serializer_org = Organization_withstatusSerializer(query)
        serializer_org_users = Org_User_Serializers(query_client,many = True)
        req = {
            "org_data": serializer_org.data,
            "org_user_data": serializer_org_users.data,
        }
        msg = {"message_type":"data_found","data":req}
    except ObjectDoesNotExist:
        msg = {"message_type":"d_not_f"}
    return Response(msg)


#------------------jaydeeproysarkar test for products dummy dat
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProducts(request):

    return Response(products)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProduct(request, pk):
    for i in product:
        if i['organization_id'] == pk:
            product = i
            break
    return Response(product)

#from api import serializers

class UserListOrg(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Organization_data.objects.all()
    serializer_class = Joinfkey_Serializer
class UserDetailOrg(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Organization_data.objects.all()
    serializer_class = Joinfkey_Serializer
    
#To combine two tables billings and plans models

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Billings_Plans_data(request):

    if request.method=="POST":

        billingsserialize=Billings_Data_Serializer(data=request.data) #first models of serializers

        planserializer=Plans_Data_Serializer(data=request.data)

        if billingsserialize.is_valid() and planserializer.is_valid():

            billingsserialize.save()

            planserializer.save()
            api_logs_make(request,"billing plan data","new billing plan added")

            data = {

                'plan':  planserializer.data,

                'billing': billingsserialize.data

            }

            return Response(data,status=status.HTTP_201_CREATED)

        return Response(billingsserialize.errors,status=status.HTTP_400_BAD_REQUEST)

#To add plan details
@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
@parser_classes([MultiPartParser, FormParser, JSONParser])
def Add_Plans_data_status_updated(request):
    serializer_variable = Plans_Data_Serializer(data=request.data)
    if serializer_variable.is_valid():
        serializer_variable.save()
        api_logs_make(request,"add plan","new plan added")
        return Response({"message_type":"successfully_inserted","message":"Successfull inserted data in org"}, status=status.HTTP_200_OK)
    else:
        return Response({"message_type":"unsuccessfully","message":"Data was not inserted"}, status=status.HTTP_400_BAD_REQUEST) 
    
#To add billing data
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def Add_Billings_data_status_updated(request):
    if request.method=="POST":
        billingsserialize=Billings_Data_Serializer(data=request.data) #first models of serializers
        #planserializer=Plans_Data_Serializer(data=request.data)
        if billingsserialize.is_valid():
            billingsserialize.save()
            api_logs_make(request,"add billing","new billing added")
            return Response({"message_type":"successfully_inserted","message":"Successfull inserted data in org"}, status=status.HTTP_200_OK)
        else:
            return Response({"message_type":"unsuccessfully","message":"Data was not inserted","errors":billingsserialize.errors}, status=status.HTTP_400_BAD_REQUEST)

#Display all the data in table plan

@api_view(['GET'])
def Show_Plan_Data(request):
    if request.method == 'GET':
        results= Plans_data.objects.all()
        serialize = Plans_Data_Serializer(results,many=True)
        return Response(serialize.data)
    
#-------------------To combine two tables billings and plans models-----------
@api_view(['POST'])
def Billings_Plans_data(request):
    if request.method=="POST":
        billingsserialize=Billings_Data_Serializer(data=request.data)
        planserializer=Plans_Data_Serializer(data=request.data)
        if billingsserialize.is_valid() and planserializer.is_valid():
            billingsserialize.save()
            planserializer.save()
            data = {
                'plan':  planserializer.data,
                'billing': billingsserialize.data
            }
            return Response(data,status=status.HTTP_201_CREATED)
        return Response(billingsserialize.errors,status=status.HTTP_400_BAD_REQUEST)


#-------------------To add plan details-----------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Add_Plans_data(request):
    if request.method=="POST":
        #billingsserialize=Billings_Data_Serializer(data=request.data)
        planserializer=Plans_Data_Serializer(data=request.data)
        if planserializer.is_valid():
            planserializer.save()
            api_logs_make(request,"add plans","new plan added")
            return Response(planserializer.data,status=status.HTTP_201_CREATED)
        return Response(planserializer.errors,status=status.HTTP_400_BAD_REQUEST)

#-----------To add billing data-----------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Add_Billings_data(request):
    if request.method=="POST":
        billingsserialize=Billings_Data_Serializer(data=request.data)
        #planserializer=Plans_Data_Serializer(data=request.data)
        if billingsserialize.is_valid():
            billingsserialize.save()
            api_logs_make(request,"add billing","new billing added")
            return Response(billingsserialize.data,status=status.HTTP_201_CREATED)
        return Response(billingsserialize.errors,status=status.HTTP_400_BAD_REQUEST)

#-----------Display all the data in table plan-----------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Show_Plan_Data(request):
    if request.method == 'GET':
        results= Plans_data.objects.all()
        serialize = Plans_Data_Serializer(results,many=True)
        return Response(serialize.data)

#-----------To display the billing details in list with id-----------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def BillingListOrg(request):
    queryset = Billings_data.objects.all()
    if not queryset:
        msg = {"message_type":"d_not_f"}
    else:
        serializer = Billings_Data_Serializer(queryset, many=True)
        msg = {"message_type":"data_found","data":serializer.data}
    return Response(msg)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def BillingDetailOrg(request, pk):
    try:
        query = Billings_data.objects.get(id = pk)
        serializer = Billings_Data_Serializer(query)
        return Response({"message_type": "data_found","data":serializer.data})
    except ObjectDoesNotExist:
        return Response({"message_type":"d_not_f"})

#-----------To display the plan details in list with id-----------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def PlanListOrg(request):
    queryset = Plans_data.objects.all()
    if not queryset:
        msg = {"message_type":"d_not_f"}
    else:
        serializer = Plans_Data_Serializer(queryset, many=True)
        msg = {"message_type":"data_found","data":serializer.data}
    return Response(msg)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def PlanDetailOrg(request, pk):
    try:
        query = Plans_data.objects.get(id = pk)
        serializer = Plans_Data_Serializer(query)
        return Response({"message_type": "data_found","data":serializer.data})
    except ObjectDoesNotExist:
        return Response({"message_type":"d_not_f"})

    
#----------display Country table data---------------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Display_Country_data(request):
    results= Country_data.objects.all()
    if not results:
        msg = {"message_type":"d_not_f"}
    else:
        serializer = CountrySerializer(results,many=True)
        msg = {"message_type":"data_found","data":serializer.data}
    return Response(msg)

#----------display Time_Zone table data---------------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Display_TimeZone_data(request):
    results= Time_Zone_data.objects.all()
    if not results:
        msg = {"message_type":"d_not_f"}
    else:
        serializer = TimeZoneSerializer(results,many=True)
        msg = {"message_type":"data_found","data":serializer.data}
    return Response(msg)


#-----------To display the billing details in list with id date and time based on india-----------
class BillingListOrgTimes(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Billings_data.objects.all()
    serializer_class = Billings_Data_Serializer_Times

class BillingDetailOrgTimes(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Billings_data.objects.all()
    serializer_class = Billings_Data_Serializer_Times

#-----------To display the plan details in list with id date and time based on india-----------
class PlanListOrgTimes(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Plans_data.objects.all()
    serializer_class = Plans_Data_Serializer_Times

class PlanDetailOrgTimes(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Plans_data.objects.all()
    serializer_class = Plans_Data_Serializer_Times

#--------------add agent details with location 
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def store_agent_into_db(request):
    if request.method=="POST":
        serializervariable = AgentSerializer(data=request.data)
        if serializervariable.is_valid():
            serializervariable.save()
            api_logs_make(request,"agent add","new agent added")
            return Response({"message_type":"successfully_inserted","message": "Successfully inserted data in db"}, status=status.HTTP_200_OK)
        else:
            return Response({"message_type":"unsuccessful","message": "Data was not inserted"}, status=status.HTTP_400_BAD_REQUEST)


#--------------store user details in db ( Priya Duggal )----------------------------------------------------

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def store_user_in_db(request):
    generate_pass = ''.join([random.choice( string.ascii_uppercase + string.ascii_lowercase + string.digits) for n in range(10)])
    contextData = {
        'client_password' : generate_pass,
        'username' :  str(request.data.get("first_name")) + " " + str(request.data.get("last_name"))
        }
    request.data.update(contextData)
    serializervariable = UseraddSerializer(data=request.data)
    if serializervariable.is_valid():
        serializervariable.save()
        api_logs_make(request,"user add","new user added")
        # generate link for new user
        link = BaseUrl+"/generate-new-password/"+str(serializervariable.data.get("id"))

        template_context = dict({
                            "link":link,
                            "temp_pass" :generate_pass,
                            "name" :str(serializervariable.data.get("username")),
                            "email" :str(serializervariable.data.get("email"))
                            })

        send = send_multiple_mail([str(serializervariable.data.get("email"))],"XDR Registration",template_context,"backend_app/welcome_password.html")
        if send.get("status") == "ok":
            return Response({"message_type":"successfully_inserted","message": "Successfully inserted data in db"}, status=status.HTTP_200_OK)
        else:
            return Response({"message_type":"s_is_w","message":"mail sending error", "mail_err": send.get("msg")}, status = status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"message_type":"unsuccessful","message": "Data was not inserted","errors":serializervariable.errors}, status=status.HTTP_400_BAD_REQUEST)
        

#--------------store email config in db ( Priya Duggal )----------------------------------------------------
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def store_email_config_indb(request):
    if request.method=="POST":
        serializervariable = emailConfigSerializer(data=request.data)
        if serializervariable.is_valid():
            serializervariable.save()
            api_logs_make(request,"email config","new email added")
            
            return Response({"message_type":"successfully_inserted","message": "Successfully inserted data in db"}, status=status.HTTP_200_OK)
        else:
            return Response({"message_type":"unsuccessful","message": "Data was not inserted"}, status=status.HTTP_400_BAD_REQUEST)

#--------------get all email config( Priya Duggal )----------------------------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def display_email_config(request):
    if request.method=='GET':
        fetch_from_db = email_config_data.objects.all()
        serializer_variable = emailConfigSerializer(fetch_from_db, many=True)
        return Response(serializer_variable.data)

# To get users details with check if organization is active true then will display users details updated code (26-10-23)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_users(request):
    try:
        # Query data directly from the database and select specific fields
        query_location = Client_data.objects.select_related(
            'organization_id',
            'location_id',
        ).filter(organization_id__is_active=True).values(
            'id',
            'is_active',
            'created_at',
            'role_id_id',
            'allow_MFA',
            'first_config',
            'location_id__branchcode',
            'location_id__city',
            'organization_id__organization_name',
            'first_name',
            'last_name',
            'email',
            'username',
            'contact_number',
        ).order_by('-created_at')

        data = list(query_location)  # Convert the queryset to a list of dictionaries

        custom_data = []
        for item in data:
            custom_item = {
                "id": item["id"],
                "organization_name": item["organization_id__organization_name"],
                "first_name": item["first_name"],
                "last_name": item["last_name"],
                "email": item["email"],
                "contact_number": item["contact_number"],
                "username": item["username"],
                "is_active": item["is_active"],
                "created_at": item["created_at"],
                "role_id_id": item["role_id_id"],
                "allow_MFA": item["allow_MFA"],
                "first_config": item["first_config"],
                "location_branchcode": item["location_id__branchcode"],
                "location_city": item["location_id__city"],
            }
            custom_data.append(custom_item)

        return Response(custom_data)
    except Client_data.DoesNotExist:
        return Response({"message_type": "d_not_f"})

#-----------------------------testing-----------------------------

class Retrieve_users(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Client_data.objects.all()
    serializer_class = UserdisplaySerializer

@permission_classes([IsAuthenticated])
def api_logs_make(request,log_type = 0,description = 0):
    userDataS = UserProfileSerializer(request.user)
    ip = request.META.get('HTTP_X_FORWARDED_FOR')
    browser_type = request.META["HTTP_USER_AGENT"]
    req_method = request.method

    if ip:
        ip = ip.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    makeData = {
        "table_name"   :   "backend_app_user",
        "master_id"    :   userDataS.data['id'],
        "type"         :   log_type,
        "ip"           :   ip,
        "browser_type" :   browser_type,
        "req_method"   :   req_method,
        "description"  :   description,
        "date_time"    :   strftime("%Y-%m-%d %H:%M:%S", gmtime())
    }
    convertPostData = request.post = makeData

    valid_data_serializer = LogsSerializer (data = convertPostData)
    valid_data_serializer.is_valid()
    valid_data_serializer.save()   

#---------sending welcome mail with automatic password from db in mail template ( Priya Duggal )--------------
def send_email_api(request, id):
    fetch_organization_query = Client_data.objects.get(user_id=id)
    email_from_db = fetch_organization_query.email
    name = fetch_organization_query.username
    temp_pass = fetch_organization_query.password
    send_mail(email_from_db, name, temp_pass, id)
    data = {
        'success': True,
        'message':'api to send an email'
    }
    return JsonResponse(data)


def send_mail(receivers, name, temp_pass, id):
    html_tpl_path = 'backend_app/welcome_password.html'
    link = BaseUrl+"/generate-new-password/"+id
    context_data = {'email_addr':receivers, 'name': name, 'temp_pass':temp_pass, 'link':link}
    email_html_template = get_template(html_tpl_path).render(context_data)
    receivers_list = list(receivers.split(" "))
    email_msg = EmailMessage(subject = 'Welcome Mail!!!!', body = email_html_template, from_email = settings.EMAIL_HOST_USER, to = receivers_list, reply_to=[settings.EMAIL_HOST_USER],)
    # this is the crucial part that sends email as html content but not as a plain text
    email_msg.content_subtype = 'html'
    email_msg.send(fail_silently=False)

# To create Client api logs
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Displayall_Client_Logs(request):
    _limit = request.GET.get("limit")
    _offset = request.GET.get("offset")
    if _limit is None:
        _limit = 10
    else:
        _limit = int(_limit)

    if _offset is None:
        _offset = 0
    else:
        _offset = int(_offset)
    query = ApiLogs.objects.filter(table_name = "client_data").order_by('-date_time')[_offset:_offset+_limit]
    serializer = Api__Client_LogsSerializer(query, many=True)
    
    if len(serializer.data) > 0:
        return Response({"message_type":"data_found","data":serializer.data})
    else:
        return Response({"message_type":"data_not_found"})


# To create Master logs    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Displayall_Master_Logs(request):
    _limit = request.GET.get("limit")
    _offset = request.GET.get("offset")
    if _limit is None:
        _limit = 100
    else:
        _limit = int(_limit)

    if _offset is None:
        _offset = 0
    else:
        _offset = int(_offset)

    # Apply limit and offset to the queryset
    query = ApiLogs.objects.filter(table_name="backend_app_user").order_by('-date_time')[_offset:_offset + _limit]
    serializer = Api_Master_LogsSerializer(query, many=True)
    if len(serializer.data) > 0:
        return Response({"message_type": "data_found", "data": serializer.data})
    else:
        return Response({"message_type": "data_not_found"})


# To get apllogs users
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Show_ApiLogs(request):
    uid = request.GET.get("uid")
    try:
        results = ApiLogs.objects.filter(client_id = str(uid)).order_by('-date_time')
        serializer = ApiLogs_serializer(results, many=True)
        return Response({"message_type":"data_found","data":serializer.data})
    except ObjectDoesNotExist:
        return Response({"message_type":"d_not_f"}) 

@csrf_exempt
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
@permission_classes([IsAuthenticated])
def Add_Applications(request):
    if request.method=="POST":
        serializervariable = Application_Serializer(data=request.data)
        if serializervariable.is_valid():
            serializervariable.save()
            api_logs_make(request,"application add","new application added")
            return Response({"message_type":"successfully_inserted","message": "Successfully inserted data in db"}, status=status.HTTP_200_OK)
        else:
            return Response({"message_type":"unsuccessful","message": "Data was not inserted"}, status=status.HTTP_400_BAD_REQUEST)               

# To get all agent details with get location_id basis agent details
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_agent_details(request):
    queryset = Agent_data.objects.all()
    location_id = request.GET.get('location_id')
    if location_id and location_id != "null":
        queryset = queryset.filter(org_location=location_id)
    serializer_class = AgentfkeySerializer(queryset, many=True)
    if not serializer_class.data:
        return Response({"message_type": "d_not_f", "message": "Data not found"})
    return Response({"message_type": "success", "data": serializer_class.data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ApplicationListOrg(request):
    queryset = Applications.objects.all()
    base_url =  "{0}://{1}/".format(request.scheme, request.get_host())
    serializer = Application_Views_Serializer(queryset, many=True, context = {"base_url":base_url})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ApplicationDetailOrg(request, pk):
    try:
        query = Applications.objects.get(id = pk)
        base_url =  "{0}://{1}/".format(request.scheme, request.get_host())
        serializer = Application_Views_Serializer(query, context = {"base_url":base_url})
        return Response({"message_type": "success","data":serializer.data})
    except ObjectDoesNotExist:
        return Response({"message_type":"d_not_f"})

class ApiSetData(APIView):
    def post(self, request, format=None):
        index = request.data.get("index")
        alert_data = request.data.get("alert_data")
        if index is None:
            return Response({"msg":"index params is empty.","error":"index"})
        if alert_data is None:
            return Response({"msg":"alert data params is empty.","error":"alert_data"})
        check_db = save_data(alert_data,index)
        return Response(check_db)

# To show users how many users come in particular organization   
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def OrgUserNumber(request):
    org_id = request.GET.get("org_id")
    query = Client_data.objects.filter(organization_id = org_id)
    serializer = OrgUserNumSerializer(query,many=True)
    return Response(serializer.data)  

# To add data in app_details table
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
@permission_classes([IsAuthenticated])
def AddAppDetails(request):
    request.data._mutable=True
    Dict = dict(request.data)
    app_id = request.data.get('id')
    file_check = request.FILES.get('application_image', False)
    img_path = "null"
    if Dict.get('application_steps[]') == None:
        application_steps = []
    else:
        application_steps = json.dumps(Dict.get('application_steps[]'))# converting list data type to string
    context_data = {'application_steps' : application_steps}
    request.data.update(context_data)
    application_obj = Applications.objects.get(id = app_id)
    serializervariable = AppDetailsSerializer(application_obj, data=request.data)
    if serializervariable.is_valid():
        serializervariable.save()
        if file_check != False:
            
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            client_s3 = boto3.client('s3',aws_access_key_id = settings.AWS_ACCESS_KEY_ID,aws_secret_access_key= settings.AWS_SECRET_ACCESS_KEY)
            photo = serializervariable.data.get('application_image')
            photo_name = str(photo).replace('/image/', '/')
            bucket_key = 'applicationimages'+photo_name#location in s3 bucket where i want to upload image
            file_location = 'static/image'+photo_name#location of image on my local directory
            base_url =  "{0}://{1}".format(request.scheme, request.get_host())
            img_path = base_url+str(photo)
            client_s3.upload_file(file_location, bucket_name, bucket_key, ExtraArgs={'ContentType': 'image/jpeg'})
        api_logs_make(request,"application details add","application details added")
        return Response({"message_type": "success", "img_path" : img_path}, status=status.HTTP_200_OK)
    else:
        return Response({"message_type":"errors", "error":f"{serializervariable.errors}"}, status=status.HTTP_400_BAD_REQUEST)                          

# To display page_permissions api
class PagePermissionsView(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        jsonRes = {}
        location_id = str(request.data.get("org_id"))

        if location_id is None and location_id:
            jsonRes = {"message_type":"errors","message":"org_id params is missing."}

        try:
            query_client = Page_Permissions.objects.get(location_id = location_id)
            serializer = AddPagePermissionsSerializer(query_client, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                api_logs_make(request,"env_page_config_update","Update env-trace or env-wazuh.")
                jsonRes = {"message_type":"success","data":serializer.data}

        except ObjectDoesNotExist:
            try:
                Organization_data.objects.get(location_id = location_id)
                serializer = AddPagePermissionsSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    api_logs_make(request,"env_page_config_insert","added new env-trace or env-wazuh")
                    jsonRes = {"message_type":"success","data":serializer.data} 
                else:
                    jsonRes = {"message_type":"errors","message":serializer.errors}
            except ObjectDoesNotExist:
                jsonRes = {"message_type":"errors","message":"Organization ID doesn't exist."}
        return Response(jsonRes)

    def get(self, request):
        org_id = request.GET.get('org_id')
        res_msg = {}
        try:
            query_result = Page_Permissions.objects.get(org_id = org_id)
            obj = PagePermissionsSerializer(query_result)
            res_msg = {"message_type":"success","data":obj.data}
        except ObjectDoesNotExist:
            res_msg = {"message_type":"d_not_f"}
            
        return Response(res_msg)

# To display data from location table   
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def display_location(request):
    try:
        get_org_name_query = Attach_Location.objects.select_related('org_id').values(organization_name=F('org_id__organization_name'), organization_id = F('org_id__organization_id'))

        query_location = get_org_name_query.values('id','branchcode','city','email','phone_number','is_active','created_at', 'organization_name', 'organization_id', 'activated_plan_id').order_by('-created_at')
        
        msg = {"message_type": "data_found", "data": query_location}
    except Attach_Location.DoesNotExist:
        msg = {"message_type": "d_not_f"}
    return Response(msg)
   

# To display location data on basis of specific location_id along with opensearch connection values(db_username, db_password, host,port) from agent_details table  
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pkey_display_location(request, pk, pk2):
    if (pk is None) or (pk == "null"):
        return Response({"message_type":"d_not_f", "message":"location_id_n_found"})
    
    if (pk2 is None) or (pk2 == "null"):
        return Response({"message_type":"d_not_f", "message":"plan_id_n_found"})
    
    try:
        HidsLicenseObj = Hids_License_Management.objects.filter(updated_plan_id = pk2).first()
        NidsLicenseObj = Nids_License_Management.objects.filter(updated_plan_id = pk2).first()
        SoarLicenseObj = Soar_License_Management.objects.filter(updated_plan_id = pk2).first()
        TraceLicenseObj = Trace_License_Management.objects.filter(updated_plan_id = pk2).first()

        base_url =  "{0}://{1}/".format(request.scheme, request.get_host())
        context_dict = {"base_url":base_url}

        dynamic_sensor_key_dict = {}
        
        if HidsLicenseObj is not None:
            hids_sensor_key = HidsLicenseObj.sensor_key
            if (hids_sensor_key is not None) or (hids_sensor_key != "null"):
                dynamic_sensor_key_dict.update({"hids_sensor_key":hids_sensor_key})

        if NidsLicenseObj is not None:
            nids_sensor_key = NidsLicenseObj.sensor_key
            if (nids_sensor_key is not None) or (nids_sensor_key != "null"):
                dynamic_sensor_key_dict.update({"nids_sensor_key":nids_sensor_key})

        if SoarLicenseObj is not None:
            soar_sensor_key = SoarLicenseObj.sensor_key
            if (soar_sensor_key is not None) or (soar_sensor_key != "null"):
                dynamic_sensor_key_dict.update({"soar_sensor_key":soar_sensor_key})
        
        if TraceLicenseObj is not None:
            trace_sensor_key = TraceLicenseObj.sensor_key
            if (trace_sensor_key is not None) or (trace_sensor_key != "null"):
                dynamic_sensor_key_dict.update({"trace_sensor_key":trace_sensor_key})
        
        # AgentDataObj = Agent_data.objects.filter(org_location = pk, updated_plan_id = pk2).first()
        # db_username = None
        # db_password = None
        # db_host = None
        # db_port = None

        # if AgentDataObj:
        #     db_username = AgentDataObj.db_username
        #     db_password = AgentDataObj.db_password
        #     db_host = AgentDataObj.db_host
        #     db_port = AgentDataObj.db_port

        # query_location = Attach_Location.objects.filter(id=pk, activated_plan_id = pk2)
        query_location = Attach_Location.objects.prefetch_related('agent_data_set').filter(id=pk, activated_plan_id = pk2)

        serializer = GetLocationSerializer(query_location,many = True,context = context_dict)
        data = serializer.data[0] # Get the first item from the serialized data list

        # data.update({"hids_sensor_key": hids_sensor_key, "nids_sensor_key":nids_sensor_key, "soar_sensor_key":soar_sensor_key, "trace_sensor_key":trace_sensor_key})
        data.update(dynamic_sensor_key_dict)

        msg = {"message_type": "data_found", "data": data}
    except Exception:
        msg = {"message_type": "d_not_f"}
    return Response(msg)


# display nested json---display organisation wise all locations
@api_view(['GET'])
def display_location_org_nested_json(request):
    try:       
        query = list(Attach_Location.objects.order_by().values_list('org_id', flat=True).distinct())
        nested_json = []
        for org in query:
            orgobj = Organization_data.objects.get(organization_id = org)
            ser_var = DisplayAllOrganizationSerializer(orgobj)
            location = list(Attach_Location.objects.values('org_id','id','city','branchcode').filter(org_id = org))
            # print(f"org_name:{ser_var.data.get('organization_name')}")
            org_name = ser_var.data.get('organization_name')
            for i,n in enumerate(location):
                branchcode_city = '{}-{}'.format(org_name, n['branchcode'])
                n['sensor_name'] = branchcode_city
                n['org_name'] = org_name
            updated_ser = {}
            updated_ser.update(ser_var.data)
            updated_ser.update({"location":location})
            nested_json.append(updated_ser)
        return Response(nested_json)
    except ObjectDoesNotExist:
        return Response({"message_type":"d_not_f"})
    
# get all location data within an organization #similar to bothstatus url
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def display_all_location_in_org(request):
    try:
        org_obj = Organization_data.objects.filter(is_active=False).values('organization_id')#filtering organizations which are disabled
        query = Organization_data.objects.all().exclude(organization_id__in=org_obj).order_by('-onboarding_timestamp')
        serializer = GetLocationsInOrgSerializer(query,many=True)
        Dict_org_ids = []
        for i, n in enumerate(serializer.data):
            id = n.get('organization_id')
            organization_name = n.get('organization_name')
            Dict_org_ids.append(id)
            location = list(Attach_Location.objects.values('org_id','id','city','branchcode').filter(org_id = id))
            for j,m in enumerate(location):
                branchcode_city = '{}-{}'.format(organization_name, m['branchcode'])
                m['sensor_name'] = branchcode_city
                m['org_name'] = organization_name
                n['location'] = location
        msg = {"message_type":"data_found","data":serializer.data}
    except ObjectDoesNotExist:
        msg = {"message_type":"d_not_f"}
    return Response(msg)

# get org-name in add location-step-1
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def add_location_get_org_name(request):
    try:
        org_obj = Organization_data.objects.filter(is_active=False).values('organization_id')#filtering organizations which are disabled
        query = Organization_data.objects.all().exclude(organization_id__in=org_obj).order_by('-onboarding_timestamp')
        serializer = AddLocationGetOrgNameSerializer(query,many=True)
        msg = {"message_type":"data_found","data":serializer.data}
    except ObjectDoesNotExist:
        msg = {"message_type":"d_not_f"}
    return Response(msg)

# # # step-2 add plan details
# Updated code step-2 location  plan and page permission models 29-09-23
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def add_location_step_two(request):
    location_id = request.POST.get('location_id')
    plan_name = request.data.get('plan_name')
    plan_descriptions = request.data.get('plan_descriptions')
    plan_start_date = request.data.get('plan_start_date')
    plan_end_date = request.data.get('plan_end_date')
    isodatetime = datetime.now(pytz.timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')
    random_key = str(uuid.uuid4())
    jsonRes = []
    plans_dee = None
    organization_instance = None
    plan_env_all = ['default_page', 'env_trace', 'env_nids', 'env_hids', 'env_soar', 'xdr_live_map', 'env_hc', 'env_mm', 'env_tptf', 'env_sbs', 'env_ess', 'env_tps']

    try:
        # Check if a Location with the provided location_id exists
        query_location = Attach_Location.objects.get(id=location_id)
        org_id = query_location.org_id

        # Initialize existing_plan to None
        existing_plan = None

        # Check if the Location already has an updated_plan_id
        if query_location.activated_plan_id:
            # If it has an updated_plan_id, check if a Plan with the same updated_plan_id exists
            existing_plan = Updated_Plan_Details.objects.filter(id=query_location.activated_plan_id.id).first()

            if existing_plan:
                # If a Plan with the same updated_plan_id exists, update its details
                existing_plan.plan_name = plan_name
                existing_plan.plan_descriptions = plan_descriptions
                existing_plan.plan_start_date = plan_start_date
                existing_plan.plan_end_date = plan_end_date
                existing_plan.plan_updations_timestamp = isodatetime
                existing_plan.save()
                
            else:
                plans_dee = Updated_Plan_Details(
                    plan_name=plan_name,
                    plan_descriptions=plan_descriptions,
                    plan_creations_timestamp=isodatetime,
                    plan_start_date=plan_start_date,
                    plan_end_date=plan_end_date,
                    plan_key=random_key,
                )

                plans_dee.save()
                query_location.activated_plan_id = plans_dee
                query_location.plan_status = True
                query_location.save()
              

        else:
            # If the Location doesn't have an updated_plan_id, create a new Plan instance and link it
            plans_dee = Updated_Plan_Details(
                plan_name=plan_name,
                plan_descriptions=plan_descriptions,
                plan_creations_timestamp=isodatetime,
                plan_start_date=plan_start_date,
                plan_end_date=plan_end_date,
                plan_key=random_key,  
            )

            plans_dee.save()
            query_location.activated_plan_id = plans_dee
            query_location.plan_status = True
            query_location.save()
           

        # Fetch the Organization_data instance based on the organization_id
        organization_instance = Organization_data.objects.filter(organization_id=org_id.organization_id).first()
        

        try:
            # Check if the Location already has an activated_plan_id
            if query_location.activated_plan_id:
                # If it has an activated_plan_id, check if a Plan with the same activated_plan_id exists
                existing_plan = Updated_Plan_Details.objects.filter(id=query_location.activated_plan_id.id).first()

            # Create or update Page_Permissions with plan_id
            query_client, created = Page_Permissions.objects.get_or_create(
                location_id=query_location,
                org_id=organization_instance
            )

            # Set the updated_plan_id attribute to existing_plan if it exists, otherwise plans_dee
            if existing_plan:
                print("Updating Page_Permissions")
                query_client.updated_plan_id = existing_plan
            else:
                print("Inserting Page_Permissions")
                query_client.updated_plan_id = plans_dee

            query_client.save()

            serializer = ActivateLocationSerializer(query_client, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()

                # Fetch the corresponding Updated_Plan_Details instance
                plan_query_obj = Updated_Plan_Details.objects.filter(id=query_client.updated_plan_id.id).first()

                # Dynamically update fields based on plan_env_all
                for env_type in plan_env_all:
                    field_name = env_type
                    field_value = getattr(query_client, env_type, None)
                    setattr(plan_query_obj, field_name, field_value)

                plan_query_obj.save()
                print(plan_query_obj)
                api_logs_make(request, "to add new page_permission behalf of location_id ", "to add new page")
                jsonRes = {"message_type": "successfully_inserted", "message": "Successfully inserted data in db","plan_id":query_location.activated_plan_id.id}
        except Page_Permissions.DoesNotExist:
            serializer = ActivateLocationSerializer(data=request.data)
            if serializer.is_valid():
                print("ser inserting")
                serializer.save()
                data = serializer.data

                plan_query_obj = Updated_Plan_Details.objects.filter(id=plans_dee.id).first()
                # Dynamically update fields based on plan_env_all
                for env_type in plan_env_all:
                    field_name = env_type
                    field_value = getattr(query_client, env_type, None)
                    print(field_value)
                    setattr(plan_query_obj, field_name, field_value)

                plan_query_obj.save()
                print(f"success update both tables: {plan_query_obj}")

                api_logs_make(request, "to add new page_permission behalf of location_id ", "to add new page")
                jsonRes = {"message_type": "successfully_inserted", "message": "Successfully inserted data in db","plan_id":query_location.activated_plan_id.id}

    except Attach_Location.DoesNotExist:
        return Response({"message_type": "errors", "message": "Location not found with the given ID"})

    return Response(jsonRes)
    

# To add location step-1
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
@permission_classes([IsAuthenticated])
def add_location_step_one(request):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    client_s3 = boto3.client('s3',aws_access_key_id = settings.AWS_ACCESS_KEY_ID,aws_secret_access_key= settings.AWS_SECRET_ACCESS_KEY)
    
    serializervariable = AddLocationStepOneSerializer(data=request.data)
    if serializervariable.is_valid():
        serializervariable.save()
        location_id = serializervariable.data.get('id')
        gst_image = serializervariable.data.get('gst_image')
        tan_image = serializervariable.data.get('tan_image')
        pan_image = serializervariable.data.get('pan_image')
        cin_image = serializervariable.data.get('cin_image')
        images = [gst_image, tan_image, pan_image, cin_image]
        api_logs_make(request,"Add location step-1 org","new location org added")
        for image in images:
            img_name = str(image).replace('/image/', '/')
            bucket_key = 'company-credential-details'+img_name
            file_location = 'static/image'+img_name
            client_s3.upload_file(file_location, bucket_name, bucket_key, ExtraArgs={'ContentType': 'image/jpeg'})
        return Response({"message_type":"successfully_inserted","message": "Successfully inserted data in db", "location_id":location_id}, status=status.HTTP_200_OK)
    else:
        return Response({"message_type":"unsuccessful","message": "Data was not inserted", "errors":serializervariable.errors}, status=status.HTTP_400_BAD_REQUEST)

# To add location step-3(to store column_values in to tuples)
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
@permission_classes([IsAuthenticated])
def add_location_step_three(request):
    location_id = request.POST.get('location_id')
    plan_id = request.POST.get('plan_id')
    db_username = request.data.get('db_username')
    db_password = request.data.get('db_password')
    db_port = request.data.get('db_port')
    db_host = request.data.get('db_host')

    try:
        locationobj = Attach_Location.objects.get(id=location_id,activated_plan_id = plan_id)
        org_id = locationobj.org_id
        branchcode = locationobj.branchcode

        org_name = str(locationobj.org_id.organization_name.strip(u'\u200b')).lower() #removing unicode if any
        trimmed_org_name = org_name.replace(" ", "")[:3] # removing whitespaces from org_name


    except ObjectDoesNotExist:
        return Response({"message_type": "d_not_f"}, status=status.HTTP_200_OK)
    try:
        plan_instance = Updated_Plan_Details.objects.get(id=plan_id)
    except Updated_Plan_Details.DoesNotExist:
        # Handle the case where the plan_id is not found
        plan_instance = None
     

    try:
        # entry for dashboard config
        platform_val = request.POST.getlist('platform_val[]')
        severity_val = request.POST.getlist('severity_val[]')
        trace_sensor = request.POST.getlist('trace_val[]')


        if len(platform_val) == 1:
            platform_val = f"('{platform_val[0]}')"  # Wrap single value in parentheses
        else:
            platform_val = tuple(platform_val)

        if len(severity_val) == 1:
            severity_val = f"({int(severity_val[0])})"  # Wrap single value in parentheses
        else:
            severity_val = f"({','.join(map(str, map(int, severity_val)))})"    
        if len(trace_sensor) == 1:
            trace_sensor = f"('{trace_sensor[0]}')"  # Wrap single value in parentheses
        else:
            trace_sensor = tuple(trace_sensor)

        init_config_detail = Init_Configs(
            config_type="dashboard_filter",
            platform_val=platform_val,
            severity_val=severity_val,
            accuracy_val=request.POST.get('accuracy_val'),
            trace_sensor=trace_sensor,
            org_id=org_id,
            location_id=locationobj,
            updated_plan_id = plan_instance,
        )

        init_config_detail.save()

        # entry for email config
        email_platform_val = request.POST.getlist('email_platform_val[]')
        email_severity_val = request.POST.getlist('email_severity_val[]')
        email_trace_val = request.POST.getlist('email_trace_val[]')


        if len(email_platform_val) == 1:
            email_platform_val = f"('{email_platform_val[0]}')"  # Wrap single value in parentheses
        else:
            email_platform_val = tuple(email_platform_val)

        if len(email_severity_val) == 1:
            email_severity_val = f"({int(email_severity_val[0])})"  # Wrap single value in parentheses
        else:
            email_severity_val = f"({','.join(map(str, map(int, email_severity_val)))})"    
   
        if len(email_trace_val) == 1:
            email_trace_val = f"('{email_trace_val[0]}')"  # Wrap single value in parentheses
        else:
            email_trace_val = tuple(email_trace_val)        

        init_config_detail = Init_Configs(
            config_type="email_config_live",
            email_ids=request.POST.get('email'),
            platform_val=email_platform_val,
            severity_val=email_severity_val,
            accuracy_val=request.POST.get('email_accuracy_val'),
            trace_sensor=email_trace_val,
            org_id=org_id,
            location_id=locationobj,
            updated_plan_id = plan_instance
        )

        init_config_detail.save()

        # entry for notification config
        notification_platform_val = request.POST.getlist('notification_platform_val[]')
        notification_severity_val = request.POST.getlist('notification_severity_val[]')
        notification_trace_val= request.POST.getlist('notification_trace_val[]')
       

        if len(notification_platform_val) == 1:
            notification_platform_val = f"('{notification_platform_val[0]}')"  # Wrap single value in parentheses
        else:
            notification_platform_val = tuple(notification_platform_val)

        if len(notification_severity_val) == 1:
            notification_severity_val = f"({int(notification_severity_val[0])})"  # Wrap single value in parentheses
        else:
            notification_severity_val = f"({','.join(map(str, map(int, notification_severity_val)))})"    


        if len(notification_trace_val) == 1:
            notification_trace_val = f"('{notification_trace_val[0]}')"  # Wrap single value in parentheses
        else:
            notification_trace_val = tuple(notification_trace_val)    

        init_config_detail = Init_Configs(
            config_type="notification_live",
            platform_val=notification_platform_val,
            severity_val=notification_severity_val,
            time_interval_val=request.POST.get('time_interval_val'),
            accuracy_val=request.POST.get('notification_accuracy_val'),
            trace_sensor=notification_trace_val,
            org_id=org_id,
            location_id=locationobj,
            updated_plan_id = plan_instance,
        )

        init_config_detail.save()

        sensor_dict = {
            "nids": ["event", "alert", "incident", "assets", "nmap", "glog"],
            "trace": ["event", "alert", "incident", "glog", "dpi"],
            "hids": ["event", "alert", "incident", "assets"],
            "soar": ["actions"],
            "single_log": ["tps", "ess", "sbs", "tptf", "mm", "hc"]
        }

        # add data to agent table
        agent_data = Agent_data()

        for key, values in sensor_dict.items():
            for value in values:
                if value == "glog":
                    setattr(agent_data, f"{key}_global_agent",f"xdr-glog")
                elif key == "soar":
                    setattr(agent_data, f"{key}_agent",
                            f"xdr-{key}-{value}-{{}}-{{}}".format(trimmed_org_name, branchcode))
                elif key == "single_log":
                    setattr(agent_data, f"{value}_agent",
                            f"xdr-{value}-feeds-{{}}-{{}}".format(trimmed_org_name, branchcode))
                else:
                    setattr(agent_data, f"{key}_{value}_agent",
                            f"xdr-{key}-{value}-{{}}-{{}}".format(trimmed_org_name, branchcode))

        agent_data.org_location = locationobj
        agent_data.updated_plan_id = plan_instance
        agent_data.organization_id = org_id
        random_key = str(uuid.uuid4())
        agent_data.attach_agent_key = random_key
        agent_data.attach_agent_group = "xdr-logs-{}".format(trimmed_org_name)
        agent_data.attach_agent_network = "xdr-network-map-{}".format(trimmed_org_name)
        agent_data.wazuh_attach_agent = "xdr-wazuhlogs-{}".format(trimmed_org_name)
        agent_data.trace_attach_agent = "xdr-trace-{}".format(trimmed_org_name)
        agent_data.db_password = db_password
        agent_data.db_host = db_host
        agent_data.db_port = db_port
        agent_data.db_username = db_username

        agent_data.save()

        api_logs_make(request, "Add location step-3 org", "new location org added")

        return Response({"message_type": "successfully_inserted", "message": "Successfully inserted data in db"},
                        status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message_type": "unsuccessful", "message": "Data was not inserted", "errors": str(e)},
                        status=status.HTTP_400_BAD_REQUEST)



# To get email_config with location_id and config_types
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
@permission_classes([IsAuthenticated])
def email_config_update(request):
    location_id = request.POST.get('location_id')
    config_type = request.POST.get('config_type')
    plan_id = request.POST.get('activated_plan_id')
    if config_type is None:
        return Response({"message_type":"unsuccessful", "message":"config_type_n_found"})
    
    if location_id is None:
        return Response({"message_type":"unsuccessful", "message":"location_id_n_found"})
    
    if plan_id is None:
        return Response({"message_type":"unsuccessful", "message":"plan_id_n_found"})
    
    try:
        locationobj = Attach_Location.objects.get(id=location_id)
        init_config_detail = Init_Configs.objects.get(location_id=locationobj, config_type=config_type, updated_plan_id = plan_id)
    except Attach_Location.DoesNotExist:
        return Response({"message_type": "location_not_found"})
    except Init_Configs.DoesNotExist:
        return Response({"message_type": "config_not_found"})
    
    platform_val_tuple = request.data.getlist('platform_val[]')
    severity_val_tuple = request.data.getlist('severity_val[]')
    trace_sensor_tuple = request.data.getlist('trace_sensor[]')
    email_ids_tuple = request.data.getlist('email_ids[]')

    if len(platform_val_tuple) == 1:
        platform_val_tuple = f"('{platform_val_tuple[0]}')"  # Wrap single value in parentheses
    else:
        platform_val_tuple = tuple(platform_val_tuple)

    if len(severity_val_tuple) == 1:
        severity_val_tuple = f"({int(severity_val_tuple[0])})"  # Wrap single value in parentheses
    else:
        severity_val_tuple = f"({','.join(map(str, map(int, severity_val_tuple)))})" 

    if len(trace_sensor_tuple) == 1:
        trace_sensor_tuple = f"('{trace_sensor_tuple[0]}')"  # Wrap single value in parentheses
    else:
        trace_sensor_tuple = tuple(trace_sensor_tuple)  

    if len(email_ids_tuple) == 1:
        email_ids_tuple = email_ids_tuple[0]  # Wrap single value in parentheses
    else:
        email_ids_tuple = f"{','.join(map(str, email_ids_tuple))}"
        
    init_config_detail.platform_val = platform_val_tuple
    init_config_detail.severity_val = severity_val_tuple
    init_config_detail.trace_sensor = trace_sensor_tuple
    init_config_detail.email_ids = email_ids_tuple
    init_config_detail.config_type = config_type
    init_config_detail.save()
    
    serializer = EmailConfigSerializer(init_config_detail)  # Use your serializer class here
    data = serializer.data
    data['platform_val'] = platform_val_tuple
    data['severity_val'] = severity_val_tuple
    data['trace_sensor'] = trace_sensor_tuple
    data['email_ids'] = email_ids_tuple
    
    api_logs_make(request, "Update email config", "email config updated")
  
    return Response({"message_type": "updated successfully"})
    
# To get dashboard_config with location_id and config_types
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
@permission_classes([IsAuthenticated])
def dashboard_config_update(request):
    location_id = request.POST.get('location_id')
    config_type = request.POST.get('config_type')
    plan_id = request.POST.get('activated_plan_id')

    if config_type is None:
        return Response({"message_type":"unsuccessful", "message":"config_type_n_found"})
    
    if location_id is None:
        return Response({"message_type":"unsuccessful", "message":"location_id_n_found"})
    
    if plan_id is None:
        return Response({"message_type":"unsuccessful", "message":"plan_id_n_found"})
    
    try:
        locationobj = Attach_Location.objects.get(id=location_id)
        init_config_detail = Init_Configs.objects.get(location_id=locationobj, config_type=config_type, updated_plan_id = plan_id)
    except Attach_Location.DoesNotExist:
        return Response({"message_type": "location_not_found"})
    except Init_Configs.DoesNotExist:
        return Response({"message_type": "config_not_found"})

    platform_val_tuple = request.data.getlist('platform_val[]')
    severity_val_tuple = request.data.getlist('severity_val[]')
    trace_sensor_tuple = request.data.getlist('trace_sensor[]')

    if len(platform_val_tuple) == 1:
        platform_val_tuple = f"('{platform_val_tuple[0]}')"  # Wrap single value in parentheses
    else:
        platform_val_tuple = tuple(platform_val_tuple)

    if len(severity_val_tuple) == 1:
        severity_val_tuple = f"({int(severity_val_tuple[0])})"  # Wrap single value in parentheses
    else:
        severity_val_tuple = f"({','.join(map(str, map(int, severity_val_tuple)))})" 

    if len(trace_sensor_tuple) == 1:
        trace_sensor_tuple = f"('{trace_sensor_tuple[0]}')"  # Wrap single value in parentheses
    else:
        trace_sensor_tuple = tuple(trace_sensor_tuple)  

    init_config_detail.platform_val = platform_val_tuple
    init_config_detail.severity_val = severity_val_tuple
    init_config_detail.accuracy_val = request.data.get('accuracy_val')[0]
    init_config_detail.trace_sensor = trace_sensor_tuple
    init_config_detail.config_type = config_type
    init_config_detail.save()

    serializer = DahboardConfigSerializer(init_config_detail)  # Use your serializer class here
    data = serializer.data
    data['platform_val'] = platform_val_tuple
    data['severity_val'] = severity_val_tuple
    data['trace_sensor'] = trace_sensor_tuple
    api_logs_make(request,"Update dashboard config","dashboard config updated")

    return Response({"message_type": "updated successfully", "data": data})


# To get notification_config with location_id and config_types
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
@permission_classes([IsAuthenticated])
def notification_config_update(request):
    location_id = request.POST.get('location_id')
    config_type = request.POST.get('config_type')
    plan_id = request.POST.get('activated_plan_id')

    if config_type is None:
        return Response({"message_type":"unsuccessful", "message":"config_type_n_found"})
    
    if location_id is None:
        return Response({"message_type":"unsuccessful", "message":"location_id_n_found"})
    
    if plan_id is None:
        return Response({"message_type":"unsuccessful", "message":"plan_id_n_found"})

    try:
        locationobj = Attach_Location.objects.get(id=location_id)
        init_config_detail = Init_Configs.objects.get(location_id=locationobj, config_type=config_type, updated_plan_id = plan_id)
    except Attach_Location.DoesNotExist:
        return Response({"message_type": "location_not_found"})
    except Init_Configs.DoesNotExist:
        return Response({"message_type": "config_not_found"})
    platform_val_tuple = request.data.getlist('platform_val[]')
    severity_val_tuple = request.data.getlist('severity_val[]')
    trace_sensor_tuple = request.data.getlist('trace_sensor[]')

    if len(platform_val_tuple) == 1:
        platform_val_tuple = f"('{platform_val_tuple[0]}')"  # Wrap single value in parentheses
    else:
        platform_val_tuple = tuple(platform_val_tuple)

    if len(severity_val_tuple) == 1:
        severity_val_tuple = f"({int(severity_val_tuple[0])})"  # Wrap single value in parentheses
    else:
        severity_val_tuple = f"({','.join(map(str, map(int, severity_val_tuple)))})" 

    if len(trace_sensor_tuple) == 1:
        trace_sensor_tuple = f"('{trace_sensor_tuple[0]}')"  # Wrap single value in parentheses
    else:
        trace_sensor_tuple = tuple(trace_sensor_tuple)  
    init_config_detail.platform_val = platform_val_tuple
    init_config_detail.severity_val = severity_val_tuple
    init_config_detail.trace_sensor = trace_sensor_tuple
    init_config_detail.time_interval_val = int(request.data.get('time_interval_val', 0))
    init_config_detail.config_type = config_type
    init_config_detail.save()

    serializer = NotificationConfigSerializer(init_config_detail)  # Use your serializer class here
    data = serializer.data
    data['platform_val'] = platform_val_tuple
    data['severity_val'] = severity_val_tuple
    data['trace_sensor'] = trace_sensor_tuple
    api_logs_make(request,"notification config","notification config updated")

    return Response({"message_type": "updated successfully", "data": data})  


#To get all notification config email
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def display_notification_config(request):
    location_id = request.POST.get("location_id")
    try:       
        query_client = Init_Configs.objects.filter(config_type = 'notification_live').filter(location_id = location_id)
        serializer_org_users =NotificationConfigSerializer(query_client,many = True)
        return Response({"message_type":"data_found","data":serializer_org_users.data})
    except ObjectDoesNotExist:
        return Response({"message_type":"d_not_f"})      
    

#To get all dashboard config email
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def display_dashboard_config(request):
    location_id = request.POST.get("location_id")
    try:       
        query_client = Init_Configs.objects.filter(config_type = 'dashboard_filter').filter(location_id = location_id)
        serializer_org_users = DahboardConfigSerializer(query_client,many = True)
        return Response({"message_type":"data_found","data":serializer_org_users.data})
    except ObjectDoesNotExist:
        return Response({"message_type":"d_not_f"})    

#To get all dashboard config email
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def display_email_config(request):
    location_id = request.POST.get("location_id")
    try:       
        query_client = Init_Configs.objects.filter(config_type = 'email_config_live').filter(location_id = location_id)
        serializer_org_users =  Email_Config_Serializer(query_client,many = True)
        return Response({"message_type":"data_found","data":serializer_org_users.data})
    except ObjectDoesNotExist:
        return Response({"message_type":"d_not_f"})             

#To get all details of init config email and dashboard record
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_display_config(request):
    config_type = request.GET.get("config_type")
    location_id = request.GET.get("location_id")
    plan_id = request.GET.get("activated_plan_id")
    if config_type is None:
        return Response({"message_type":"d_not_f", "message":"config_type_n_found"})
    
    if (location_id is None) or (location_id == "null"):
        return Response({"message_type":"d_not_f", "message":"location_id_n_found"})
    
    if (plan_id is None) or (plan_id == "null"):
        return Response({"message_type":"d_not_f", "message":"plan_id_n_found"})
    
    try: 
        query_client = Init_Configs.objects.filter(config_type = config_type, location_id = location_id, updated_plan_id = plan_id)

        if not query_client:
            return Response({"message_type":"d_not_f"})

        serializer_org_users = Config_Serializer(query_client,many = True)
        data = serializer_org_users.data
        for obj in data:
            if 'platform_val' in obj:
                    platform_val = obj['platform_val']
                    if platform_val is not None:
                        platform_val = platform_val.strip("()")  # Remove parentheses
                        platform_val = platform_val.replace("'", "")  # Remove single quotes
                        platform_val = platform_val.replace(" ", "")
                    else:
                        platform_val = ""  # Set platform_val to an empty string
                    obj['platform_val'] = platform_val

            if 'severity_val' in obj:
                severity_val = obj['severity_val']
                if severity_val.startswith("(") and severity_val.endswith(")"):
                    severity_val = severity_val[1:-1]  # Remove parentheses
                obj['severity_val'] = severity_val  

            if 'trace_sensor' in obj:
                trace_sensor = obj['trace_sensor']
                if trace_sensor is not None:
                    trace_sensor = trace_sensor.strip("()")  # Remove parentheses
                    trace_sensor = trace_sensor.replace("'", "")  # Remove single quotes
                    trace_sensor = trace_sensor.replace(" ", "")
                else:
                    trace_sensor = ""  # Set platform_val to an empty string
                obj['trace_sensor'] = trace_sensor

            if 'time_interval_val' in obj:
                time_interval_val = obj['time_interval_val']
                if time_interval_val is not None:
                    time_interval_val = int(time_interval_val)  # Convert to integer
                obj['time_interval_val'] = time_interval_val

        return Response({"message_type":"data_found","data":serializer_org_users.data})
    except ObjectDoesNotExist:
        return Response({"message_type":"d_not_f"})
    
# To agents details active or deactive behalf of location_id org_id,is_active = 1 or 0 from agent details models      
@api_view(['POST'])
def is_active_true_false_all_agent(request):
    org_id = request.GET.get("org_id")
    location_id = request.GET.get("location_id")
    is_active = request.GET.get('is_active')

    try:
        query_client = Agent_data.objects.filter(organization_id=org_id, org_location=location_id).first()

        if query_client:
            if is_active == "1":
                query_client.is_active = True
            elif is_active == "0":
                query_client.is_active = False
            query_client.save()

            serializer = UpdateAllagentDetailsSerializer(query_client,data = request.data)
            if serializer.is_valid():
                serializer.save()
                api_logs_make(request,"is_active updated agent details","agent details active or deactive")
                return Response({"message_type": "updated_successfully", "data": serializer.data})
            else:
                return Response({"message_type": "validation_error", "data": serializer.errors})
        else:
            return Response({"message_type": "d_not_f", "data": "No data found for the given location_id"})
    except Agent_data.DoesNotExist:
        return Response({"message_type": "d_not_f", "data": "No data found for the given location_id"})

# # To get page permission
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def display_all_pagepermission(request):
    location_id = request.GET.get("location_id")
    plan_id = request.GET.get("activated_plan_id")

    if (location_id is None) or (location_id == "null"):
        return Response({"message_type": "d_not_f", "data": "location_id_n_found"})
    
    if (plan_id is None) or (plan_id == "null"):
        return Response({"message_type": "d_not_f", "data": "plan_id_n_found"})

    try:
        query_page = Page_Permissions.objects.filter(location_id=location_id, updated_plan_id = plan_id)
        
        if not query_page:
            return Response({"message_type": "d_not_f"})
        else:
            serializer = AddPagePermissionsSerializer(query_page, many=True)
            data = serializer.data  # Retrieve serialized data as a list
            response_data = data[0] if data else {}  # Retrieve the first object from the list or an empty dictionary if no data is found
            return Response({"message_type": "data_found", "data": response_data})
    
    except Page_Permissions.DoesNotExist:
        return Response({"message_type": "d_not_f", "data": "No data found for the given location_id"})


# To update page permission behalf of location_id, plan_id also updated_plan_details would be updated
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_pagepermission(request):
    location_id = request.data.get("location_id")
    plan_id = request.data.get('activated_plan_id')
    
    if location_id is None:
        return Response({"message_type":"unsuccessful", "message":"location_id_n_found"})
    
    if plan_id is None:
        return Response({"message_type":"unsuccessful", "message":"plan_id_n_found"})
    
    data = request.data.copy()
    data.pop("location_id")  # Remove the location_id from the data payload

    try:
        PagePermissionsObj = Page_Permissions.objects.filter(location_id=location_id, updated_plan_id = plan_id).first()  # Use .first() to get a single object
        UpdatePlanObj = Updated_Plan_Details.objects.get(id = plan_id)
        page_permission_serializer = UpdatePagePermissionsSerializer(PagePermissionsObj, data=data, partial=True)

        if page_permission_serializer.is_valid():
            page_permission_serializer.save()
            updated_data_for_plan_table = page_permission_serializer.data
            updated_plan_serializer = UpdatePlanWithPagePermissionsSerializer(UpdatePlanObj, data=updated_data_for_plan_table, partial=True)
            if updated_plan_serializer.is_valid():
                updated_plan_serializer.save()

            api_logs_make(request,"updated pagepermission, updated plan behalf of location_id, plan_id","pagepermission, plan updated")
            return Response({"message_type": "updated_successfully", "data": page_permission_serializer.data})
        else:
            return Response({"message_type": "unsuccessful", "data": page_permission_serializer.errors})
    except (Page_Permissions.DoesNotExist, Updated_Plan_Details.DoesNotExist):
        return Response({"message_type": "unsuccessful", "data": "No data found for the given location_id"})

# To update opensearch connection credentials(like db_host, db_port, username, password) on behalf of location_id
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def update_opensearch_connection_details(request):
    location_id = request.data.get("location_id")
    plan_id = request.data.get('activated_plan_id')
    if location_id is None:
        return Response({"message_type":"unsuccessful", "message":"location_id_n_found"})
    
    if plan_id is None:
        return Response({"message_type":"unsuccessful", "message":"plan_id_n_found"})
    
    request_data_copy = request.data.copy()
    request_data_copy.pop("location_id")  # Remove the location_id from the data payload
    request_data_copy.pop("activated_plan_id")

    agent_table_query = Agent_data.objects.filter(org_location=location_id, updated_plan_id = plan_id).first()  # Use .first() to get a single object #returns None if object not found
    if not agent_table_query:
        return Response({"message_type": "unsuccessful", "data": "No data found for the given location_id, plan_id"})
    
    serializer = UpdateAgentDataSerializer(agent_table_query, data=request_data_copy, partial=True)
    if serializer.is_valid():
        serializer.save()
        api_logs_make(request,"updated agentdetails on behalf of location_id, plan_id","opensearch connection credentials updated")
        return Response({"message_type": "success", "data": serializer.data})
    else:
        return Response({"message_type": "unsuccessful", "data": serializer.errors})
    

# display email id of all clients within same location--using login id 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def EmailClientListOrg(request):
    location_id = request.GET.get("location_id")
    msg = {"message_type":"s_is_w"}
    try:
        queryset = Client_data.objects.filter(location_id = location_id)
        if not queryset:
            return Response({"message_type":"data_not_found"})
        serializer = Clent_Email_Serializer(queryset, many = True)
        msg = {"message_type":"d_found", "data": serializer.data}
    except ObjectDoesNotExist:
        msg = {"message_type":"data_not_found"}
    
    return Response(msg)


# To add trace license management details with updated if location_id allready exist then updated behalf of location_id
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
@permission_classes([IsAuthenticated])
def add_trace_license_management(request):
    request.data._mutable = True
    try:
        request_data = request.data
        location_id = request.POST.get("location_id")
        plan_id_val = request.POST.get("plan_id")
        # print(f"plan_id_val: {request.data}")
        random_key = str(uuid.uuid4())
        isodatetime = datetime.now(pytz.timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')

        if not location_id:
            return Response({"message_type": "missing_location_id_field", "errors": "location_id field is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            location_query = Attach_Location.objects.get(id=location_id)
            # branch_code_Val = location_query.branchcode
            plan_query = Updated_Plan_Details.objects.get(id=plan_id_val)
     

            org_id_val = location_query.org_id
            sensor_name_list = request.POST.getlist("sensor_name[]")
            if sensor_name_list == ['']:
                sensor_name_list = ""
            elif len(sensor_name_list) == 1:
                sensor_name_list = f"('{sensor_name_list[0]}')"  # Wrap single value in parentheses
            else:
                sensor_name_list = str(tuple(sensor_name_list))

            # Calculate sensor_active_count from sensor_create_count
            sensor_create_count = int(request_data.get("sensor_create_count", 0))
            sensor_active_count = sensor_create_count  # Set sensor_active_count to sensor_create_count

            context_data = {
                'sensor_name': sensor_name_list,
                'updated_plan_id': plan_query.id,
                'sensor_active_count': sensor_active_count,  # Set sensor_active_count here
                # Add other fields here
            }
            request_data.update(context_data)

            try:
                existing_record = Trace_License_Management.objects.get(updated_plan_id=plan_query.id)
                serializer = TraceLicenseManagementSerializer(existing_record, data=request_data)
                if serializer.is_valid():
                    serializer.validated_data['updated_at'] = isodatetime
                    serializer.save()
                    api_logs_make(request, "Update trace license_management details", "trace license_management details updated")
                    return Response({"message_type": "success", "message": "Successfully updated data in db"})
                else:
                    return Response({"message_type": "unsuccessful", "message": "Data was not updated", "error": serializer.errors})
            except Trace_License_Management.DoesNotExist:
                request_data['created_at'] = isodatetime
                request_data['sensor_key'] = random_key
                request_data['sensor_active_count'] = sensor_active_count

                serializervariable = TraceLicenseManagementSerializer(data=request_data)
                if serializervariable.is_valid():
                    serializervariable.save()
                    api_logs_make(request, "Add trace license_management details", "new trace license_management added")
                    return Response({"message_type": "success", "message": "Successfully inserted data in db"})
                else:
                    return Response(serializervariable.errors)
        except Attach_Location.DoesNotExist:
            return Response({"message_type": "unsuccessful", "message": "Location does not exist"})
        except Organization_data.DoesNotExist:
            return Response({"message_type": "unsuccessful", "message": "Organization does not exist"})
        except Exception as e:
            return Response({"message_type": "unsuccessful", "message": str(e)})
    except Exception as e:
        return Response({"message_type": "unsuccessful", "message": str(e)})

# To add Nids license management details with updated if location_id allready exist then updated behalf of location_id
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
@permission_classes([IsAuthenticated])
def add_nids_license_management(request):
    request.data._mutable = True
    location_id = request.POST.get("location_id")
    plan_id_val = request.POST.get("plan_id")
    request_data = request.data

    random_key = str(uuid.uuid4())
    if not location_id:
        return Response({"message_type": "missing_location_id_filed", "errors": "location_id fields are required"}, status=status.HTTP_400_BAD_REQUEST)  
    isodatetime = datetime.now(pytz.timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')
    try:
       
        query_plan = Updated_Plan_Details.objects.get(id =plan_id_val)
        # Calculate sensor_active_count from sensor_create_count
        sensor_create_count = int(request_data.get("sensor_create_count", 0))
        sensor_active_count = sensor_create_count  # Set sensor_active_count to sensor_create_count

        contextData = {
            'updated_plan_id':query_plan.id,
            'sensor_active_count':sensor_active_count,
           

        }
        request.data.update(contextData)

        try:
            # Attempt to retrieve an existing record based on location_id and product_id (static)
            existing_record = Nids_License_Management.objects.get(updated_plan_id=query_plan.id)
           
            serializer = NidsLicenseManagementSerializer(existing_record, data=request.data)
            if serializer.is_valid():
                serializer.validated_data['updated_at'] = isodatetime
                serializer.save()
                api_logs_make(request, "Update nids license_management details", "nids license_management details updated")
                return Response({"message_type": "success", "message": "Successfully updated data in db"})
            else:
                return Response({"message_type": "unsuccessful", "message": "Data was not updated"})
        except Nids_License_Management.DoesNotExist:
            # If the record does not exist, proceed to insert a new one
            request.data['created_at'] = isodatetime 
            request.data['updated_plan_id'] = query_plan.id
            request.data['sensor_key'] = random_key
            request_data['sensor_active_count'] = sensor_active_count
            serializervariable = NidsLicenseManagementSerializer(data=request.data)
            if serializervariable.is_valid():
                serializervariable.save()
                api_logs_make(request, "Add nids license_management details", "new nids license_management added")
                return Response({"message_type": "success", "message": "Successfully inserted data in db","data":serializervariable.data})
            else:
                return Response({"message_type": "unsuccessful", "message": "Data was not inserted"})
    except Attach_Location.DoesNotExist:
        return Response({"message_type": "unsuccessful", "message": "Location does not exist"})
    except Organization_data.DoesNotExist:
        return Response({"message_type": "unsuccessful", "message": "Organization does not exist"})
    except Exception as e:
        return Response({"message_type": "unsuccessful", "message": str(e)}) 
    

# To add hids license management details with updated if location_id allready exist then updated behalf of location_id
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
@permission_classes([IsAuthenticated])
def add_hids_license_management(request):
    request.data._mutable = True
    request_data = request.data
    location_id = request.POST.get("location_id")
    plan_id_val = request.POST.get("plan_id")
    random_key = str(uuid.uuid4())
    if not location_id:
        return Response({"message_type": "missing_location_id_filed", "errors": "location_id fields are required"}, status=status.HTTP_400_BAD_REQUEST)
    isodatetime = datetime.now(pytz.timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')  
    try:
        query_plan = Updated_Plan_Details.objects.get(id = plan_id_val)
        sensor_create_count = int(request_data.get("sensor_create_count", 0))
        sensor_active_count = sensor_create_count  # Set sensor_active_count to sensor_create_count

        contextData = {
            'updated_plan_id':query_plan.id,
            'sensor_active_count':sensor_active_count,
        }
        request.data.update(contextData)
       
        try:
            # Attempt to retrieve an existing record based on location_id and product_id (static)
            existing_record = Hids_License_Management.objects.get(updated_plan_id=query_plan.id)
            serializer = HidsLicenseManagementSerializer(existing_record, data=request.data)
            if serializer.is_valid():
                serializer.validated_data['updated_at'] = isodatetime
                serializer.save()
                api_logs_make(request, "Update hids license_management details", "hids license_management details updated")
                return Response({"message_type": "success", "message": "Successfully updated data in db"})
            else:
                return Response({"message_type": "unsuccessful", "message": "Data was not updated"})
        except Hids_License_Management.DoesNotExist:
            # If the record does not exist, proceed to insert a new one
            request.data['created_at'] = isodatetime 
            request.data['updated_plan_id'] = query_plan.id
            request.data['sensor_key'] = random_key
            request_data['sensor_active_count'] = sensor_active_count
            serializervariable = HidsLicenseManagementSerializer(data=request.data)
            if serializervariable.is_valid():
                serializervariable.save()
                api_logs_make(request, "Add hids license_management details", "new hids license_management added")
                return Response({"message_type": "success", "message": "Successfully inserted data in db"})
            else:
                return Response(serializervariable.errors)
    except Attach_Location.DoesNotExist:
        return Response({"message_type": "unsuccessful", "message": "Location does not exist"})
    except Organization_data.DoesNotExist:
        return Response({"message_type": "unsuccessful", "message": "Organization does not exist"})
    except Exception as e:
        return Response({"message_type": "unsuccessful", "message": str(e)}) 
    

# To add Soar Sensor details with updated if location_id allready exist then updated behalf of location_id
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
@permission_classes([IsAuthenticated])
def add_soar_license_management(request):
    request.data._mutable = True
    location_id = request.POST.get("location_id")
    plan_id_val = request.POST.get("plan_id")
    random_key = str(uuid.uuid4())
    request_data = request.data
    if not location_id:
        return Response({"message_type": "missing_location_id_filed", "errors": "location_id fields are required"}, status=status.HTTP_400_BAD_REQUEST)
    isodatetime = datetime.now(pytz.timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')  
    try:
        query_plan = Updated_Plan_Details.objects.get(id = plan_id_val)
        sensor_create_count = int(request_data.get("sensor_create_count", 0))
        sensor_active_count = sensor_create_count  # Set sensor_active_count to sensor_create_count

        contextData = {
            'updated_plan_id':query_plan.id,
            'sensor_active_count':sensor_active_count,
        }
        request.data.update(contextData)
       
        try:
            # Attempt to retrieve an existing record based on location_id and product_id (static)
            existing_record = Soar_License_Management.objects.get(updated_plan_id=query_plan.id)
            serializer = SoarSensorDetailsSerializer(existing_record, data=request.data)
            if serializer.is_valid():
                serializer.validated_data['updated_at'] = isodatetime
                serializer.save()
                api_logs_make(request, "Update soar sensor details", "soar sensor details updated")
                return Response({"message_type": "success", "message": "Successfully updated data in db"})
            else:
                return Response({"message_type": "unsuccessful", "message": "Data was not updated"})
        except Soar_License_Management.DoesNotExist:
            # If the record does not exist, proceed to insert a new one
            request.data['created_at'] = isodatetime 
            request.data['updated_plan_id'] = query_plan.id
            request.data['sensor_key'] = random_key
            request_data['sensor_active_count'] = sensor_active_count
            serializervariable = SoarSensorDetailsSerializer(data=request.data)
            if serializervariable.is_valid():
                serializervariable.save()
                api_logs_make(request, "Add soar sensor details", "new soar sensor details added")
                return Response({"message_type": "success", "message": "Successfully inserted data in db"})
            else:
                return Response({"message_type": "unsuccessful", "message": "Data was not inserted"})
    except Attach_Location.DoesNotExist:
        return Response({"message_type": "unsuccessful", "message": "Location does not exist"})
    except Organization_data.DoesNotExist:
        return Response({"message_type": "unsuccessful", "message": "Organization does not exist"})
    except Exception as e:
        return Response({"message_type": "unsuccessful", "message": str(e)})

# to get api trace license management details on basis of plan_id
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def display_trace_license_management(request):
    if request.method == 'GET':
        plan_id = request.GET.get('activated_plan_id')

        if (plan_id is None) or (plan_id == "null"):
            return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

        try:
            query_trace_license_management = Trace_License_Management.objects.filter(updated_plan_id=plan_id)
            serializer_trace_license_management = GetTraceLicenseManagementSerializer(query_trace_license_management, many=True)
            data = serializer_trace_license_management.data

            # Modify sensor_name in response data
            for obj in data:
                if 'sensor_name' in obj:
                    sensor_name = obj['sensor_name']
                    if sensor_name is not None:
                        sensor_name = sensor_name.strip("()")  # Remove parentheses
                        sensor_name = sensor_name.replace("'", "")  # Remove single quotes
                        sensor_name = sensor_name.replace(" ", "")
                    else:
                        sensor_name = ""  # Set sensor_name to an empty string
                    obj['sensor_name'] = sensor_name

            if serializer_trace_license_management.data:
                response_data = {"message_type": "success", "data": data}
                return Response(response_data)
            else:
                return Response({"message_type": "d_not_f", "message": "No data found for the provided plan_id"})

        except ObjectDoesNotExist:
            return Response({"message_type": "d_not_f", "message": "No data found for the provided plan_id"})

    elif request.method == 'POST':
        plan_id = request.GET.get('activated_plan_id')
        isodatetime = datetime.now(pytz.timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')

        if not plan_id:
            return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

        try:
            updated_plan_details = Updated_Plan_Details.objects.get(id=plan_id)
        except Updated_Plan_Details.DoesNotExist:
            return Response({"message_type": "d_not_f", "message": "Plan not found"})

        random_key = str(uuid.uuid4())

        try:
            trace_license_management_query = Trace_License_Management.objects.get(updated_plan_id=updated_plan_details)
            serializer = GetTraceLicenseManagementSerializer(instance=trace_license_management_query, data=request.data)
        except Trace_License_Management.DoesNotExist:
            request_data = request.data.copy()
            request_data['created_at'] = isodatetime
            request_data['sensor_create_count'] = int(request.data.get("sensor_create_count", 0))

            # Set sensor_active_count to the same value as sensor_create_count
            request_data['sensor_active_count'] = request_data['sensor_create_count']

            request_data['updated_plan_id'] = updated_plan_details.id
            request_data['sensor_key'] = random_key

            # Modify sensor_name in request_data
            sensor_name_list = request.POST.getlist("sensor_name[]")
            if sensor_name_list == ['']:
                sensor_name_list = ""
            elif len(sensor_name_list) == 1:
                sensor_name_list = f"('{sensor_name_list[0]}')"  # Wrap single value in parentheses
            else:
                sensor_name_list = str(tuple(sensor_name_list))

            request_data['sensor_name'] = sensor_name_list

            serializer = GetTraceLicenseManagementSerializer(data=request_data)

        if serializer.is_valid():
            # Check if the instance existed before and after the serializer's save
            instance_existed_before = hasattr(serializer, 'instance')
            instance = serializer.save()
            api_logs_make(request, "Add trace license_management details behalf of plan_id", "trace license_management added behalf of plan_id")
            # Set sensor_active_count to the same value as sensor_create_count in the saved instance
            instance.sensor_active_count = instance.sensor_create_count
            instance.save()

            instance_existed_after = hasattr(serializer, 'instance')

            if instance_existed_before and instance_existed_after:
                response_data = {"message_type": "success", "message": "Data was updated in db", "data": serializer.data}
            elif not instance_existed_before and instance_existed_after:
                response_data = {"message_type": "success", "message": "Data was inserted in db", "data": serializer.data}
            else:
                response_data = {"message_type": "d_not_f", "message": "Data was not updated or inserted"}
        else:
            response_data = {"message_type": "d_not_f", "message": "Data was not updated or inserted"}

        return Response(response_data)
    
# to get nids license management details on basis of plan_id
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def display_nids_license_management(request):
    if request.method == 'GET':
        plan_id = request.GET.get('activated_plan_id')

        if (plan_id is None) or (plan_id == "null"):
            return Response({"message_type": "d_not_f", "message": "plan_id_not_found"})

        try:
            nids_license_management_query = Nids_License_Management.objects.get(updated_plan_id=plan_id)
        except Nids_License_Management.DoesNotExist:
            return Response({"message_type": "d_not_f", "message": "Plan not found"})

        serializer = NidsLicenseManagementSerializer(instance=nids_license_management_query)
        response_data = serializer.data

        return Response({"message_type": "success", "data": [response_data]})

    elif request.method == 'POST':
        plan_id = request.GET.get('activated_plan_id')
        isodatetime = datetime.now(pytz.timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')

        if not plan_id:
            return Response({"message_type": "d_not_f", "message": "plan_id_not_found"})

        try:
            updated_plan_details = Updated_Plan_Details.objects.get(id=plan_id)
        except Updated_Plan_Details.DoesNotExist:
            return Response({"message_type": "d_not_f", "message": "Plan not found"})

        random_key = str(uuid.uuid4())

        try:
            # Try to retrieve an existing Nids_License_Management record by updated_plan_id
            nids_license_management_query = Nids_License_Management.objects.get(updated_plan_id=updated_plan_details)
            serializer = NidsLicenseManagementSerializer(instance=nids_license_management_query, data=request.data)
        except Nids_License_Management.DoesNotExist:
            # If the Nids_License_Management record doesn't exist, insert a new row
            request_data = request.data.copy()
            request_data['created_at'] = isodatetime

            # Set sensor_create_count and sensor_active_count to the same value
            sensor_create_count = int(request.data.get("sensor_create_count", 0))
            request_data['sensor_create_count'] = sensor_create_count
            request_data['sensor_active_count'] = sensor_create_count

            request_data['updated_plan_id'] = updated_plan_details.id
            request_data['sensor_key'] = random_key

            # Modify sensor_name in request_data
            sensor_name_list = request.POST.getlist("sensor_name[]")
            if sensor_name_list == ['']:
                sensor_name_list = ""
            elif len(sensor_name_list) == 1:
                sensor_name_list = f"('{sensor_name_list[0]}')"  # Wrap single value in parentheses
            else:
                sensor_name_list = str(tuple(sensor_name_list))

            request_data['sensor_name'] = sensor_name_list

            serializer = NidsLicenseManagementSerializer(data=request_data)

        if serializer.is_valid():
            serializer.validated_data['updated_plan_id'] = updated_plan_details
            serializer.validated_data['updated_at'] = isodatetime
            serializer.save()
            api_logs_make(request, "updated nids license management details behalf of plan_id ",
                          "nids license management details upgrade")
            response_data = serializer.data
            response_msg = {"message_type": "success", "message": "Data was updated in db", "data": [response_data]}
        else:
            response_msg = {"message_type": "d_not_f", "message": "Data was not updated"}

        return Response(response_msg)

# to get api hids license management details on basis of plan_id
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def display_hids_license_management(request):
    if request.method == 'GET':
        plan_id = request.GET.get('activated_plan_id')
        isodatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')

        # Check if plan_id is None or empty
        if (plan_id is None) or (plan_id == "null"):
            return Response({"message_type": "d_not_f", "message": "plan_id_not_found"})
        random_key = str(uuid.uuid4())

        try:
            # Try to retrieve an existing Updated_Plan_Details record by plan_id
            updated_plan_details = Updated_Plan_Details.objects.get(id=plan_id)
        except Updated_Plan_Details.DoesNotExist:
            return Response({"message_type": "d_not_f", "message": "Plan not found"})

        # Now, you can create or update Hids_License_Management based on the fetched Updated_Plan_Details
        hids_license_management_query = Hids_License_Management.objects.filter(updated_plan_id=updated_plan_details)
        if hids_license_management_query.exists():
            serializer = HidsLicenseManagementSerializer(instance=hids_license_management_query, many=True)
            response_data = serializer.data
            response_msg = {"message_type": "success", "data": response_data}
        else:
            response_msg = {"message_type": "d_not_f", "message": "No data found for the provided plan_id"}

        return Response(response_msg)

    elif request.method == 'POST':
        plan_id = request.GET.get('activated_plan_id')
        isodatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')

        # Check if plan_id is None or empty
        if not plan_id:
            return Response({"message_type": "d_not_f", "message": "plan_id_not_found"})
        random_key = str(uuid.uuid4())

        try:
            # Try to retrieve an existing Updated_Plan_Details record by plan_id
            updated_plan_details = Updated_Plan_Details.objects.get(id=plan_id)
        except Updated_Plan_Details.DoesNotExist:
            return Response({"message_type": "d_not_f", "message": "Plan not found"})

        # Now, you can create or update Hids_License_Management based on the fetched Updated_Plan_Details
        hids_license_management_query = Hids_License_Management.objects.filter(updated_plan_id=updated_plan_details)
        
        if hids_license_management_query.exists():
            serializer = HidsLicenseManagementSerializer(instance=hids_license_management_query[0], data=request.data)
        else:
            request_data = request.data.copy()
            request_data['created_at'] = isodatetime
            request_data['sensor_create_count'] = int(request.data.get("sensor_create_count", 0))
            request_data['sensor_active_count'] = request_data['sensor_create_count']
            request_data['updated_plan_id'] = updated_plan_details.id
            request_data['sensor_key'] = random_key
            serializer = HidsLicenseManagementSerializer(data=request_data)

        if serializer.is_valid():
            serializer.validated_data['updated_plan_id'] = updated_plan_details
            serializer.validated_data['updated_at'] = isodatetime
            serializer.save()
            api_logs_make(request, "updated hids license management details behalf of plan_id ",
                          "hids license management details upgrade plan")
            response_data = serializer.data
            response_msg = {"message_type": "success", "message": "Data was updated in db", "data": [response_data]}
        else:
            response_msg = {"message_type": "d_not_f", "message": "Data was not updated"}

        return Response(response_msg)
    
# to get api soar sensor details on basis of plan_id
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def display_soar_license_management(request):

    if request.method == 'GET':
        plan_id = request.GET.get('activated_plan_id')
    elif request.method == 'POST':
        plan_id = request.GET.get('activated_plan_id')
     
    else:
        return Response({"message_type": "d_not_f", "message": "Invalid HTTP method"})

    isodatetime = datetime.now(pytz.timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')

    if (plan_id is None) or (plan_id == "null"):
        return Response({"message_type": "d_not_f", "message": "plan_id_not_found"})

    try:
        updated_plan_details = Updated_Plan_Details.objects.get(id=plan_id)
    except Updated_Plan_Details.DoesNotExist:
        return Response({"message_type": "d_not_f", "message": "Plan not found"})

    random_key = str(uuid.uuid4())

    if request.method == 'GET':
        try:
            # Try to retrieve an existing Soar_License_Management record by updated_plan_id
            soar_license_management_query = Soar_License_Management.objects.get(updated_plan_id=updated_plan_details)
            serializer = SoarSensorDetailsSerializer(instance=soar_license_management_query)
            response_msg = {
                "message_type": "success",
                "data": [serializer.data]
            }
        except Soar_License_Management.DoesNotExist:
            response_msg = {"message_type": "d_not_f", "message": "No data found for the provided plan_id"}
    elif request.method == 'POST':
        try:
            # Try to retrieve an existing Soar_License_Management record by updated_plan_id
            soar_license_management_query = Soar_License_Management.objects.get(updated_plan_id=updated_plan_details)
            serializer = SoarSensorDetailsSerializer(instance=soar_license_management_query, data=request.data)

            if serializer.is_valid():
                serializer.validated_data['updated_plan_id'] = updated_plan_details
                serializer.validated_data['updated_at'] = isodatetime
                serializer.save()
                api_logs_make(request, "updated soar license management details behalf of plan_id ",
                              "soar license management details")
                response_msg = {
                    "message_type": "success",
                    "message": "Data was updated in db",
                    "data": [serializer.data]
                }
            else:
                response_msg = {"message_type": "d_not_f", "message": "Data was not updated"}
        except Soar_License_Management.DoesNotExist:
            # If the Soar_License_Management record doesn't exist, insert a new row
            request_data = request.data.copy()
            request_data['created_at'] = isodatetime
            request_data['sensor_create_count'] = int(request.data.get("sensor_create_count", 0))
            request_data['sensor_active_count'] = request_data['sensor_create_count']
            request_data['updated_plan_id'] = updated_plan_details.id
            request_data['sensor_key'] = random_key
            serializer = SoarSensorDetailsSerializer(data=request_data)

            if serializer.is_valid():
                serializer.validated_data['updated_plan_id'] = updated_plan_details
                serializer.validated_data['updated_at'] = isodatetime
                serializer.save()
                api_logs_make(request, "updated soar license management details behalf of plan_id ",
                              "soar license management details")
                response_msg = {
                    "message_type": "success",
                    "message": "Data was inserted in db",
                    "data": [serializer.data]
                }
            else:
                response_msg = {"message_type": "d_not_f", "message": "Data was not inserted"}

    return Response(response_msg)

# get all agent details with license management details exesting location_id and org_id
@api_view(['GET'])
def display_all_agent(request):
    try: 
        query_client = Agent_data.objects.all()
        
        serializer_org_users = AllagentDetailsSerializer(query_client, many=True)
        serialized_data = serializer_org_users.data
        
        for agent_data in serialized_data:
            org_location_id = agent_data['org_location']
            organization_id = agent_data['organization_id']
            
            agent_data.setdefault('products', {})
            
            trace_license_man = Trace_License_Management.objects.filter(location_id=org_location_id, org_id=organization_id)
            if trace_license_man.exists():
                trace_data = TraceLicenseManagementSerializer(trace_license_man.first()).data
                agent_data["products"]["trace"] = trace_data
            else:
                agent_data["products"]["trace"] = {}
            
            hids_license_man = Hids_License_Management.objects.filter(location_id=org_location_id, org_id=organization_id)
            if hids_license_man.exists():
                hids_data = HidsLicenseManagementSerializer(hids_license_man.first()).data
                agent_data["products"]["hids"] = hids_data
            else:
                agent_data["products"]["hids"] = {}
            
            nids_license_man = Nids_License_Management.objects.filter(location_id=org_location_id, org_id=organization_id)
            if nids_license_man.exists():
                nids_data = NidsLicenseManagementSerializer(nids_license_man.first()).data
                agent_data["products"]["nids"] = nids_data
            else:
                agent_data["products"]["nids"] = {}

            soar_sensor_details = Soar_License_Management.objects.filter(location_id=org_location_id, org_id=organization_id)
            if soar_sensor_details.exists():
                soar_data = SoarSensorDetailsSerializer(soar_sensor_details.first()).data
                agent_data["products"]["soar"] = soar_data  
            else:
                agent_data["products"]["soar"] = {}      

            # working----------------
            # tps_agent_details = Soar_License_Management.objects.filter(location_id=org_location_id, org_id=organization_id)
            # if soar_sensor_details.exists():
            #     soar_data = SoarSensorDetailsSerializer(soar_sensor_details.first()).data
            #     agent_data["products"]["soar"] = soar_data  
            # else:
            #     agent_data["products"]["soar"] = {}  

            # tps_agent_details = Soar_License_Management.objects.filter(location_id=org_location_id, org_id=organization_id)
            # if soar_sensor_details.exists():
            #     soar_data = SoarSensorDetailsSerializer(soar_sensor_details.first()).data
            #     agent_data["products"]["soar"] = soar_data  
            # else:
            #     agent_data["products"]["soar"] = {} 

            # tps_agent_details = Soar_License_Management.objects.filter(location_id=org_location_id, org_id=organization_id)
            # if soar_sensor_details.exists():
            #     soar_data = SoarSensorDetailsSerializer(soar_sensor_details.first()).data
            #     agent_data["products"]["soar"] = soar_data  
            # else:
            #     agent_data["products"]["soar"] = {}  

            # tps_agent_details = Soar_License_Management.objects.filter(location_id=org_location_id, org_id=organization_id)
            # if soar_sensor_details.exists():
            #     soar_data = SoarSensorDetailsSerializer(soar_sensor_details.first()).data
            #     agent_data["products"]["soar"] = soar_data  
            # else:
            #     agent_data["products"]["soar"] = {} 

            # tps_agent_details = Soar_License_Management.objects.filter(location_id=org_location_id, org_id=organization_id)
            # if soar_sensor_details.exists():
            #     soar_data = SoarSensorDetailsSerializer(soar_sensor_details.first()).data
            #     agent_data["products"]["soar"] = soar_data  
            # else:
            #     agent_data["products"]["soar"] = {}  
             
            # tps_agent_details = Soar_License_Management.objects.filter(location_id=org_location_id, org_id=organization_id)
            # if soar_sensor_details.exists():
            #     soar_data = SoarSensorDetailsSerializer(soar_sensor_details.first()).data
            #     agent_data["products"]["soar"] = soar_data  
            # else:
            #     agent_data["products"]["soar"] = {}                                            
        
        result = {
            "message_type": "data_found",
            "data": serialized_data
        }
        
        return Response(result, status=status.HTTP_200_OK)
    
    except ObjectDoesNotExist:
        return Response({"message_type": "d_not_f"})

#To get client email id, admin email id for Health check sensor alert notification
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def display_hc_sensor_alert_email_config(request):
    location_id = request.GET.get("location_id")
    plan_id = request.GET.get('activated_plan_id')

    if (plan_id is None) or (plan_id == "null"):
        return Response({"message_type":"d_not_f", "errors":"plan_id_n_found"})

    if (location_id is None) or (location_id == "null"):
        return Response({"message_type":"d_not_f", "errors":"location_id_n_found"})
    try:       
        orm_query = Init_Configs.objects.filter(config_type = 'email_config_live', location_id = location_id, updated_plan_id = plan_id)
        
        if not orm_query:
            return Response({"message_type":"d_not_f"})
        
        serializer_var = HealthCheckSensorAlertEmailSerializer(orm_query,many = True)
        return Response({"message_type":"data_found","data":serializer_var.data})
    except ObjectDoesNotExist:
        return Response({"message_type":"d_not_f"}) 

# To add client email IDs, admin email IDs for Health check sensor alert notifications into DB
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def add_hc_sensor_alert_email_config(request):
    plan_id = request.POST.get('activated_plan_id')
    config_type = request.POST.get('config_type')
    location_id = request.POST.get('location_id')

    if config_type is None:
        return Response({"message_type":"unsuccessful", "message":"config_type_n_found"})
    
    if location_id is None:
        return Response({"message_type":"unsuccessful", "message":"location_id_n_found"})
    
    if plan_id is None:
        return Response({"message_type":"unsuccessful", "message":"plan_id_n_found"})
    
    client_email_id = request.data.getlist('client_emails[]')
    admin_email_id = request.data.getlist('admin_emails')
    jsonRes = []

    try:
        locationobj = Attach_Location.objects.get(id=location_id)
        InitConfigObj = Init_Configs.objects.get(location_id=locationobj, config_type=config_type, updated_plan_id = plan_id)

        InitConfigObj.sensor_alert_client = ','.join(str(item) for item in client_email_id)
        InitConfigObj.sensor_alert_admin = ','.join(str(item) for item in admin_email_id)
        InitConfigObj.save()
        api_logs_make(request, "To add client email IDs, admin for Health check sensor alert notifications into DB", "Health check sensor alert notifications into DB")

        jsonRes = {"message_type":"successfully_inserted","message": "Successfully inserted data in db"}

    except ObjectDoesNotExist:
        return Response({"message_type": "unsuccessful", "message": "object_n_found"})
    
    return Response(jsonRes)

# To add plan (Step-one)-- adds data to 'updated_plan_details' table
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def add_plan_step_one(request):
    response_msg = {}
    request.data._mutable = True
    isodatetime = datetime.now(pytz.timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')
    random_key = str(uuid.uuid4())
    request.data.update({"plan_creations_timestamp":isodatetime, "plan_key":random_key})
    serializervariable = AddPlanStepOneSerializer(data=request.data)
    if serializervariable.is_valid():
        serializervariable.save()
        api_logs_make(request,"updated plan add","new plan added in updated_plan_details")
        plan_id = serializervariable.data.get('id')
        
        response_msg = {"message_type":"successfully_inserted","message": "Successfully inserted data in db","plan_id":plan_id}
    else:
        response_msg = {"message_type":"unsuccessful","message": "Data was not inserted"}
        
    return Response(response_msg)

# To add plan (Step-two)-- adds data to 'updated_plan_details' table against 'plan_id' object created in step 1
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def add_plan_step_two(request):
    response_msg = {}
    plan_id = request.data.get('plan_id')
    
    if plan_id is None:
        return Response({"message_type":"unsuccessful","message": "plan_id_not_found"})

    try:
        UpdatedPlanObj = Updated_Plan_Details.objects.filter(id=plan_id).first()
        serializervariable = AddPlanStepTwoSerializer(UpdatedPlanObj, data=request.data)
        if serializervariable.is_valid():
            serializervariable.save()
            api_logs_make(request,"To add plan (step-2 section)","plan_id object created in step 1")
            response_msg = {"message_type":"successfully_inserted","message": "Successfully inserted data in db", "plan_id":plan_id}
        else:
            response_msg = {"message_type":"unsuccessful","message": "Data was not inserted", "err":serializervariable.errors}
    except Updated_Plan_Details.DoesNotExist:
        response_msg = {"message_type":"unsuccessful","message": "object_n_found"}
    
    return Response(response_msg)


# To add plan (Step-three)-- adds data to 'trace_license_management' table against 'plan_id' object created in step 1
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def add_trace_license_plan_step_three(request):
    response_msg = {}
    request.data._mutable = True
    plan_id = request.data.get('plan_id')
    if plan_id is None:
        return Response({"message_type":"unsuccessful","message": "plan_id_not_found"})

    # altering some fields to store in database
    sensor_name_list = request.data.getlist("sensor_name[]")
    
    if sensor_name_list == ['']:
        sensor_name_list = ""
    elif len(sensor_name_list) == 1:
        sensor_name_list = f"('{sensor_name_list[0]}')"  # Wrap single value in parentheses
    else:
        sensor_name_list = str(tuple(sensor_name_list))

    random_key = str(uuid.uuid4())
    isodatetime = datetime.now(pytz.timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')
    sensor_create_count = int(request.data.get("sensor_create_count", 0))
    sensor_active_count = sensor_create_count
    
    # updating altered fields to request.data
    request.data.update({"created_at":isodatetime, "sensor_create_count":sensor_create_count, "sensor_active_count":sensor_active_count, "sensor_key":random_key, "updated_plan_id": plan_id, "sensor_name":sensor_name_list})

    serializervariable = AddTraceLicensePlanStepThreeSerializer(data=request.data)
    if serializervariable.is_valid():
        serializervariable.save()
        api_logs_make(request,"Add trace license management details", "new trace license management added")
        response_msg = {"message_type":"successfully_inserted","message": "Successfully inserted data in db"}
    else:
        response_msg = {"message_type":"unsuccessful","message": "Data was not inserted"}
        
    return Response(response_msg)

# To add plan (Step-three)-- adds data to 'nids_license_management' table against 'plan_id' object created in step 1
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def add_nids_license_plan_step_three(request):
    response_msg = {}
    request.data._mutable = True
    plan_id = request.data.get('plan_id')
    
    if plan_id is None:
        return Response({"message_type":"unsuccessful","message": "plan_id_not_found"})
    
    random_key = str(uuid.uuid4())
    isodatetime = datetime.now(pytz.timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')
    sensor_create_count = int(request.data.get("sensor_create_count", 0))
    sensor_active_count = sensor_create_count

    # updating altered fields to request.data
    request.data.update({"created_at":isodatetime, "sensor_create_count":sensor_create_count, "sensor_active_count":sensor_active_count, "updated_plan_id": plan_id, "sensor_key":random_key})

    serializervariable = AddNidsLicensePlanStepThreeSerializer(data=request.data)
    if serializervariable.is_valid():
        serializervariable.save()
        api_logs_make(request, "Add nids license management details", "new nids license management added")
        response_msg = {"message_type":"successfully_inserted","message": "Successfully inserted data in db"}
    else:
        response_msg = {"message_type":"unsuccessful","message": "Data was not inserted"}
        
    return Response(response_msg)

# To add plan (Step-three)-- adds data to 'hids_license_management' table against 'plan_id' object created in step 1
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def add_hids_license_plan_step_three(request):
    response_msg = {}
    request.data._mutable = True
    plan_id = request.data.get('plan_id')
    
    if plan_id is None:
        return Response({"message_type":"unsuccessful","message": "plan_id_not_found"})
    
    random_key = str(uuid.uuid4())
    isodatetime = datetime.now(pytz.timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')
    sensor_create_count = int(request.data.get("sensor_create_count", 0))
    sensor_active_count = sensor_create_count

    # updating altered fields to request.data
    request.data.update({"created_at":isodatetime, "sensor_create_count":sensor_create_count, "sensor_active_count":sensor_active_count, "updated_plan_id": plan_id, "sensor_key":random_key})

    serializervariable = AddHidsLicensePlanStepThreeSerializer(data=request.data)
    if serializervariable.is_valid():
        serializervariable.save()
        api_logs_make(request, "Add hids license management details", "new hids license management added")
        response_msg = {"message_type":"successfully_inserted","message": "Successfully inserted data in db"}
    else:
        response_msg = {"message_type":"unsuccessful","message": "Data was not inserted"}
        
    return Response(response_msg)

# To add plan (Step-three)-- adds data to 'soar_license_management' table against 'plan_id' object created in step 1
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def add_soar_license_plan_step_three(request):
    response_msg = {}
    request.data._mutable = True
    plan_id = request.data.get('plan_id')
    
    if plan_id is None:
        return Response({"message_type":"unsuccessful","message": "plan_id_not_found"})
    
    random_key = str(uuid.uuid4())
    isodatetime = datetime.now(pytz.timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')
    sensor_create_count = int(request.data.get("sensor_create_count", 0))
    sensor_active_count = sensor_create_count

    # updating altered fields to request.data
    request.data.update({"created_at":isodatetime, "sensor_create_count":sensor_create_count, "sensor_active_count":sensor_active_count, "updated_plan_id": plan_id, "sensor_key":random_key})

    serializervariable = AddSoarLicensePlanStepThreeSerializer(data=request.data)
    if serializervariable.is_valid():
        serializervariable.save()
        api_logs_make(request, "Add soar license management details", "new soar license management added")
        response_msg = {"message_type":"successfully_inserted","message": "Successfully inserted data in db"}
    else:
        response_msg = {"message_type":"unsuccessful","message": "Data was not inserted"}
        
    return Response(response_msg)

# Get all objects of Updated Plan table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def display_all_updated_plan(request):
    queryset = Updated_Plan_Details.objects.all()
    serializer = DisplayUpdatedPlanSerializer(queryset, many=True)
    return Response({"message_type": "success","data":serializer.data})

# Get single object of Updated Plan table on basis of id
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def display_id_wise_updated_plan(request, pk):
    try:
        PlanIdObj = Updated_Plan_Details.objects.filter(id = pk).first()
        serializer = DisplayUpdatedPlanSerializer(PlanIdObj)
        response_dict = serializer.data

        # trace
        TraceLicenseObj = Trace_License_Management.objects.filter(updated_plan_id = PlanIdObj).first()
        trace_license_ser = DisplayTraceLicenseSerializer(TraceLicenseObj)
        response_dict['trace_license_management'] = trace_license_ser.data

        # nids
        NidsLicenseObj = Nids_License_Management.objects.filter(updated_plan_id = PlanIdObj).first()
        nids_license_ser = DisplayNidsLicenseSerializer(NidsLicenseObj)
        response_dict['nids_license_management'] = nids_license_ser.data

        # hids
        HidsLicenseObj = Hids_License_Management.objects.filter(updated_plan_id = PlanIdObj).first()
        hids_license_ser = DisplayHidsLicenseSerializer(HidsLicenseObj)
        response_dict['hids_license_management'] = hids_license_ser.data

        # soar
        SoarLicenseObj = Soar_License_Management.objects.filter(updated_plan_id = PlanIdObj).first()
        soar_license_ser = DisplaySoarLicenseSerializer(SoarLicenseObj)
        response_dict['soar_license_management'] = soar_license_ser.data
        
        return Response({"message_type": "success","data":response_dict})
    except ObjectDoesNotExist:
        return Response({"message_type":"d_not_f"})

# To dcrease count from sensor_active_count in license management details models
class DecreaseLicenseCount(APIView):
    def post(self, request):
        sensor_key = request.headers.get('sensorkey')
        decrease_count = request.headers.get('deccount')
        increment_count = request.headers.get('inccount')
        if decrease_count is not None and increment_count is not None:
            return Response({"message_type": "validation_error", "message": "Both deccount and inccount cannot be provided at the same time"})
        elif decrease_count is None and increment_count is None:
            return Response({"message_type": "validation_error", "message": "Please provide either deccount or inccount"})

        if (decrease_count is not None and int(decrease_count) <= 0):
            return Response({"message_type": "decrement count is not greater than 0", "message": "decrement count should be greater than 0"})

        if (increment_count is not None and int(increment_count) <= 0):
            return Response({"message_type": "increment count is not greater than 0", "message": "increment count should be greater than 0"})

        if not sensor_key:
            return Response({"message_type": "validation_error", "message": "Please provide sensorkey, deccount, or inccount"})
        try:
            decrease_count = int(decrease_count) if decrease_count else 0
            increment_count = int(increment_count) if increment_count else 0
        except ValueError:
            return Response({"message_type": "validation_error", "message": "Invalid deccount or inccount, must be integers"})

        # Create a dictionary to map license types to their corresponding models and serializers
        license_data = {
            "NIDS": {"model": Nids_License_Management, "serializer": DecreaseNidsLicenseManagementSerializer},
            "TRACE": {"model": Trace_License_Management, "serializer": DecreaseTraceLicenseManagementSerializer},
            "HIDS": {"model": Hids_License_Management, "serializer": DecreaseHidsLicenseManagementSerializer},
            "SOAR": {"model": Soar_License_Management, "serializer": DecreaseSoarLicenseManagementSerializer},
        }

        response_data = {}  # Initialize an empty response dictionary

        for license_type, data in license_data.items():
            model = data["model"]
            serializer_class = data["serializer"]
            try:
                license = model.objects.get(sensor_key=sensor_key)
                try:
                    location_query = Attach_Location.objects.filter(activated_plan_id=license.updated_plan_id.id).first()  # Use filter and first() to handle missing Attach_Location

                    if location_query:
                        org_id_val = location_query.org_id
                        org_name = org_id_val.organization_id
                        branch_code = location_query.branchcode
                        org_query = Organization_data.objects.get(organization_id=org_name)
                        org_name_val = org_query.organization_name.lower()[:3]
                        company_index_name_Val = org_name_val + '-' + branch_code

                        create_count = int(license.sensor_create_count)  # Get the sensor_create_count

                        if decrease_count != 0:
                            # Perform a decrement operation
                            if decrease_count <= 0:
                                response_data[license_type] = {"message": f"Invalid decrease count for {license_type}"}
                            elif int(license.sensor_active_count) == 0:
                                response_data[license_type] = {"message": f"{license_type} sensor_active_count has expired"}
                            else:
                                active_count = int(license.sensor_active_count) - decrease_count
                                if active_count >= 0:
                                    license.sensor_active_count = str(active_count)
                                    license.save()
                                    if active_count == 0:
                                        response_data[license_type] = {
                                            "message": f"{license_type} sensor_active_count has expired"
                                        }
                                    else:
                                        serializer = serializer_class(license)
                                        # Serialize the entire license object and add company_index_name
                                        serialized_data = serializer.data
                                        if 'registry_address' in serialized_data:
                                            serialized_data['registry_server'] = serialized_data.pop('registry_address')
                                            serialized_data['xdr_default_region'] = serialized_data.pop('aws_default_region')

                                        serialized_data["company_index_name"] = company_index_name_Val
                                        response_data[license_type] = serialized_data

                        elif increment_count != 0:
                            # Perform an increment operation
                            if increment_count <= 0:
                                response_data[license_type] = {"message": f"Invalid increment count for {license_type}"}
                            else:
                                active_count = int(license.sensor_active_count) + increment_count
                                if active_count <= create_count:
                                    license.sensor_active_count = str(active_count)
                                    license.save()
                                    serializer = serializer_class(license)
                                    # Serialize the entire license object and add company_index_name
                                    serialized_data = serializer.data
                                    if 'registry_address' in serialized_data:
                                        serialized_data['registry_server'] = serialized_data.pop('registry_address')
                                        serialized_data['xdr_default_region'] = serialized_data.pop('aws_default_region')

                                    serialized_data["company_index_name"] = company_index_name_Val
                                    response_data[license_type] = serialized_data
                                else:
                                    response_data[license_type] = {"message": f"active_count is not greater from create_count"}

                    else:
                        # Attach_Location record not found for this license type
                        response_data[license_type] = {"message": f"The license of the plan id is not active any more"} # for making company index name used

                except ObjectDoesNotExist:
                    # Attach_Location record does not exist for this license type
                    response_data[license_type] = {"message": f"The license of the plan id is not active any more"}

            except model.DoesNotExist:
                # Sensor key does not exist for this license type, so we don't add it to response_data
                pass

        if not response_data:
            return Response({"message": "Data not found"}, status=status.HTTP_404_NOT_FOUND)
            
        return Response(response_data)



# # if check license_active_count is always = current_count then will display data if is it equal then then display
@api_view(['GET'])
def get_license_management_details_with_logs_indices_env(request):
    try:
        sensor_key = request.GET.get("sensor_key")  # Check if sensor_key is provided
        plan_key = request.GET.get("plan_key")
        if not sensor_key and not plan_key:
            return Response({"message_type": "validation_error", "message": "Please provide either sensor_key or plan_id"})


        if sensor_key:
            env_types = [
                ("env_hids", AlldataAgentPermissionsSerializer, Hids_License_Management),
                ("env_nids", NidsAlldataAgentPermissionsSerializer, Nids_License_Management),
                ("env_soar", SoarAlldataAgentPermissionsSerializer, Soar_License_Management),
                ("env_trace", TraceAlldataAgentPermissionsSerializer, Trace_License_Management),
                # Add other environment types here
            ]

            # Initialize the data dictionary
            data = {
                "message_type": "data_found",
                "data": []
            }

            # Loop through the environment types
            for env_type, serializer_class, license_model in env_types:
                # Query license management details for the provided sensor_key and environment type
                license_management_data = license_model.objects.filter(sensor_key=sensor_key).values().first()
                product_name = env_type.replace("env_", "").upper()
                if plan_key:  # Change plan_id to plan_key
            # Get the plan details based on plan_key
                    plan_details = Updated_Plan_Details.objects.get(plan_key=plan_key)
                    license_management_data = license_model.objects.filter(
                        updated_plan_id=plan_details
                    ).values().first()


                if license_management_data:
                    license_management_data.pop('company_index_name', None)
                    plan_details = Updated_Plan_Details.objects.get(id=license_management_data['updated_plan_id_id'])
                    location_query = Attach_Location.objects.get(activated_plan_id=plan_details)
                    org_id_val = location_query.org_id
                    org_name = org_id_val.organization_name
                    branch_code = location_query.branchcode
                    org_name_val = org_name.lower()[:3]
                    company_index_name_Val = org_name_val + '-' + branch_code
                    license_management_data['company_index_name'] = company_index_name_Val

                    # Retrieve log names for the environment type
                    indices_data = []  # Store log names for the environment type
                    agent_query = Agent_data.objects.filter(updated_plan_id=plan_details)
                    for agent_data in agent_query:
                        serializer_class = serializer_class  # Use the appropriate serializer class
                        serializer = serializer_class(agent_data)
                        column_values = serializer.data.values()
                        valid_values = [value for value in column_values if value is not None and value != "null"]
                        indices_data.extend(valid_values)

                    license_management_data.pop('updated_plan_id_id', None)
                    # Create a dictionary for the environment type
                    env_data = {
                        env_type: True,
                        f"{env_type}_data": {
                            "indice_data": indices_data,
                            "license_management": license_management_data
                        }
                    }

                    data["data"].append(
                        {
                            "plan_id": plan_details.id,
                            "plan_name": plan_details.plan_name,
                            "plan_description": plan_details.plan_descriptions,
                            "products": [env_data]
                        }
                    )
                    product_data = {
                            product_name: env_data
                        }

                    data["data"][0]["products"] = product_data

            if not data["data"]:
                return Response({"message_type": "data_not_found", "message": "No data found for the provided sensor_key"})

            return Response(data)
        company_index_name = "Default-Value"
        if plan_key:  # Change plan_id to plan_key
            plan_details = Updated_Plan_Details.objects.get(plan_key=plan_key)  # Change plan_id to plan_key
            # print(F"plan_details: {plan_details.id}")
            data = {
                "message_type": "data_found",
                "data": [
                    {
                        "id": plan_details.id,
                        "plan_name": plan_details.plan_name,
                        "plan_description": plan_details.plan_descriptions,
                        "products": {}  # Initialize as a dictionary
                    }
                ]
            }

            # Retrieve the page permissions based on the plan_id
            page_permissions = Page_Permissions.objects.filter(updated_plan_id=plan_details)
            location_query = Attach_Location.objects.get(activated_plan_id=plan_details)
            org_id_val = location_query.org_id
            org_name = org_id_val.organization_name
            branch_code = location_query.branchcode
            org_name_val = org_name.lower()[:3]
            company_index_name = org_name_val + '-' + branch_code
            # print(f"page_permissions: {page_permissions}")

            # Define a list of environment types and their corresponding serializers and license models
            env_types = [
                ("env_hids", AlldataAgentPermissionsSerializer, Hids_License_Management),
                ("env_nids", NidsAlldataAgentPermissionsSerializer, Nids_License_Management),
                ("env_soar", SoarAlldataAgentPermissionsSerializer, Soar_License_Management),
                ("env_trace", TraceAlldataAgentPermissionsSerializer, Trace_License_Management),
                ("env_wazuh", WazuhAlldataAgentPermissionsSerializer, None),
                ("env_hc", HealthCheckAlldataAgentPermissionsSerializer, None),
                ("env_ess", EssAgentAlldataAgentPermissionsSerializer, None),
                ("env_tps", TpsAgentAlldataAgentPermissionsSerializer, None),
                ("env_sbs", SbsAgentAlldataAgentPermissionsSerializer, None),
                ("env_tptf", TptfAgentAlldataAgentPermissionsSerializer, None),
                ("env_mm", MmAgentAlldataAgentPermissionsSerializer, None),
            ]

            for env_type, serializer_class, license_model in env_types:
                # Check if the environment type is True in the Page_Permissions model
                if page_permissions.filter(**{env_type: True}).exists():
                    # Capitalize the product name
                    product_name = env_type.replace("env_", "").upper()

                    # Retrieve log names for the environment type
                    indices_data = []  # Store log names for the environment type
                    agent_query = Agent_data.objects.filter(updated_plan_id=plan_details.id)
                    # print(f"agent_query: {agent_query}, indices_data: {indices_data}")
                    for agent_data in agent_query:
                        serializer = serializer_class(agent_data)
                        column_values = serializer.data.values()
                        valid_values = [value for value in column_values if value is not None and value != "null"]
                        indices_data.extend(valid_values)

                    # Initialize the license management data to an empty dictionary
                    license_management_data = {}

                    # Check if a license model is defined for the environment type
                    if license_model:
                        # Query license management details for the environment type
                        license_management_data = license_model.objects.filter(
                            updated_plan_id=plan_details.id,
                        ).values().first()
                        # location_query = Attach_Location.objects.get(activated_plan_id=plan_details)
                        # org_id_val = location_query.org_id
                        # org_name = org_id_val.organization_name
                        # branch_code = location_query.branchcode
                        # org_name_val = org_name.lower()[:3]
                        # company_index_name_Val = org_name_val + '-' + branch_code
                        # license_management_data['company_index_name'] = company_index_name_Val
                    # Create a dictionary for the environment type
                    env_data = {
                        env_type: True,
                        f"{env_type}_data": {
                            "indice_data": indices_data,
                            "license_management": license_management_data
                        }
                    }

                    # Update the data dictionary with the capitalized product name
                    data["data"][0]["products"][product_name] = env_data
                data["data"][0]["company_index_name"] = company_index_name
   

            return Response(data)

            # return Response(data)

    except Updated_Plan_Details.DoesNotExist:
        return Response({"message_type": "plan_not_found", "message": "Plan not found for the provided plan_id"})
    except Exception as e:
        return Response({"message_type": "error", "message": str(e)})

    except Updated_Plan_Details.DoesNotExist:
        return JsonResponse({"message_type": "plan_not_found", "message": "Plan not found for the provided sensor_key or plan_key"})
    except Exception as e:
        return JsonResponse({"message_type": "error", "message": str(e)})


# Get decreament count details api
license_data = {
    "NIDS": {
        "model": Nids_License_Management,
        "serializer": DecreaseNidsLicenseManagementSerializer,
    },
    "TRACE": {
        "model": Trace_License_Management,
        "serializer": DecreaseTraceLicenseManagementSerializer,
    },
    "HIDS": {
        "model": Hids_License_Management,
        "serializer": DecreaseHidsLicenseManagementSerializer,
    },
    "SOAR": {
        "model": Soar_License_Management,
        "serializer": DecreaseSoarLicenseManagementSerializer,
    },
}
class GetMultipleLicenseData(APIView):
    def get(self, request):
        sensor_key = request.headers.get('sensorkey')
        response_data = {}  # Initialize an empty response dictionary
        if sensor_key is None:
            return Response({"message_type": "sensor_key is missing", "message": "sensor_key_not_found"})
        
        for license_type, data in license_data.items():
            model = data["model"]
            serializer_class = data["serializer"]

            try:
                license = model.objects.get(sensor_key=sensor_key)
                
                try:
                    location_query = Attach_Location.objects.get(activated_plan_id=license.updated_plan_id.id)
                    org_id_val = location_query.org_id
                    org_name = org_id_val.organization_id
                    branch_code = location_query.branchcode
                    org_query = Organization_data.objects.get(organization_id=org_name)
                    org_name_val = org_query.organization_name.lower()[:3]
                    company_index_name_Val = org_name_val + '-' + branch_code
                  
                    if int(license.sensor_active_count) >= 0:
                        # Serialize the license data
                        serializer_data = serializer_class(license).data

                        # Rename the 'registry_address' field to 'registry_server' in the data dictionary
                        if 'registry_address' in serializer_data:
                            serializer_data['registry_server'] = serializer_data.pop('registry_address')
                            serializer_data['xdr_default_region'] = serializer_data.pop('aws_default_region')
                        serializer_data["company_index_name"] = company_index_name_Val
                        response_data[license_type] = serializer_data
                    else:
                        response_data[license_type] = {
                            "message": f"{license_type} sensor_active_count has expired"
                        }
                except Attach_Location.DoesNotExist:
                    # Attach_Location record does not exist for this license type
                    response_data[license_type] = {"message": f"The license of the plan id is not active any more"} # for making runtime company index name used
            except model.DoesNotExist:
                # Sensor key does not exist for this license type, so we don't add it to response_data
                pass

        # If no data was found for any license type, return a message
        if not response_data:
            return Response({"message": "Data not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(response_data)



# upgrade plan (for table nme: "updated_plan_details")
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def upgrade_plan(request):
    response_msg = {}
    plan_id = request.data.get('plan_id') # plan_id which we need to update
    location_id = request.GET.get('location_id') # location_id against which we need to update the plan_id
    
    if plan_id is None:
        return Response({"message_type":"unsuccessful","message": "plan_id_not_found"})
    
    if location_id is None:
        return Response({"message_type":"unsuccessful","message": "location_id_not_found"})

    # updation of new plan_id would be done in 5 tables: Attach_Location, Page_Permissions, Agent_data, Init_Configs, blacklisted_data
    try:
        with transaction.atomic():

            UpdatedPlanObj = Updated_Plan_Details.objects.get(id = plan_id)
            LocationObj = Attach_Location.objects.get(id = location_id)

            # plan would not be upgraded to the given plan if it is already active for any other location
            plan_exists_in_location_table = Attach_Location.objects.filter(activated_plan_id = UpdatedPlanObj).exists()
            # print(f"plan_exists_in_location_table:{plan_exists_in_location_table}")

            if plan_exists_in_location_table:
                return Response({"message_type":"unsuccessful","message": "plan_is_active_on_another_location"})
            else:
                current_plan_id = LocationObj.activated_plan_id #16
                previous_plan_id = LocationObj.deactivated_plan_id #14

                if current_plan_id is not None:
                    if current_plan_id.id == int(plan_id):
                        return Response({"message_type":"success","message": " given_plan_id_is_already_activated"})
                
                # updating plan_id in location table
                if current_plan_id is None:
                    LocationObj.activated_plan_id = UpdatedPlanObj
                else:
                    activated_plan_id_str = str(LocationObj.activated_plan_id.id)

                    if (previous_plan_id.strip() == "") or (previous_plan_id is None): #deactivated_plan_id is blank 
                        LocationObj.deactivated_plan_id = activated_plan_id_str
                        LocationObj.activated_plan_id = UpdatedPlanObj
                    else: #deactivated_plan_id already contain some plan_id
                        previous_plan_id_wo_brackets = previous_plan_id.strip("()").split(",")  # Extract existing values
                        previous_plan_id_wo_brackets.append(activated_plan_id_str)
                        
                        LocationObj.deactivated_plan_id = "({})".format(",".join(previous_plan_id_wo_brackets))
                        LocationObj.activated_plan_id = UpdatedPlanObj
                LocationObj.save()
                
                # updating plan_id in page_permission table
                PagePermissionsObj = Page_Permissions.objects.get(location_id = LocationObj)

                # updating other columns in page_permission table
                # source_object = UpdatedPlanObj is given to setattr ,  target_object = PagePermissionsObj is given to getattr
                # List of column names to update
                columns_to_update = ['env_trace', 'env_wazuh', 'env_hids', 'env_nids', 'env_soar', 'env_tps', 'env_ess', 'env_sbs', 'env_tptf', 'env_mm', 'env_hc', 'xdr_live_map', 'default_page']

                # Use a list comprehension to update the target object attributes
                [setattr(PagePermissionsObj, column_name, getattr(UpdatedPlanObj, column_name)) for column_name in columns_to_update]

                PagePermissionsObj.updated_plan_id = UpdatedPlanObj
                PagePermissionsObj.save()

                # updating plan_id in agent table
                AgentDataObj = Agent_data.objects.get(org_location = LocationObj)
                AgentDataObj.updated_plan_id = UpdatedPlanObj
                AgentDataObj.save()
                api_logs_make(request, "upgrade plan_id", "updated plan details")
                # updating plan_id in init_config table
                filter_loc_id = Init_Configs.objects.filter(location_id = LocationObj)
                if filter_loc_id.exists():
                    filter_loc_id.update(updated_plan_id = UpdatedPlanObj)
                else:
                    return Response({"message_type":"unsuccessful","message": "location_id_n_found_init_config_table"})
                
                # updating plan_id in blacklisted table
                blacklisted_data.objects.filter(location_id = LocationObj).update(updated_plan_id = UpdatedPlanObj)

                response_msg = {"message_type":"success","message":"Successfully upgraded plan"}
    # except ObjectDoesNotExist:
    except (Updated_Plan_Details.DoesNotExist, Attach_Location.DoesNotExist, Page_Permissions.DoesNotExist, Agent_data.DoesNotExist, Init_Configs.DoesNotExist) as e:

        exception_response_mapping = {
        Updated_Plan_Details.DoesNotExist: "loc_id_n_found_in_updated_plan_details",
        Attach_Location.DoesNotExist: "loc_id_n_found_in_attach_location",
        Page_Permissions.DoesNotExist: "loc_id_n_found_in_page_permissions",
        Agent_data.DoesNotExist: "loc_id_n_found_in_agent_data",
        Init_Configs.DoesNotExist: "loc_id_n_found_in_init_config"
        }

        # Get the custom response based on the exception type
        model_exception = exception_response_mapping.get(type(e), "Unknown exception")
        response_msg = {"message_type":"unsuccessful","message": model_exception}
    
    except Exception:
        response_msg = {"message_type":"unsuccessful","message": "exception_raised"}

    return Response(response_msg)

# get plans not active on any location
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def get_all_plans_not_active_on_any_location(request):
    try:
        db_query = Attach_Location.objects.values_list('activated_plan_id', flat=True)
        plans_active_on_location_list = list(set(db_query))

        inactive_plans_id_query = Updated_Plan_Details.objects.exclude(id__in = plans_active_on_location_list)
        
        if not inactive_plans_id_query.exists():
            return Response({"message_type": "d_not_f", "message": "no_inactive_plan_found_currently"})

        ser_var = DisplayUpdatedPlanSerializer(inactive_plans_id_query, many = True)
        
        response_msg = {"message_type": "success","data":ser_var.data}
    except Exception:
        response_msg = {"message_type": "d_not_f"}
    return Response(response_msg)

# get id wise plan which are not active on any location
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def get_single_plan_not_active_on_any_location(request, pk):
    try:
        PlanIdObj = Updated_Plan_Details.objects.filter(id = pk).first()
        if not PlanIdObj:
            return Response({"message_type": "d_not_f", "message": "data_n_found_for_plan_id"})
        ser_var = DisplayUpdatedPlanSerializer(PlanIdObj)
        
        response_msg = {"message_type": "success","data":ser_var.data}
    except Exception:
        response_msg = {"message_type": "d_not_f"}
    return Response(response_msg)

# Update api plan2 details (upgrade section) plan2_update_details
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def plan2_update_details(request):
    response_msg = {}
    request.data._mutable = True
    plan_id = request.data.get('plan_id')
    isodatetime = datetime.now(pytz.timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')
    
    if plan_id is None:
        return Response({"message_type":"unsuccessful","message": "plan_id_not_found"})
    try:
        plan2_query = Updated_Plan_Details.objects.get(id=plan_id)
    except Updated_Plan_Details.DoesNotExist:
        return Response({"message_type": "unsuccessful", "message": "Plan not found"})
    serializervariable = Plan2DetailsSerializer(instance=plan2_query, data=request.data)
    if serializervariable.is_valid():
        serializervariable.validated_data['plan_updations_timestamp'] = isodatetime
        serializervariable.save()
        api_logs_make(request, "Updated Plan2 details", "updated plan2 details")
        response_msg = {"message_type":"updated_successfully","message": "updated successfully data in db"}
    else:
        response_msg = {"message_type":"unsuccessful","message": "Data was not inserted"}
        
    return Response(response_msg)

#  Update api plan2 plan details (upgrade section plan2) pruduct_update_details_plan2
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def pruduct_update_details_plan2(request):
    response_msg = {}
    plan_id = request.data.get('plan_id')
    isodatetime = datetime.now(pytz.timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')
    if plan_id is None:
        return Response({"message_type":"unsuccessful","message": "plan_id_not_found"})
    try:
        plan_env_query = Updated_Plan_Details.objects.get(id = plan_id)
    except Updated_Plan_Details.DoesNotExist:
        return Response({"message_type": "unsuccessful", "message": "Plan not found"})
    serializer = UpgradePlan2teLocationSerializer(instance=plan_env_query,data=request.data)
    if serializer.is_valid():
        serializer.validated_data['plan_updations_timestamp'] = isodatetime
        serializer.save()
        api_logs_make(request, "updated plan2 plan env behalf of plan_id ", "updated plan2 plan env behalf of plan_id")
        response_msg = {"message_type": "updated_successfully", "message": "updated successfully data in db"}
    else:
        response_msg = {"message_type":"unsuccessful","message": "Data was not inserted"}
        
    return Response(response_msg)


# Update api plan2 trace_license_management details (upgrade section plan2) trace_license_management_update_details_plan2
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def trace_license_management_update_details_plan2(request):
    response_msg = {}
    plan_id = request.GET.get('plan_id')
    isodatetime = datetime.now(pytz.timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')
    
    if plan_id is None:
        return Response({"message_type": "unsuccessful", "message": "plan_id_not_found"})
    
    # Update altered fields to request.data
    sensor_name_list = request.POST.getlist("sensor_name[]")
    if sensor_name_list == ['']:
        sensor_name_list = ""
    elif len(sensor_name_list) == 1:
        sensor_name_list = f"('{sensor_name_list[0]}')"  # Wrap single value in parentheses
    else:
        sensor_name_list = str(tuple(sensor_name_list))
    
    try:
        # Try to retrieve an existing Updated_Plan_Details record by plan_id
        updated_plan_details = Updated_Plan_Details.objects.get(id=plan_id)
    except Updated_Plan_Details.DoesNotExist:
        return Response({"message_type": "unsuccessful", "message": "Plan not found"})
    
    random_key = str(uuid.uuid4())
    
    try:
        # Try to retrieve an existing Trace_License_Management record by updated_plan_id
        trace_license_management_query = Trace_License_Management.objects.get(updated_plan_id=updated_plan_details)
        serializer = UpgradeTraceLicensePlanStepThreeSerializer(instance=trace_license_management_query, data=request.data)
    except Trace_License_Management.DoesNotExist:
        # If the Trace_License_Management record doesn't exist, insert a new row
        request_data = request.data.copy()
        request_data['created_at'] = isodatetime
        request_data['sensor_create_count'] = int(request.data.get("sensor_create_count", 0))
        request_data['sensor_active_count'] = request_data['sensor_create_count']
        request_data['updated_plan_id'] = updated_plan_details.id
        request_data['sensor_key'] = random_key
        request_data['sensor_name'] = sensor_name_list
        serializer = UpgradeTraceLicensePlanStepThreeSerializer(data=request_data)
    
    if serializer.is_valid():
        serializer.validated_data['updated_plan_id'] = updated_plan_details
        serializer.validated_data['updated_at'] = isodatetime
        serializer.validated_data['sensor_name'] = sensor_name_list
        serializer.save()
        api_logs_make(request, "updated plan2 trace license management details behalf of plan_id ",
                      "trace license management details upgrade plan2")
        response_msg = {"message_type": "updated_successfully", "message": "Data was updated in db"}
    else:
        response_msg = {"message_type": "unsuccessful", "message": "Data was not updated"}
    
    return Response(response_msg)


#  Update api plan2 nids license management details (upgrade section plan2) nids_license_management_update_details_plan2
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def nids_license_management_update_details_plan2(request):
    response_msg = {}
    plan_id = request.GET.get('plan_id')
    isodatetime = datetime.now(pytz.timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')
    if not plan_id:
        return Response({"message_type": "unsuccessful", "message": "plan_id_not_found"})

    try:
        updated_plan_details = Updated_Plan_Details.objects.get(id=plan_id)
    except Updated_Plan_Details.DoesNotExist:
        return Response({"message_type": "unsuccessful", "message": "Plan not found"})
    random_key = str(uuid.uuid4())

    try:
        # Try to retrieve an existing Soar_License_Management record by updated_plan_id
        soar_license_management_query = Nids_License_Management.objects.get(updated_plan_id=updated_plan_details)
        serializer = UpgradeNidsLicensePlanStepThreeSerializer(instance=soar_license_management_query, data=request.data)
    except Nids_License_Management.DoesNotExist:
        # If the Soar_License_Management record doesn't exist, insert a new row
        request_data = request.data.copy()
        request_data['created_at'] = isodatetime
        request_data['sensor_create_count'] = int(request.data.get("sensor_create_count", 0))
        request_data['sensor_active_count'] = request_data['sensor_create_count']
        request_data['updated_plan_id'] = updated_plan_details.id
        request_data['sensor_key'] = random_key
        serializer = UpgradeNidsLicensePlanStepThreeSerializer(data=request_data)

    if serializer.is_valid():
        serializer.validated_data['updated_plan_id'] = updated_plan_details
        serializer.validated_data['updated_at'] = isodatetime
        serializer.save()
        api_logs_make(request, "updated plan2 soar license management details behalf of plan_id ",
                      "soar license management details upgrade plan2")
        response_msg = {"message_type": "updated_successfully", "message": "Data was updated in db"}
    else:
        response_msg = {"message_type": "unsuccessful", "message": "Data was not updated"}

    return Response(response_msg)


#  Update api plan2 hids license management details (upgrade section plan2) nids_license_management_update_details_plan2
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def hids_license_management_update_details_plan2(request):
    response_msg = {}
    plan_id = request.GET.get('plan_id')
    isodatetime = datetime.now(pytz.timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')

    # Check if plan_id is None or empty
    if not plan_id:
        return Response({"message_type": "unsuccessful", "message": "plan_id_not_found"})
    random_key = str(uuid.uuid4())
    try:
        # Try to retrieve an existing Updated_Plan_Details record by plan_id
        updated_plan_details = Updated_Plan_Details.objects.get(id=plan_id)
    except Updated_Plan_Details.DoesNotExist:
        return Response({"message_type": "unsuccessful", "message": "Plan not found"})

    # Now, you can create or update Hids_License_Management based on the fetched Updated_Plan_Details
    try:
        hids_license_management_query = Hids_License_Management.objects.get(updated_plan_id=updated_plan_details)
        serializer = UpgradeHidsLicensePlanStepThreeSerializer(instance=hids_license_management_query, data=request.data)
        if serializer.is_valid():
        
            serializer.save()
            api_logs_make(request, "updated plan2 hids license management details behalf of plan_id ",
                      "hids license management details upgrade plan2")
            response_msg = {"message_type": "updated_successfully", "message": "Data was updated in db"}
        else:
         response_msg = {"message_type": "unsuccessful", "message": "Data was not updated"}

       
    except Hids_License_Management.DoesNotExist:
        
        request_data = request.data.copy()
        request_data['created_at'] = isodatetime
        request_data['sensor_create_count'] = int(request.data.get("sensor_create_count", 0))
        request_data['sensor_active_count'] = request_data['sensor_create_count']
        request_data['updated_plan_id'] = updated_plan_details.id
        request_data['sensor_key'] = random_key
        serializer = UpgradeHidsLicensePlanStepThreeSerializer(data=request_data)
        
    if serializer.is_valid():
        serializer.validated_data['updated_plan_id'] = updated_plan_details
        serializer.validated_data['updated_at'] = isodatetime
        serializer.save()
        api_logs_make(request, "updated plan2 hids license management details behalf of plan_id ",
                      "hids license management details upgrade plan2")
        response_msg = {"message_type": "updated_successfully", "message": "Data was inserted in db"}
    else:
        response_msg = {"message_type": "unsuccessful", "message": "Data was not updated"}

    return Response(response_msg)

# Update api plan2 nids license management details (upgrade section plan2) nids_license_management_update_details_plan2
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def soar_license_management_update_details_plan2(request):
    response_msg = {}
    plan_id = request.GET.get('plan_id')
    isodatetime = datetime.now(pytz.timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')
    if not plan_id:
        return Response({"message_type": "unsuccessful", "message": "plan_id_not_found"})

    try:
        updated_plan_details = Updated_Plan_Details.objects.get(id=plan_id)
    except Updated_Plan_Details.DoesNotExist:
        return Response({"message_type": "unsuccessful", "message": "Plan not found"})
    random_key = str(uuid.uuid4())

    try:
        # Try to retrieve an existing Soar_License_Management record by updated_plan_id
        soar_license_management_query = Soar_License_Management.objects.get(updated_plan_id=updated_plan_details)
        serializer = UpgradeSoarLicensePlanStepThreeSerializer(instance=soar_license_management_query, data=request.data)
    except Soar_License_Management.DoesNotExist:
        # If the Soar_License_Management record doesn't exist, insert a new row
        request_data = request.data.copy()
        request_data['created_at'] = isodatetime
        request_data['sensor_create_count'] = int(request.data.get("sensor_create_count", 0))
        request_data['sensor_active_count'] = request_data['sensor_create_count']
        request_data['updated_plan_id'] = updated_plan_details.id
        request_data['sensor_key'] = random_key
        serializer = UpgradeSoarLicensePlanStepThreeSerializer(data=request_data)

    if serializer.is_valid():
        serializer.validated_data['updated_plan_id'] = updated_plan_details
        serializer.validated_data['updated_at'] = isodatetime
        serializer.save()
        api_logs_make(request, "updated plan2 soar license management details behalf of plan_id ",
                      "soar license management details upgrade plan2")
        response_msg = {"message_type": "updated_successfully", "message": "Data was updated in db"}
    else:
        response_msg = {"message_type": "unsuccessful", "message": "Data was not updated"}

    return Response(response_msg)
	
	
# to verify-- unverified users 
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_unverified_user(request, user_id):
    try:
        clientObj = Client_data.objects.get(id = user_id)

        if clientObj.first_config == 1:
            return Response({"message_type":"s_is_w","message":"user_already_verified"})
        else:
            generate_pass = ''.join([random.choice( string.ascii_uppercase + string.ascii_lowercase + string.digits) for n in range(10)])
            clientObj.client_password = generate_pass
            clientObj.save()
            api_logs_make(request,"user verified","already existing user verified")
            # generate link for new user
            link = BaseUrl+"/generate-new-password/"+str(clientObj.id)

            template_context = dict({
                                "link":link,
                                "temp_pass" :generate_pass,
                                "name" :str(clientObj.username),
                                "email" :str(clientObj.email)
                                })

            send = send_multiple_mail([str(clientObj.email)],"XDR Registration",template_context,"backend_app/welcome_password.html")
            if send.get("status") == "ok":
                return Response({"message_type":"success","message": "Mail sent to user"})
            else:
                return Response({"message_type":"s_is_w","message":"mail sending error", "mail_err": send.get("msg")})
    
    except Client_data.DoesNotExist:
        return Response({"message_type": "s_is_w", "message": "User/client object doesn't exist"})

# to reset_user_password
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reset_user_password(request):
    user_id = request.data.get('id')
    client_password = str(request.data.get('client_pass'))
    if (client_password is None) or (client_password == "") or (not(client_password.strip())):
        return Response({"message_type": "s_is_w", "message": "Enter a valid password"})
    
    sanitised_password = client_password.strip() #removed white spaces from entered password
    
    try:
        clientObj = Client_data.objects.get(id = user_id)
        desired_hasher = PBKDF2PasswordHasher()
        hashed_password = make_password(sanitised_password, salt=None, hasher=desired_hasher)
        clientObj.password = hashed_password
        clientObj.first_config = 1
        clientObj.client_password = ""
        clientObj.save()
        api_logs_make(request,"user password changed","already existing user password updated")

        return Response({"message_type":"success","message": "client password updated"}, status=status.HTTP_200_OK)
    
    except Client_data.DoesNotExist:
        return Response({"message_type": "s_is_w", "message": "User/client object doesn't exist"})