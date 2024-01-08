#  =========================================================================================================================================================
#  File Name: views.py
#  Description: This file contains code for functionalities like: user registration, user login, static reports, dynamic reports, dynamic network map etc.

#  ---------------------------------------------------------------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  ==========================================================================================================================================================

from rest_framework.decorators import api_view, permission_classes
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import parser_classes
from time import gmtime, strftime
from django.db import connection
import requests
from .mail_to import send_email_from_app
import json, ast
import random,uuid
import time
from datetime import date,datetime,timezone, timedelta
import pytz, dateutil.parser
from django.http import Http404
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

# import urllib
import random
import uuid
from .helpers import api_logs_make,strToComma, getIndexNameByLocationId, getPlatformAndBlacklistedItemsByLocationId
from .dashboard_queries import *
from .attack_events_queries import *
from .intelligence_queries import *
from .mldldetection_queries import *
# from .wazuh_query import *
from .custome_auth import ApiWithKeyAuth,UpdatedApiWithKeyAuth
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
from ._connection import *
from django.shortcuts import render
from .opensearch_config import query,opensearch_conn_using_db, querywazuh

from django.shortcuts import get_object_or_404
from .time_filter_on_queries import calculate_start_end_time,report_config_calculate_start_end_time, calculate_start_end_time_static_report

import ast
from .wazuh_mitre_attack_page import *
from .wazuh_query import *
from .crypt_func import encrypt, decrypt
from .soar_query import *
# from .send_pdf_mail import *



# auto generate token for user #START
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
# auto generate token for user #END

# master user registration #START


class UserRegistrationView(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            responst_json = {
                "message_type": "register_success request",
                "message": "Registration Successfully."
            }
            return Response(responst_json, status.HTTP_200_OK)

        responst_json = {
            "message_type": "form_errors",
            "message": "Required param not pass.",
            "errors": serializer.errors
        }
        return Response(responst_json, status.HTTP_400_BAD_REQUEST)
# master user registration #END

# master user login #START

class UserLoginView(APIView):
    def post(self, request, format=None):

        try:
            encrypted_payload = request.data.get('payload')
            decrypted_payload = decrypt(encrypted_payload)
            req_payload = json.loads(decrypted_payload)
        except json.JSONDecodeError as json_error:
            return Response({
            "message_type": "error",
            "message": f"invalid JSON format : {json_error}"
            }, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
            "message_type": "error",
            "message": f"Error : {e}"
            }, status.HTTP_400_BAD_REQUEST)

        serializer = UserLoginSerializer(data=dict({"email": req_payload.get("email"), "password": req_payload.get("password")}))
        
        if serializer.is_valid():
            password = serializer.data.get("password")
            email = serializer.data.get("email")
            userCheck = authenticate(email=email, password=password)
            if userCheck is not None:
                userDataS = UserProfileSerializer(userCheck)
                if userDataS.data.get("allow_MFA") == 1:
                    request.user = userCheck
                    v_token = uuid.uuid4()
                    otp = random.randrange(100000, 1000000, 6)
                    ip = request.META.get('HTTP_X_FORWARDED_FOR')
                    if ip:
                        ip = ip.split(',')[0]
                    else:
                        ip = request.META.get('REMOTE_ADDR')

                    template_context = {
                        "ip": ip,
                        "otp": otp,
                        "name": userDataS.data.get("username")
                    }

                    modelObj = Client_data.objects.get(email=str(request.user))
                    modelObj.otp_mail = otp
                    modelObj.MFA_token = v_token
                    modelObj.save()

                    # api_logs_make(request, "login", "login with MFA")
                    sendCheck = send_email_from_app(str(email), "MFA | Multifactor Authentication", template_context, "frontend/two_step_verification.html")

                    if sendCheck:
                        res_db = {
                            "message_type": "verify_mfa",
                            "v_token": v_token
                        }
                    else:
                        res_db = {
                            "message_type": "s_is_w"
                        }
                    return Response(res_db, status.HTTP_200_OK)
                else:
                    if (userDataS.data.get('profile_photo') == "") or (userDataS.data.get('profile_photo') == None):
                        new_userDataS = {'profile_photo_path':None}
                    else:
                        base_url = "{0}://{1}/".format(request.scheme, request.get_host())+'api'
                        full_profile_path = base_url+str(userDataS.data.get('profile_photo'))
                        new_userDataS = {'profile_photo_path':full_profile_path}
                    new_userDataS.update(userDataS.data)
                    request.user = userCheck


                    location_id_obj = userDataS.data.get('location_id')
                    plan_id = userDataS.data.get('activated_plan_id')
                    query_result_p = Page_Permissions.objects.get(location_id = location_id_obj, updated_plan_id = plan_id)
                    serializer_var_p = PagePermissionsSerializer(query_result_p)
                    

                    # api_logs_make(request, "login", "login without MFA")
                    responst_json = {
                        "message_type": "login_success",
                        "message": "Login Successfully.",
                        "bk_data": new_userDataS,
                        "token": get_tokens_for_user(userCheck),
                        "default_page" : serializer_var_p.data.get('default_page')
                    }
                    return Response(responst_json, status.HTTP_200_OK)
            else:
                responst_json = {
                    "message_type": "user_not_exist",
                    "message": "Incorrect email address or password"
                }
                return Response(responst_json, status.HTTP_404_NOT_FOUND)
        responst_json = {
            "message_type": "form_errors",
            "message": "Required param not pass.",
            "errors": serializer.errors
        }
        return Response(responst_json, status.HTTP_400_BAD_REQUEST)
# master user login #END

# master user profile #START


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        responst_json = {
            "message_type": "profile_data",
            "message": "show profile data",
            "data": serializer.data,
        }
        return Response(responst_json, status.HTTP_200_OK)


class ChangeCleintPasswordView(APIView):
    def post(self, request):
        serializer_class = ChangeCleintPasswordSerializer(data=request.data)
        if serializer_class.is_valid():
            return Response({"message_type": "success", "message": "Successfully updated password."}, status=status.HTTP_200_OK)
        else:
            return Response({"message_type": "form_errror", "message": "validation error", "errors": serializer_class.errors}, status=status.HTTP_400_BAD_REQUEST)

# To call all api of Dashboard page
class DashboardPage(APIView):
    permission_classes([IsAuthenticated])

    def post(self, request):
        login_client_email = str(request.user)
        agent_name = getAgentName(login_client_email)
        start_date = request.data.get("start_date")
        end_date = request.data.get("end_date")
        _platform = request.data.get("platform")
        platform = ",".join( repr(e) for e in _platform)
        _severity = request.data.get("threat_severity")
        severity=",".join( repr(e) for e in _severity)        
        _start_date = get_time_zone(start_date)
        _end_date = get_time_zone(end_date)
        
        start_date = _start_date[3]
        end_date = _end_date[3]
        # if type(platform) == list and type(severity) == list:
        #     if len(platform) == 0:
        #         platform = ["onpremise", "aws", "azure"]
        #     if len(severity) == 0:
        #         severity = [1,2,3]
        #     else:
        #         severity = list(map(int,severity))
        # if type(platform) is type(None):
        #     print("entered none condition")
        #     platform = ["onpremise", "aws", "azure"]
        # if type(severity) is type(None):
        #     severity = [1,2,3]
        
        lateral_attack_count = lateral_attack_func(agent_name,start_date,end_date,platform,severity)
        internalCompromised_attack_count = internalCompromised_attack_func(agent_name,start_date,end_date,platform,severity)
        severity1_attack_count = severity1_attack_count_func(agent_name,start_date,end_date,platform,severity)
        external_attack_count = external_attack_count_func(agent_name,start_date,end_date,platform,severity)
        attacker_table = Attacker_Table_func(agent_name,start_date,end_date,platform,severity)
        internal_external_count = Internal_External_Attack_Count(agent_name,start_date,end_date,platform,severity)
        MlThreatCount = Ml_Threat_Count_Func(agent_name,start_date,end_date,platform,severity)
        DlThreatCount = Dl_Threat_Count_Func(agent_name,start_date,end_date,platform,severity)
        IdsThreatCount = Ids_Threat_Count_Func(agent_name,start_date,end_date,platform,severity)
        internal_external_pie_chart = internal_external_pie(agent_name,start_date,end_date,platform,severity)
        zero_day_attack_count= zero_day_attack_card(agent_name,start_date,end_date,platform,severity)

        return Response({"attacker_table": attacker_table,"internalCompromised_attack_count": internalCompromised_attack_count, "external_attack_count": external_attack_count, "severity1_attack_count": severity1_attack_count,"lateral_attack_count": lateral_attack_count,"MlThreatCount": MlThreatCount, "DlThreatCount": DlThreatCount, "IdsThreatCount": IdsThreatCount,"internal_external_pie_chart": internal_external_pie_chart,"internal_external_count": internal_external_count, "zero_day_attack_count": zero_day_attack_count})

# To call all api of Attack_Events page
class ChartsAttackEvents(APIView):
    permission_classes([IsAuthenticated])

    def post(self, request):
        login_client_email = str(request.user)
        agent_name = getAgentName(login_client_email)
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        _platform = request.data.get("platform")
        platform = ",".join( repr(e) for e in _platform)
        _severity = request.data.get("threat_severity")
        severity=",".join( repr(e) for e in _severity)
        _start_date = get_time_zone(start_date)
        _end_date = get_time_zone(end_date)
        
        start_date = _start_date[3]
        end_date = _end_date[3]
        
        # print("platform before entering if block:", platform)
        # print("platform_type:", type(platform))# str,list
        # if type(platform) == list and type(severity) == list:
            # if len(platform) == 0:
            #     platform = ["onpremise", "aws", "azure"]
            # if len(severity) == 0:
            #     severity = [1,2,3]
        # print(f"after entering if block, platform is {platform}, severity is {severity}")

        Geoipcityname = Geoip_city_name(agent_name, start_date, end_date, platform, severity)
        AttackerLocationsTimestamp = Attacker_Locations_Timestamp(agent_name, start_date, end_date, platform, severity)
        CountryCount = geoip_country_name(agent_name, start_date, end_date, platform, severity)
        AsnCount = Asn_name_count(agent_name, start_date, end_date, platform, severity)
        TcpCount = Tcp_port_count(agent_name, start_date, end_date, platform, severity)
        FrequentAttackerMackAddresses = Frequent_Attacker_Mack_Addresses(agent_name, start_date, end_date, platform, severity)
        AttackerIPCount = Attacker_IP_count(agent_name, start_date, end_date, platform, severity)
        FrequencyOfAttacks = Frequency_of_attacks(agent_name, start_date, end_date, platform, severity)
        ServiceName = Service_Name(agent_name, start_date, end_date, platform, severity)

        return Response({"CountryCount": CountryCount, "Geoipcityname": Geoipcityname, "AsnCount": AsnCount, "AttackerLocationsTimestamp": AttackerLocationsTimestamp,"AttackerIPCount": AttackerIPCount, "FrequentAttackerMackAddresses": FrequentAttackerMackAddresses,"TcpCount": TcpCount,"FrequencyOfAttacks": FrequencyOfAttacks,"ServiceName": ServiceName})


def getAgentName(login_client_email,network_agent = False):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT b.attach_agent_group, b.attach_agent_network FROM client_data a  inner JOIN agent_details b ON b.organization_id = a.organization_id where email = %s", [
                       login_client_email])
        row = cursor.fetchone()
        if network_agent:
            agent_name = str(row[1])
        else:
            agent_name = str(row[0])
    finally:
        cursor.close()

    return agent_name
 
# To count Frequency of attacks in categories & series format
class ChartsIntelligence(APIView):
    permission_classes([IsAuthenticated])

    def post(self, request):
        login_client_email = str(request.user)
        agent_name = getAgentName(login_client_email)
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        _platform = request.data.get("platform")
        platform = ",".join( repr(e) for e in _platform)
        _severity = request.data.get("threat_severity")
        severity=",".join( repr(e) for e in _severity)
        _start_date = get_time_zone(start_date)
        _end_date = get_time_zone(end_date)
        
        start_date = _start_date[3]
        end_date = _end_date[3]
        # if type(platform) == list and type(severity) == list:
            # if len(platform) == 0:
            #     platform = ["onpremise", "aws", "azure"]
            # if len(severity) == 0:
            #     severity = [1,2,3]
        # print("platform after entering if block:", platform)

        TopVictimIpaddresses = Top_Victim_Ip_addresses(agent_name, start_date, end_date, platform, severity)
        TopAttackingIPs = Top_Attacking_IPs(agent_name, start_date, end_date, platform, severity)
        FastestAttackers = Fastest_Attackers(agent_name, start_date, end_date, platform, severity)
        GeolocationData = Geolocation_Data(agent_name, start_date, end_date, platform, severity)
        Victimtcpservicesattacked = Victimtcp_servicesattacked(agent_name, start_date, end_date, platform, severity)
        Victimudpservicesattacked = Victim_udp_services_attacked(agent_name, start_date, end_date, platform, severity)
        TopAttackTypesVictims = Top_Attack_Types_Victims(agent_name, start_date, end_date, platform, severity)
        TopAttackTypesAttackers = Top_Attack_Types_Attackers(agent_name, start_date, end_date, platform, severity)

        return Response({"TopVictimIpaddresses": TopVictimIpaddresses, "TopAttackingIPs": TopAttackingIPs, "FastestAttackers": FastestAttackers, "GeolocationData": GeolocationData, "Victimtcpservicesattacked": Victimtcpservicesattacked, "Victimudpservicesattacked": Victimudpservicesattacked, "TopAttackTypesVictims": TopAttackTypesVictims, "TopAttackTypesAttackers": TopAttackTypesAttackers})


# To call all api of Test page
class MlDlDetectionPage(APIView):
    permission_classes([IsAuthenticated])
    
    def post(self, request):
        login_client_email = str(request.user)
        agent_name = getAgentName(login_client_email)
        start_date = request.data.get("start_date")
        end_date = request.data.get("end_date")
        _platform = request.data.get("platform")
        platform = ",".join( repr(e) for e in _platform)
        # _severity = request.data.get("threat_severity")
        # severity=",".join( repr(e) for e in _severity)
        # accuracy = request.data.get("accuracy")
        # assigning right value to accuracy
        # case 1. above 90% ---- >90 and <=100
        accuracy1 = 0
        accuracy2 = 0
        if request.data.get("accuracy") == 1:
            # print("entered acc 1")
            accuracy1 = 90
            accuracy2 = 100
        # case 2. above 75% ---- >75 and <=90
        elif request.data.get("accuracy") == 2:
            # print("entered acc 2")
            accuracy1 = 75
            accuracy2 = 90
        # case 3. above 65% ----- >65 and <=75
        elif request.data.get("accuracy") == 3:
            # print("entered acc 3")
            accuracy1 = 65
            accuracy2 = 75
        # end
        _start_date = get_time_zone(start_date)
        _end_date = get_time_zone(end_date)
        
        start_date = _start_date[3]
        end_date = _end_date[3]
        # if type(platform) == list:
            # if len(platform) == 0:
            #     platform = ["onpremise", "aws", "azure"]
            # if len(severity) == 0:
            #     severity = [1,2,3]
        
        TestPageTable = test_page_table(agent_name,start_date,end_date,platform,accuracy1, accuracy2)
        CriticalThreats = critical_threats_count(agent_name,start_date,end_date,platform,accuracy1, accuracy2)
        LateralAttackCount = lateral_attack_count(agent_name,start_date,end_date,platform,accuracy1, accuracy2)
        InternalCompromisedAttackCount = internalCompromised_attack_count(agent_name,start_date,end_date,platform,accuracy1, accuracy2)
        ExternalAttackCount = external_attack_count(agent_name,start_date,end_date,platform,accuracy1, accuracy2)
        GeoipCityCount = Geoip_city_count(agent_name, start_date, end_date, platform, accuracy1, accuracy2)
        GeoipCountryCount = geoip_country_count(agent_name, start_date, end_date, platform, accuracy1, accuracy2)
        AsnNameCount = Asn_count_func(agent_name, start_date, end_date, platform, accuracy1, accuracy2)
        TcpPortCount = Tcp_port_count_func(agent_name, start_date, end_date, platform, accuracy1, accuracy2)
        AttackerMacAddresses = Attacker_Mac_Addresses(agent_name, start_date, end_date, platform, accuracy1, accuracy2)
        FrequencyOfAttacks = Frequency_of_attacks_func(agent_name, start_date, end_date, platform, accuracy1, accuracy2)
        ServiceName = Service_Name_func(agent_name, start_date, end_date, platform, accuracy1, accuracy2)
        AttackerIPCount = Attacker_IP_count_func(agent_name, start_date, end_date, platform, accuracy1, accuracy2)
        MlThreatCount = Ml_Threat_Count(agent_name,start_date,end_date,platform,accuracy1, accuracy2)
        DlThreatCount = Dl_Threat_Count(agent_name,start_date,end_date,platform,accuracy1, accuracy2)
        
        return Response({"TestPageTable": TestPageTable,"CriticalThreats": CriticalThreats, "LateralAttackCount": LateralAttackCount, "InternalCompromisedAttackCount": InternalCompromisedAttackCount, "ExternalAttackCount": ExternalAttackCount, "GeoipCityCount": GeoipCityCount, "GeoipCountryCount": GeoipCountryCount, "AsnNameCount": AsnNameCount, "TcpPortCount": TcpPortCount, "AttackerMacAddresses": AttackerMacAddresses, "FrequencyOfAttacks": FrequencyOfAttacks, "ServiceName": ServiceName, "AttackerIPCount": AttackerIPCount, "MlThreatCount": MlThreatCount, "DlThreatCount": DlThreatCount})

# query for nmap for different sensors(aws,onpremise,azure) #helper functn used in 'dynamic_network_map' view mentioned below
def different_platform_query_output(indice_name, location_id, platform, plan_id):
    for i in range(31):
        today_date = date.today()-timedelta(days=i)
        date_in_format = today_date.strftime("%Y.%m.%d")
        nmap_sql_query = (f"SELECT network_map FROM {indice_name}-{date_in_format} WHERE map_category = '{platform}' ORDER BY attack_epoch_time DESC LIMIT 1;")
        
        nmap_query_search = opensearch_conn_using_db(nmap_sql_query, location_id, plan_id)
        check_query_length = nmap_query_search.get("total")
        if nmap_query_search.get("total") is None:
            check_query_length = 0
        if check_query_length > 0:
            break

    if nmap_query_search.get("total") is None:
        check_query_length = 0
    
    if check_query_length > 0:
        query_result_list = nmap_query_search['datarows']
        new_list = str(query_result_list)[3:-3]
        json_data = [json.loads(new_list)]
    else:
        json_data = []
    return json_data

# (display network map of all 3 sensors on current date where capture_timestamp is the latest)
# dynamic network map which returns data of all sensors where data is available--aws/onprim/azure 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dynamic_network_map(request):
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "err": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_nmap_agent')

    run_nmap_query = opensearch_conn_using_db(f"SELECT map_category FROM {indice_name}-* GROUP BY map_category;", location_id, plan_id)

    set_response = {"message_type":"success"}

    if run_nmap_query.get("total") not in [0,None]:
        query_op_list = run_nmap_query.get('datarows')
        flat_list = [element for innerList in query_op_list for element in innerList]
        set_response["aws"] = False
        set_response["onpremise"] = False
        set_response["azure"] = False
        set_response["data"] = {}

        if "aws" in flat_list:
            set_response["aws"] = True
            json_data = different_platform_query_output(indice_name, location_id, "aws", plan_id)
            set_response["data"].update({"aws":json_data})
        else:
            set_response["data"].update({"aws":[]})
        
        if "onpremise" in flat_list:
            set_response["onpremise"] = True
            json_data = different_platform_query_output(indice_name, location_id, "onpremise", plan_id)
            set_response["data"].update({"onpremise":json_data})
        else:
            set_response["data"].update({"onpremise":[]})
        
        if "azure" in flat_list:
            set_response["azure"] = True
            json_data = different_platform_query_output(indice_name, location_id, "azure", plan_id)
            set_response["data"].update({"azure":json_data})
        else:
            set_response["data"].update({"azure":[]})

    else:
        set_response = {"message_type":"d_not_f"}
    
    return Response(set_response)

# ----------display Country table data---------------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Display_Country_data(request):
    if request.method == 'GET':
        results = Country_data.objects.all()
        serializer = CountrySerializer(results, many=True)
        return Response(serializer.data)

# below view is used to get list of 'trace_sensor' in db against location of logged in user by Priya  
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetTraceSensorNames(request):
    msg = {"message_type":"s_is_w"}
    location_id = request.user.location_id.id
    try:
        init_obj = Init_Configs.objects.filter(location_id = location_id).first()
        formatted_sensor_names = ast.literal_eval(init_obj.trace_sensor)
        msg = {"message_type":"d_found", "data":formatted_sensor_names }   
        
    except ObjectDoesNotExist:
        msg = {"message_type":"d_not_f"}
    
    return Response(msg)

@api_view(['POST'])
def Incident_Response_report(request):
    if request.method == 'POST':
        Dict = dict(request.POST)
        if 'condition' in Dict:
            condition = Dict.get('condition')[0]
        else:
            condition = 'last_7_days'

        location_id = request.user.location_id.id
        plan_idObj = request.user.location_id.activated_plan_id

        if plan_idObj is not None:
            plan_id = plan_idObj.id
        else:
            return Response({"message_type": "d_not_f", "err": "plan_id_n_found"})
        
        index_name_dict = getIndexNameByLocationId(location_id, plan_id)

        # getting values from request
        product_types = Dict.get('product_types')
        product_name = product_types[0]
        if product_name in ("nids", "hids"):
            _platform_tuple = str(Dict.get("platform"))
            platform_tuple = "({})".format(_platform_tuple.strip("[]"))
        elif product_name in ("trace"):
            _sensor_tuple = str(Dict.get("sensor_names"))
            sensor_tuple = "({})".format(_sensor_tuple.strip("[]"))

        logs_type = Dict.get('logs_type')

        indice_mapping = {
        ('nids', 'alert'): 'nids_alert_agent',
        ('nids', 'event'): 'nids_event_agent',
        ('nids', 'incident'): 'nids_incident_agent',
        ('hids', 'alert'): 'hids_alert_agent',
        ('hids', 'event'): 'hids_event_agent',
        ('hids', 'incident'): 'hids_incident_agent',
        ('trace', 'alert'): 'trace_alert_agent',
        ('trace', 'event'): 'trace_event_agent',
        ('trace', 'incident'): 'trace_incident_agent',
        ('trace', 'dpi'): 'trace_dpi_agent'
        }
    
        indice_name = index_name_dict.get(indice_mapping.get((product_types[0], logs_type[0])))

        detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

        if not detail_dict:
            # got empty dict
            return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
        
        blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
        
        blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
        
        s1 = f"AND ids_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
        s2 = f" AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""

        past_time, current_time = calculate_start_end_time_static_report(condition)

        if product_types == ['nids'] and request.POST['threat_type'] == 'internal_attack':
            threat_type_tuple = ('Lateral Movement', 'Internal Compromised Machine')
            formed_sql = f"SELECT attacker_ip, target_ip, target_mac, service_name,type_of_threat,ids_threat_type,ids_threat_class, count(attacker_ip) attacker_ip_count FROM {indice_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} and platform IN {platform_tuple} and type_of_threat IN {threat_type_tuple} "+s1+s2+f" GROUP BY attacker_ip, target_ip, target_mac, service_name,type_of_threat,ids_threat_type,ids_threat_class ORDER BY attacker_ip_count desc LIMIT {request.POST['top_count']};"

        elif product_types == ['nids'] and request.POST['threat_type'] == 'external_attack':
            threat_type_tuple = ('External Attack', 'Attack on External Server')
            formed_sql = f"SELECT attacker_ip, geoip_country_name,geoip_asn_name, target_ip, attacker_mac,service_name,target_mac, type_of_threat,ids_threat_type,ids_threat_class, count(attacker_ip) attacker_ip_count FROM {indice_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} and platform IN {platform_tuple} and type_of_threat IN {threat_type_tuple} and geoip_country_name IS NOT NULL and geoip_asn_name IS NOT NULL "+s1+s2+f" GROUP BY attacker_ip, geoip_country_name,geoip_asn_name, target_ip, service_name,attacker_mac,target_mac, type_of_threat,ids_threat_type,ids_threat_class ORDER BY attacker_ip_count desc LIMIT {request.POST['top_count']};"
        
        elif product_types == ['hids']:
            formed_sql = f"SELECT agent_id, agent_ip, agent_location, agent_name, location, rule_description, rule_firedtimes, potential_ransomware_event, anomaly_label from {indice_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} ORDER BY agent_id LIMIT {request.POST['top_count']};"
        
        elif product_types == ['trace']:
            # case 1:type_of_threat=Internal
            if request.POST['threat_type'] == 'internal_attack':
                threat_type_tuple = ('Lateral Movement', 'Internal Compromised Machine')
        
            # case 2:type_of_threat=External # attacker_host_type, malware_cve_id, intel_source_feed_name
            if request.POST['threat_type'] == 'external_attack':
                threat_type_tuple = ('External Attack', 'Attack on External Server')

            formed_sql = f"SELECT attack_timestamp, attacker_ip, attacker_port, service_name, target_ip, target_port, ids_threat_class, ids_threat_type, tag, sensor_name, ip_rep from {indice_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} AND type_of_threat IN {threat_type_tuple} AND sensor_name IN {sensor_tuple} "+s1+s2+f" ORDER BY attack_epoch_time DESC LIMIT {request.POST['top_count']};"

        api_query = opensearch_conn_using_db(formed_sql, location_id, plan_id)
        check_query_length = api_query.get("total")
        if api_query.get("total") is None:
            check_query_length = 0
            
        if check_query_length > 0:
            api_logs_make(request, "Incident Response Report", "get report data from db")

            key_names = [item['alias'] if (item['name'] == "count(attacker_ip)") else item['name'] for item in api_query.get('schema')]

            final_response = []
            for i in range(len( api_query.get('datarows'))):
                row =  api_query.get('datarows')[i]
                final_response.append(dict(zip(key_names, row)))
            
            for item in final_response:
                if "potential_ransomware_event" in item:
                    ransomware_boolean_val = item.get('potential_ransomware_event')
                    item['potential_ransomware_event'] = str(ransomware_boolean_val)

            return Response({"message_type": "data_ok", "data": final_response})
        else:
            return Response({"message_type": "d_not_f"})            

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Displayall_api_logs(request):
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
    query = ApiLogs.objects.filter(table_name="client_data", org_id=str(request.user.organization_id)).order_by("-date_time")[_offset:_offset+_limit]
    serializer = Api_LogsSerializer(query, many=True)
    
    if len(serializer.data) > 0:
        return Response({"message_type":"data_found","data":serializer.data})
    else:
        return Response({"message_type":"data_not_found"})

class Xdr_api(APIView):
    authentication_classes = [ApiWithKeyAuth]
    def get(self,request,format=None):
        client_email = str(request.user.client_id)
        locObj = request.user.client_id.location_id
        location_id = locObj.id
        plan_id = locObj.activated_plan_id.id
        agent_name = getAgentName(client_email)
        key_names = []
        final_response = []
        severity_one_count = 0
        severity_two_count = 0
        severity_three_count = 0
       
        get_limit = request.GET.get("limit")
        limit = ''
        if get_limit != None:
            limit = (f"LIMIT {get_limit}")            

        get_offset = request.GET.get("offset")
        offset = ''
        if get_offset != None and get_limit != None:
            offset = (f"OFFSET {get_offset}")        
        
        ids_threat_severity = request.GET.get("severity")
        severity = ''
        if ids_threat_severity == str("null"):        
            severity = (f"WHERE (ids_threat_severity IS NULL)")

        elif ids_threat_severity != None and ids_threat_severity:
            severity = (f"WHERE (ids_threat_severity IN({ids_threat_severity}))")
       
        else:
            severity = (f"WHERE ids_threat_class != 'track_sql'")

        platform = request.GET.get("platform")
        platform_q = ''
        if platform != None and platform:
            platform = strToComma(platform)
            platform_q = (f" AND (platform IN({platform}))")

        start_date_val = request.GET.get("start_date")
        start_date = ''
        if start_date_val != None:
            get_arr_datetime = get_time_zone(start_date_val)
            start_date = (f"AND (attack_epoch_time >= {get_arr_datetime[1]})")
           
        end_date_val = request.GET.get("end_date")
        end_date = ''
        if end_date_val != None:
            get_arr_datetime = get_time_zone(end_date_val)
            end_date = (f"AND (attack_epoch_time <= {get_arr_datetime[1]})")

        order_by_val = request.GET.get("order_by")
        order_by = ''
        if order_by_val != None:
            if order_by_val == "asc":
                order_by = "ORDER BY attack_epoch_time ASC"
            else:
                order_by = "ORDER BY attack_epoch_time DESC"

        order_by_col_name = request.GET.get("order_by_col_name")
        if order_by_val != None and order_by_col_name != None:
            if order_by_val == "asc":
                order_by = (f"ORDER BY {order_by_col_name} ASC")
            else:
                order_by = (f"ORDER BY {order_by_col_name} DESC")
                           
        search_query = (f"SELECT * FROM {agent_name}-* {severity} {platform_q} {start_date} {end_date} {order_by} {limit}  {offset}")

        queryCheck = opensearch_conn_using_db(search_query.strip(), location_id, plan_id)

        set_response = {"message_type":"s_is_w"}

        check_query_length = queryCheck.get("total")
        if queryCheck.get("total") is None:
            check_query_length = 0

        if check_query_length <= 0:
                set_response = {"message_type":"d_not_f"}
                # set_response = {"message_type":"d_not_f","sql_query":search_query}
        else:

            for i in range(0, len(queryCheck.get('schema'))):
                key_names.append(queryCheck.get('schema')[i].get('name'))
               
            for i in range(0, len(queryCheck.get('datarows'))):
                row = queryCheck.get('datarows')[i]

                if int(row[13]) == 1:
                    severity_one_count += 1

                if int(row[13]) == 2:
                    severity_two_count += 1

                if int(row[13]) == 3:
                    severity_three_count += 1

                final_response.append(dict(zip(key_names, row)))

            """ set_response = {"message_type":"success","data_len":len(final_response),"severity_one_event_count":severity_one_count,"severity_two_event_count":severity_two_count,"severity_three_event_count":severity_three_count,
            "sql_query":search_query,"data":final_response} """
            set_response = {"message_type":"success","data_len":len(final_response),"severity_one_event_count":severity_one_count,"severity_two_event_count":severity_two_count,"severity_three_event_count":severity_three_count,"data":final_response}
        return Response(set_response)


def get_time_zone(dates):
        check_date_time = dateutil.parser.parse(dates)
        tuple = check_date_time.timetuple()

        date_time = datetime.fromtimestamp(time.mktime(tuple)).strftime('%Y-%m-%d %H:%M:%S')

        time_only = datetime.fromtimestamp(time.mktime(tuple)).strftime('%H:%M:%S')

        date_only = datetime.fromtimestamp(time.mktime(tuple)).strftime('%Y-%m-%d')

        str_time = datetime.strptime(time_only, '%H:%M:%S')
        timestamp = int(round(check_date_time.replace(tzinfo=timezone.utc).timestamp() * 1000))
        return [date_time,timestamp,str_time,date_only]

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def Third_party_api(request):
    api_key_gen = str(uuid.uuid4()) + "-" + str(uuid.uuid4())
    api_id = request.data.get('application_id')
    application_obj = Applications.objects.get(id = api_id)
    api_name = application_obj.application_name
    req_data = {**request.data,"client_id" : request.user.id,"api_key" : api_key_gen,'api_key_status':True, 'api_name' : f"{api_name}"}
    serializer = Third_party_api_serializer(data=req_data)
    if serializer.is_valid():
        serializer.save()
        api_logs_make(request,"create_third_party_api","Create new third party api key")
        return Response({"message_type":"created","data":serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({"message_type":"form_errors","errors":serializer.errors}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Show_ApiKeys(request):
    try:
        results = Api_export.objects.filter(client_id = request.user.id)
        serializer = Api_Export_Third_Party_serializer(results, many=True)
        return Response({"message_type":"data_found","data":serializer.data})
    except ObjectDoesNotExist:
        return Response({"message_type":"d_not_f"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Third_party_status_api(request):
    try:
        clientObj = Api_export.objects.get(id = request.data.get("id"))
        serializer = Third_party_status_serializer(clientObj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            api_logs_make(request,"third_party","Third party api status update.")
            return Response({"message_type":"updated"})
        else:
            return Response({"message_type":"form_errors","errors":serializer.errors})
    except Api_export.DoesNotExist:
            return Response({"message_type":"id_not_found"})

# Executive Report
@api_view(['POST'])
def Executive_report(request):
    if request.method =='POST':
        Dict = dict(request.POST)
        if 'condition' in Dict:
            condition = Dict.get('condition')[0]
        else:
            condition = 'last_7_days'

        location_id = request.user.location_id.id
        plan_idObj = request.user.location_id.activated_plan_id

        if plan_idObj is not None:
            plan_id = plan_idObj.id
        else:
            return Response({"message_type": "d_not_f", "err": "plan_id_n_found"})
        
        index_name_dict = getIndexNameByLocationId(location_id, plan_id)

        # getting values from request
        product_types = Dict.get('product_types')
        product_name = product_types[0]
        if product_name in ("nids", "hids"):
            _platform_tuple = str(Dict.get("platform"))
            platform_tuple = "({})".format(_platform_tuple.strip("[]"))
        elif product_name in ("trace"):
            _sensor_tuple = str(Dict.get("sensor_names"))
            sensor_tuple = "({})".format(_sensor_tuple.strip("[]"))

        logs_type = Dict.get('logs_type')

        indice_mapping = {
        ('nids', 'alert'): 'nids_alert_agent',
        ('nids', 'event'): 'nids_event_agent',
        ('nids', 'incident'): 'nids_incident_agent',
        ('hids', 'alert'): 'hids_alert_agent',
        ('hids', 'event'): 'hids_event_agent',
        ('hids', 'incident'): 'hids_incident_agent',
        ('trace', 'alert'): 'trace_alert_agent',
        ('trace', 'event'): 'trace_event_agent',
        ('trace', 'incident'): 'trace_incident_agent',
        ('trace', 'dpi'): 'trace_dpi_agent'
        }
    
        indice_name = index_name_dict.get(indice_mapping.get((product_types[0], logs_type[0])))

        detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

        if not detail_dict:
            # got empty dict
            return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
        
        blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
        
        blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
        
        s1 = f"AND ids_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
        s2 = f" AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""

        past_time, current_time = calculate_start_end_time_static_report(condition)
        

        if product_types == ['nids']:
            # case 1:type_of_threat=Internal
            if request.POST['threat_type'] == 'internal_attack':
                threat_type_tuple = ('Lateral Movement', 'Internal Compromised Machine')
        
            # case 2:type_of_threat=External
            if request.POST['threat_type'] == 'external_attack':
                threat_type_tuple = ('External Attack', 'Attack on External Server')
            
            formed_sql = f"SELECT target_ip, target_mac, service_name, type_of_threat, count(attacker_ip) attacker_ip_count FROM {indice_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} AND type_of_threat IN {threat_type_tuple} AND type_of_threat IS NOT NULL AND service_name is NOT NULL AND platform IN {platform_tuple} "+s1+s2+f" GROUP BY attacker_ip, target_ip, target_mac, service_name, type_of_threat ORDER BY attacker_ip_count desc LIMIT {request.POST['top_count']};"
        
        elif product_types == ['hids'] and logs_type == ['incident']:
            formed_sql = f"SELECT agent_id, agent_ip, rule_gdpr, rule_mitre_id, rule_mitre_tactic, rule_mitre_technique, rule_nist_800_53, rule_pci_dss, rule_tsc,potential_ransomware_event, anomaly_label from {indice_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} ORDER BY agent_id LIMIT {request.POST['top_count']};"
        
        elif product_types == ['hids']:
            formed_sql = f"SELECT agent_id, agent_ip, rule_gdpr, rule_hipaa, rule_mitre_id, rule_mitre_tactic, rule_mitre_technique, rule_nist_800_53, rule_pci_dss, rule_tsc,potential_ransomware_event, anomaly_label from {indice_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} ORDER BY agent_id LIMIT {request.POST['top_count']};"
        
        elif product_types == ['trace']:
            # case 1:type_of_threat=Internal
            if request.POST['threat_type'] == 'internal_attack':
                threat_type_tuple = ('Lateral Movement', 'Internal Compromised Machine')
        
            # case 2:type_of_threat=External
            if request.POST['threat_type'] == 'external_attack':
                threat_type_tuple = ('External Attack', 'Attack on External Server')

            formed_sql = f"SELECT attack_timestamp, attacker_ip, attacker_port, service_name, target_ip, target_port, ids_threat_class, sensor_name, geoip_country_name, geoip_city, geoip_region_name, geoip_asn_name, ip_rep from {indice_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} AND type_of_threat IN {threat_type_tuple} AND sensor_name IN {sensor_tuple} "+s1+s2+f" ORDER BY attack_epoch_time DESC LIMIT {request.POST['top_count']};"

        
        sql_query = opensearch_conn_using_db(formed_sql, location_id, plan_id)

        check_query_length = sql_query.get("total")
        if sql_query.get("total") is None:
            check_query_length = 0
       
        if check_query_length > 0 :
            api_logs_make(request, "Incident Response Report", "get report data from db")

            key_names = [item['alias'] if (item['name'] == "count(attacker_ip)") else item['name'] for item in sql_query.get('schema')]

            final_response = []
            for i in range(len(sql_query.get('datarows'))):
                row = sql_query.get('datarows')[i]
                final_response.append(dict(zip(key_names, row)))
            
            for item in final_response:
                if "potential_ransomware_event" in item:
                    ransomware_boolean_val = item.get('potential_ransomware_event')
                    item['potential_ransomware_event'] = str(ransomware_boolean_val)
               
            return Response({"message_type": "data_ok", "data": final_response})
        else:
            return Response({"message_type":"d_not_f"})

#To get apllogs users
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

#Update email config and insert config type
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Email_Config_Update(request):
    config_type = request.POST.get('config_type')
    user_location_obj = request.user.location_id
    plan_id = user_location_obj.activated_plan_id

    try:
        init_config_detail = Init_Configs.objects.get(config_type=config_type, location_id = user_location_obj.id, updated_plan_id = plan_id.id)
    except Init_Configs.DoesNotExist:
        return Response({"message_type": "config_not_found"})

    platform_val_tuple = request.data.getlist('platform_val[]')
    severity_val_tuple = request.data.getlist('severity_val[]')
    email_ids_tuple = request.data.getlist('email_ids[]')
    # trace_sensor_tuple = request.data.getlist('trace_sensor[]')

    if len(platform_val_tuple) == 1:
        platform_val_tuple = f"('{platform_val_tuple[0]}')"  # Wrap single value in parentheses
    else:
        platform_val_tuple = tuple(platform_val_tuple)

    if len(severity_val_tuple) == 1:
        severity_val_tuple = f"({int(severity_val_tuple[0])})"  # Wrap single value in parentheses
    else:
        severity_val_tuple = f"({','.join(map(str, map(int, severity_val_tuple)))})"  # Join multiple values with comma and wrap in parentheses
    
    if len(email_ids_tuple) == 1:
        email_ids_tuple = email_ids_tuple[0]  # Wrap single value in parentheses
    else:
        email_ids_tuple = f"{','.join(map(str, email_ids_tuple))}"
    
    init_config_detail.platform_val = platform_val_tuple
    init_config_detail.severity_val = severity_val_tuple
    init_config_detail.email_ids = email_ids_tuple
    init_config_detail.time_interval_val = request.data.get('time_interval_val')
    init_config_detail.time_interval_name = 0
    init_config_detail.config_type = config_type
    init_config_detail.save()

    serializer = Email_Config_Serializer(init_config_detail)
    data = serializer.data
    data['platform_val'] = platform_val_tuple
    data['severity_val'] = severity_val_tuple
    api_logs_make(request,"Update dashboard config","dashboard config updated")

    return Response({"message_type": "updated", "data": data})

#To display email id from client data

# display email id of all clients within same location--using login id 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def EmailClientListOrg(request):
    msg = {"message_type":"s_is_w"}
    try:
        user_location_obj = request.user.location_id
        queryset = Client_data.objects.filter(location_id = user_location_obj.id)
        if queryset is None:
            return Response({"message_type":"data_not_found"})
        
        serializer = Clent_Email_Serializer(queryset, many = True)
        msg = {"message_type":"d_found", "data": serializer.data}
    except ObjectDoesNotExist:
        msg = {"message_type":"data_not_found"}
    
    return Response(msg)


# To get dashboard_config with location_id and config_types(updated)
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
@permission_classes([IsAuthenticated])
def Dashboard_Config_Update(request):
    config_type = request.POST.get('config_type')
    user_location_obj = request.user.location_id
    plan_id = user_location_obj.activated_plan_id
    
    try:
        init_config_detail = Init_Configs.objects.get(config_type=config_type, location_id = user_location_obj.id, updated_plan_id = plan_id.id)
    except Init_Configs.DoesNotExist:
        return Response({"message_type": "config_not_found"})

    platform_val_tuple = request.data.getlist('platform_val[]')
    severity_val_tuple = request.data.getlist('severity_val[]')
    # trace_sensor_tuple = request.data.getlist('trace_sensor[]')

    if len(platform_val_tuple) == 1:
        platform_val_tuple = f"('{platform_val_tuple[0]}')"  # Wrap single value in parentheses
    else:
        platform_val_tuple = tuple(platform_val_tuple)

    if len(severity_val_tuple) == 1:
        severity_val_tuple = f"({int(severity_val_tuple[0])})"  # Wrap single value in parentheses
    else:
        severity_val_tuple = f"({','.join(map(str, map(int, severity_val_tuple)))})"

    # if len(trace_sensor_tuple) == 1:
    #     trace_sensor_tuple = f"('{trace_sensor_tuple[0]}')"  # Wrap single value in parentheses
    # else:
    #     trace_sensor_tuple = tuple(trace_sensor_tuple)  


    init_config_detail.platform_val = platform_val_tuple
    init_config_detail.severity_val = severity_val_tuple
    init_config_detail.accuracy_val = request.data.get('accuracy_val')[0]
    # init_config_detail.trace_sensor = trace_sensor_tuple
    init_config_detail.config_type = config_type
    init_config_detail.save()

    serializer = DahboardConfigSerializer(init_config_detail)  # Use your serializer class here
    data = serializer.data
    data['platform_val'] = platform_val_tuple
    data['severity_val'] = severity_val_tuple
    # data['trace_sensor'] = trace_sensor_tuple
    api_logs_make(request,"Update dahsboard config","dashboard config updated")

    return Response({"message_type": "updated", "data": data})

#To update notification and insert config api(updated)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Notification_Config_Update(request):
    request.data._mutable = True
    config_type = request.POST.get('config_type')
    user_location_obj = request.user.location_id
    plan_id = user_location_obj.activated_plan_id

    try:
        init_config_detail = Init_Configs.objects.get(config_type=config_type, location_id = user_location_obj.id, updated_plan_id = plan_id.id)
    except Init_Configs.DoesNotExist:
        return Response({"message_type": "config_not_found"})

    platform_val_tuple = request.data.getlist('platform_val[]')
    severity_val_tuple = request.data.getlist('severity_val[]')
    if len(platform_val_tuple) == 1:
        platform_val_tuple = f"('{platform_val_tuple[0]}')"  # Wrap single value in parentheses
    else:
        platform_val_tuple = tuple(platform_val_tuple)

    if len(severity_val_tuple) == 1:
        severity_val_tuple = f"({int(severity_val_tuple[0])})"  # Wrap single value in parentheses
    else:
        severity_val_tuple = f"({','.join(map(str, map(int, severity_val_tuple)))})"  # Join multiple values with comma and wrap in parentheses

    init_config_detail.platform_val = platform_val_tuple
    init_config_detail.severity_val = severity_val_tuple
    init_config_detail.time_interval_val = request.data.get('time_interval_val')
    init_config_detail.time_interval_name = 0
    init_config_detail.config_type = config_type
    init_config_detail.save()

    serializer = Notification_Config_Serializer(init_config_detail)  # Use your serializer class here
    data = serializer.data
    data['platform_val'] = platform_val_tuple
    data['severity_val'] = severity_val_tuple
    api_logs_make(request,"Update dahsboard config","dashboard config updated")

    return Response({"message_type": "updated", "data": data})

#To get all details of init config email and dashboard record(updated)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Display_Config(request):
    config_type = request.GET.get("config_type")
    user_location_obj = request.user.location_id
    plan_id = user_location_obj.activated_plan_id
    try: 
        query_client = Init_Configs.objects.filter(config_type=config_type, location_id = user_location_obj.id, updated_plan_id = plan_id.id)
        if query_client.exists():
            serializer_org_users = Config_Serializer(query_client, many=True)
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

                if 'email_ids' in obj:
                    email_ids = obj['email_ids']
                    if email_ids is not None:
                        email_ids = email_ids.strip("()")  # Remove parentheses
                        email_ids = email_ids.replace("'", "")  # Remove single quotes
                        email_ids = email_ids.replace(" ", "")
                    else:
                        email_ids = ""  # Set email_ids to an empty string
                    obj['email_ids'] = email_ids

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

            return Response({"message_type": "data_found", "data": serializer_org_users.data})
        else:
            return Response({"message_type": "data_not_found"})
    except Client_data.DoesNotExist:
        return Response({"message_type": "user_id_not_found"})

#To update login users with activate and deactivate
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ActivateDeactivate(request):
    if request.method=="POST":
        clientObj = Client_data.objects.get(id = request.data.get("id"))
        serializer = ActivateDeactivate_Serializer(clientObj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            api_logs_make(request,"activate_deactivate"," updated activate and deactivate login")
            return Response({"message_type":"updated"}, status=status.HTTP_200_OK)
        else:
            return Response({"message_type":"form_errors","errors":serializer.errors}, status=status.HTTP_200_OK)

#To enable/disable (Dashboard or Email) notifications (is_active value is updated in db)
class UpdateUserNotificationStatus(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,*args, **kwargs):
        is_active_value = request.data.get('is_active')
        user_location_obj = request.user.location_id
        location_id = user_location_obj.id
        plan_id = user_location_obj.activated_plan_id
        config_type = request.data.get("config_type")
        init_objects_updated = Init_Configs.objects.filter(config_type = config_type,location_id = location_id, updated_plan_id = plan_id).update(is_active = is_active_value)
        if config_type == "notification_live":
            notification_type = "Dashboard Notification"
        elif config_type == "email_config_live":
            notification_type = "Email Notification"
        
        res = {}
        if is_active_value == True:
            status_variable = "Activated"
        else:
            status_variable = "Deactivated"
        
        if init_objects_updated > 0:
            api_logs_make(request,f"{notification_type}",f"{notification_type} is {status_variable}")
            res = {
                "message_type":"is_active_update",
                "data":is_active_value
            }
                
        else:
                res = {
                "message_type":"s_is_w",
                "errors":is_active_value
            }

        return Response(res)


# Key Management page- display application names in drop down list
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ApplicationListOrg(request):
    application_obj = Applications.objects.filter(integration_status=False).values('application_name')
    queryset = Applications.objects.all().exclude(application_name__in=application_obj)
    base_url =  "{0}://{1}/".format(request.scheme, request.get_host())
    serializer = Application_views_serializer(queryset, many=True, context = {"base_url":base_url})
    return Response(serializer.data)

# display application names......(below both application views created for application-shop page)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ApplicationDisplay(request):
    application_obj = Applications.objects.filter(integration_status=False).values('application_name')
    queryset = Applications.objects.all().exclude(application_name__in=application_obj)
    base_url =  "{0}://{1}/".format(request.scheme, request.get_host())
    serializer = Application_shop_serializer(queryset, many=True, context = {"base_url":base_url})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ApplicationDetailOrg(request, pk):
    try:
        query = Applications.objects.get(id = pk)
        base_url =  "{0}://{1}/".format(request.scheme, request.get_host())
        serializer = Application_shop_serializer(query, context = {"base_url":base_url})
        return Response({"message_type": "success","data":serializer.data})
    except ObjectDoesNotExist:
        return Response({"message_type":"d_not_f"})

# Innovative search # To get indices name basis on env_type in page_permission models from agent-details models
class InnovativeSearchIndicesNameView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):

        try:
            user_location_obj = request.user.location_id
            plan_idObj = request.user.location_id.activated_plan_id
            if plan_idObj is not None:
                plan_id = plan_idObj.id
            else:
                return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
            
            page_permission_obj = Page_Permissions.objects.get(location_id=user_location_obj.id, updated_plan_id = plan_id)
            user_org_obj = str(request.user.organization_id)
        except ObjectDoesNotExist:
            return Response({"message_type": "location not found"})

       
        # user_org_obj = str(request.user.organization_id)
        columns_serializers = {
            'env_hids': AlldataAgentPermissionsSerializer,
            'env_nids': NidsAlldataAgentPermissionsSerializer,
            'env_trace': TraceAlldataAgentPermissionsSerializer,
            'env_wazuh': WazuhAlldataAgentPermissionsSerializer,
            'env_hc': HealthCheckAlldataAgentPermissionsSerializer,
            'env_soar': SoarAlldataAgentPermissionsSerializer,
            'env_ess': EssAgentAlldataAgentPermissionsSerializer,
            'env_tps': TpsAgentAlldataAgentPermissionsSerializer,
            'env_sbs': SbsAgentAlldataAgentPermissionsSerializer,
            'env_tptf': TptfAgentAlldataAgentPermissionsSerializer,
            'env_mm': MmAgentAlldataAgentPermissionsSerializer

        }

        true_columns = [column for column in columns_serializers.keys() if getattr(page_permission_obj, column)]

        if len(true_columns) > 0:
            agent_data_objs = Agent_data.objects.filter(org_location=user_location_obj.id, organization_id=user_org_obj, updated_plan_id = plan_id)

            # Filter out None and "null" values from indices_data updated code
            indices_data = []
            for agent_data_obj in agent_data_objs:
                for column in true_columns:
                    serializer = columns_serializers[column](agent_data_obj)
                    column_values = serializer.data.values()
                    valid_values = [value for value in column_values if value is not None and value != "null"]
                    indices_data.extend(valid_values)

            return Response({"message_type": "success", "data": {"indices": indices_data}})
        else:
            return Response({"message_type": "env type is not true"})

# To search api innovative
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def InnovativeSearchApi(request):
    index_name = request.GET.get('index_name')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    if not index_name:    
        return Response({"message_type":"d_not_f", "errors": "index_name_required"})

    column_name = request.GET.get('col_name')
    search_val = request.GET.get('search_val')
    _limit = request.GET.get('limit')
    _offset = request.GET.get('offset')
    res_json = {}
    check_params = True
   
    if column_name == "" or column_name is None:
        check_params = False
        res_json = {"message_type": "s_is_wrong", "col_name": "required", "message": "this param is required."}
       
    if search_val == "" or search_val is None:
        check_params = False
        res_json = {"message_type": "s_is_wrong", "search_val": "required", "message": "this param is required."}
    
    if _limit is None:
        _limit = 10
    else:    
        _limit = int(_limit)
       
    if _offset is None:
        _offset = 0
    else:
        _offset = int(_offset)

    
    if check_params :
        search_query = f"SELECT * from {index_name}-* WHERE {column_name} = '{search_val}' ORDER BY attack_epoch_time DESC LIMIT {_limit} OFFSET {_offset}"
        
        sql_query = opensearch_conn_using_db(search_query, location_id, plan_id)
        check_query_length = sql_query.get("total")
        
        if sql_query.get("total") in [0,None]:
            check_query_length = 0

        if check_query_length > 0:
            
            key_names = []
            for i in range(len(sql_query.get('schema'))):
                key_names.append(sql_query.get('schema')[i].get('name'))
            query_output = []
            for i in range(len(sql_query.get('datarows'))):
                row = sql_query.get('datarows')[i]
                query_output.append(dict(zip(key_names, row)))
            for i,n in enumerate(query_output):
                if "ids_threat_severity" in n:
                    if n['ids_threat_severity'] == 1.0:
                        n['ids_threat_severity'] = 'High'
                    elif n['ids_threat_severity'] == 2.0:
                        n['ids_threat_severity'] = 'Medium'
                    else:
                        n['ids_threat_severity'] = 'Low'  
                else:
                    pass      
            res_json = {"message_type":"data_ok","data":query_output}
        else:
            res_json = {"message_type": "data_not_found", "message": "query output is empty"}
       
    return Response(res_json)

class ApiSetData(APIView):
    authentication_classes = [ApiWithKeyAuth]
    def post(self, request, format=None):
        index = request.data.get("index")
        alert_data = request.data.get("alert_data")
        if index is None:
            return Response({"msg":"index params is empty.","error":"index"})
        if alert_data is None:
            return Response({"msg":"alert data params is empty.","error":"alert_data"})
        check_db = save_data(alert_data,index)
        return Response(check_db)

# To change language in profile login section api with dynamic
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dashboard_lang_update(request):
    try:
        clientObj = Client_data.objects.get(id = request.user.id)
        serializer = Client_Language_Serializer(clientObj,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            api_logs_make(request,"client_language_update","language profile section updated")
            return Response({"message_type":"updated","data":serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"message_type":"form_errors","errors":serializer.errors}, status=status.HTTP_200_OK)  
    except Client_data.DoesNotExist:
        return Response({"message_type":"user_id_not_found"})

# To show api change language in profile login section  
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboar_lang(request):
    try:
        clientObj = Client_data.objects.get(id = request.user.id)
        serializer = Client_Language_Serializer(clientObj)
        return Response({"message_type":"data_found","data":serializer.data})
    except ObjectDoesNotExist:
        return Response({"message_type":"d_not_f"})

# To display page_permissions api
class DisplayPagePermissionsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        res_msg = {}
        try:
            user_location_obj = request.user.location_id
            plan_id = user_location_obj.activated_plan_id
            query_result = Page_Permissions.objects.get(location_id = user_location_obj.id, updated_plan_id = plan_id.id)
            serializer_var = PagePermissionsSerializer(query_result)
            res_msg = {"message_type":"success","data":serializer_var.data}
        except ObjectDoesNotExist:
            res_msg = {"message_type":"d_not_f"}

        return Response(res_msg)
   
def convert_to_kolkata_time(utc_time_str):
    # Convert UTC string to datetime object
    utc_time = datetime.strptime(utc_time_str, '%Y-%m-%d %H:%M:%S')

    # Create timezone objects for UTC and Asia/Kolkata
    utc_tz = pytz.timezone('UTC')
    kolkata_tz = pytz.timezone('Asia/Kolkata')

    # Convert UTC datetime to Asia/Kolkata datetime
    kolkata_time = utc_tz.localize(utc_time).astimezone(kolkata_tz)

    # Format the Asia/Kolkata datetime as a string
    kolkata_time_str = kolkata_time.strftime('%Y-%m-%d %H:%M:%S')

    return kolkata_time_str



class Check_Api(APIView):    
    def get(self, request):
        
        key_names_email = []
        final_response = []
        queryCheck = query("SELECT ids_threat_class,target_os,attacker_ip, target_ip, count(attacker_ip) attacker_ip_count, attack_timestamp, attack_epoch_time FROM xdr-logs-whizhack-* WHERE attacker_ip IS NOT NULL and platform IN('aws','azure','onpremise') and ids_threat_severity IN(1,2,3) GROUP BY ids_threat_class,target_os,attacker_ip,target_ip, attack_timestamp, attack_epoch_time ORDER BY attack_epoch_time  desc limit 1000")

        check_query_length = queryCheck.get("total")

        format = "%Y-%m-%d %H:%M:%S"

        isoTime = datetime.now().isoformat()

        global_utc_now = datetime.now().utcnow()
        global_UTC_now = global_utc_now.strftime(format)
        

        if queryCheck.get("total") is None:
            check_query_length = 0

        if check_query_length > 0:
            for i in range(0, len(queryCheck.get('schema'))):
                if i == 4:
                    key_names_email.append(queryCheck.get('schema')[i].get('alias'))
                else:
                    key_names_email.append(queryCheck.get('schema')[i].get('name'))
                
            for i in range(0, len(queryCheck.get('datarows'))):
                row = queryCheck.get('datarows')[i]
                final_response.append(dict(zip(key_names_email, row)))
                
                final_response.append({"convert_to_kolkata_time":convert_to_kolkata_time(row[5]),"ISO Now":isoTime, "UTC Now":global_UTC_now})
        
        return Response(final_response)
    

# To add blacklisted detials with updated    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_classes_blacklist(request):
    try:
        blacklisted_classes = request.data.get('blacklisted_class', [])  # Get list of blacklisted classes
        blacklisted_ips = request.data.get('blacklisted_ip', [])

        # Convert blacklisted classes to tuple
        blacklisted_classes_tuple = tuple(blacklisted_classes) if blacklisted_classes else None
        if blacklisted_classes_tuple and len(blacklisted_classes_tuple) == 1:
            blacklisted_classes_tuple = f"('{blacklisted_classes_tuple[0]}')"

        # Convert blacklisted IPs to tuple
        blacklisted_ips_tuple = tuple(blacklisted_ips) if blacklisted_ips else None
        if blacklisted_ips_tuple and len(blacklisted_ips_tuple) == 1:
            blacklisted_ips_tuple = f"('{blacklisted_ips_tuple[0]}')"

        clientObj = request.user
        location_instance = clientObj.location_id
        org_instance = location_instance.org_id

        isodatetime = datetime.now(pytz.timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')
        
        blacklist_data = blacklisted_data.objects.filter(location_id = location_instance.id).first() #here purposely plan_id is not filtered so that if plan_id is null then new record shouldn't be added
        
        # if plan_id is None then also update
        if blacklist_data is not None:
            # Existing record, update the record
            message_type = "updated"
            message = "blacklisted record already exists, blacklisted record updated"
            blacklist_data.updated_at = isodatetime  # Update the 'updated_at' field
            blacklist_data.location_id = location_instance
            blacklist_data.user_id = clientObj
            blacklist_data.org_id = org_instance  # Assign the organization instance
            blacklist_data.blacklisted_class = blacklisted_classes_tuple
            blacklist_data.blacklisted_ip = blacklisted_ips_tuple
            blacklist_data.updated_plan_id = location_instance.activated_plan_id
            blacklist_data.save()

            serializer_var = AddBlacklistedDetailsSerializer(blacklist_data)
            response_data = {"message_type": message_type,"message": message,"data": serializer_var.data}

        else:
            # Create the BlacklistedData object and save it
            message_type = "added"
            message = "new blacklisted record created"
            new_blacklisted_record = blacklisted_data(
                user_id = clientObj,
                created_at = isodatetime,
                location_id = location_instance,
                org_id = org_instance,
                blacklisted_class = blacklisted_classes_tuple,
                blacklisted_ip = blacklisted_ips_tuple,
                updated_plan_id = location_instance.activated_plan_id
            )
            new_blacklisted_record.save()
            serializer_var = AddBlacklistedDetailsSerializer(new_blacklisted_record)
            response_data = {"message_type": message_type,"message": message,"data": serializer_var.data}

        return Response(response_data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message_type": "s_is_wrong"})

# To display classes type (blacklisted details) with updated
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def display_blacklisted_details(request):
    user_location_obj = request.user.location_id
    plan_id = user_location_obj.activated_plan_id
    try:
        blacklistedObj = blacklisted_data.objects.get(location_id = user_location_obj.id, updated_plan_id = plan_id.id)
        serializer = GetBlacklistedDetailsSerializer(blacklistedObj)

        updated_data = serializer.data

        # Check if blacklisted_class exists in the database
        if 'blacklisted_class' in updated_data:
            blacklisted_class_str = updated_data['blacklisted_class']
            if blacklisted_class_str is not None:
                blacklisted_class_list = ast.literal_eval(blacklisted_class_str)
                if isinstance(blacklisted_class_list, str):
                    blacklisted_class_list = [blacklisted_class_list]
                blacklisted_class_list = [item.strip("'") if item is not None else "" for item in blacklisted_class_list if isinstance(item, str)]
                blacklisted_class_list = [item for item in blacklisted_class_list if item]  # Remove empty values from the list
            else:
                blacklisted_class_list = []
            updated_data['blacklisted_class'] = blacklisted_class_list
        else:
            updated_data['blacklisted_class'] = []

        # Check if blacklisted_ip exists in the database
        if 'blacklisted_ip' in updated_data:
            blacklisted_ip_str = updated_data['blacklisted_ip']
            if blacklisted_ip_str is not None:
                blacklisted_ip_list = ast.literal_eval(blacklisted_ip_str)
                if isinstance(blacklisted_ip_list, str):
                    blacklisted_ip_list = [blacklisted_ip_list]
                blacklisted_ip_list = [item.strip("'") if item is not None else "" for item in blacklisted_ip_list if isinstance(item, str)]
                blacklisted_ip_list = [item for item in blacklisted_ip_list if item]  # Remove empty values from the list
            else:
                blacklisted_ip_list = []
            updated_data['blacklisted_ip'] = blacklisted_ip_list
        else:
            updated_data['blacklisted_ip'] = []

        # Additional condition to remove commas from blacklisted_class
        if 'blacklisted_class' in updated_data:
            blacklisted_class = updated_data['blacklisted_class']
            if isinstance(blacklisted_class, str):
                blacklisted_class = blacklisted_class.replace(",", "")
                updated_data['blacklisted_class'] = blacklisted_class

        return Response({"message_type": "data_found", "data": updated_data})

    except ObjectDoesNotExist:
        return Response({"message_type": "d_not_f"})    

# To get indices name basis on env_type in page_permission models from agent-details models
class IndicesNameView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        condition = request.GET.get('condition_type')
        past_time, current_time = calculate_start_end_time(condition)
        _limit = request.GET.get("limit")
        if not past_time:
            return Response({"message_type": "d_not_f", "err": "invalid_condition"})

        if _limit is None:
            _limit = 100
        else:
            _limit = int(_limit)
        final_response = []  # Initialize final_response with an empty list

        try:
            user_location_obj = request.user.location_id
            plan_idObj = request.user.location_id.activated_plan_id
            if plan_idObj is not None:
                plan_id = plan_idObj.id
            else:
                return Response({"message_type": "d_not_f", "err": "plan_id_n_found"})
            
            page_permission_obj = Page_Permissions.objects.get(location_id=user_location_obj.id, updated_plan_id = plan_id)
            user_org_obj = str(request.user.organization_id)
        except ObjectDoesNotExist:
            return Response({"message_type": "d_not_f", "err": "location_n_found"})

        columns_serializers = {
            'env_hids': AlldataAgentPermissionsSerializer,
            'env_nids': NidsAlldataAgentPermissionsSerializer,
            'env_trace': TraceAlldataAgentPermissionsSerializer,
            'env_wazuh': WazuhAlldataAgentPermissionsSerializer,
            'env_hc': HealthCheckAlldataAgentPermissionsSerializer,
            'env_soar': SoarAlldataAgentPermissionsSerializer,
            'env_ess': EssAgentAlldataAgentPermissionsSerializer,
            'env_tps': TpsAgentAlldataAgentPermissionsSerializer,
            'env_sbs': SbsAgentAlldataAgentPermissionsSerializer,
            'env_tptf': TptfAgentAlldataAgentPermissionsSerializer,
            'env_mm': MmAgentAlldataAgentPermissionsSerializer

        }

        true_columns = [column for column in columns_serializers.keys() if getattr(page_permission_obj, column)]

        if len(true_columns) > 0:
            agent_data_objs = Agent_data.objects.filter(org_location=user_location_obj.id, organization_id=user_org_obj, updated_plan_id = plan_id)

            # indices_data = []
            # print(f"indices_data: {indices_data}")
            # for agent_data_obj in agent_data_objs:
            #     for column in true_columns:
            #         serializer = columns_serializers[column](agent_data_obj)
            #         column_values = serializer.data.values()
            #         indices_data.extend(column_values)

            # Filter out None and "null" values from indices_data updated code
            indices_data = []
            for agent_data_obj in agent_data_objs:
                for column in true_columns:
                    serializer = columns_serializers[column](agent_data_obj)
                    column_values = serializer.data.values()
                    valid_values = [value for value in column_values if value is not None and value != "null"]
                    indices_data.extend(valid_values)

            indices_with_alert_key = [index for index in indices_data if "alert" in index]
          
            if len(indices_with_alert_key) > 0:
                first_index = indices_with_alert_key[0]
                first_index_table = first_index
                queryfunc = f"SELECT * FROM {first_index_table}-* where timestamp >= {past_time} AND timestamp <= {current_time} ORDER BY timestamp DESC LIMIT {_limit};"
                
                run_sql = opensearch_conn_using_db(queryfunc, user_location_obj, plan_id)

                if run_sql.get("total") not in [0,None]:
                    key_names = []
                    for i, n in enumerate(run_sql.get('schema')):
                        if n.get('name') == 'id':
                            key_names.append('_id')
                        else:
                            key_names.append(n.get('name'))

                    for i in range(len(run_sql.get('datarows'))):
                        row = run_sql.get('datarows')[i]
                        item_dict = dict(zip(key_names, row))
                        final_response.append(item_dict)
                    return Response({"message_type": "success", "data": {"indices": indices_data, "default_index": first_index, "default_data": final_response}})
                else:
                    return Response({"message_type": "success","data": {"indices": indices_data, "default_index": first_index, "default_data": final_response}})
            else:
                return Response({"message_type": "d_not_f", "err": "agent_data_obj_empty"})
        else:
            return Response({"message_type": "d_not_f", "err": "env_type_not_true"})

# To get indice filters name updated code
@parser_classes([JSONParser])
class FilterIndiceData(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        index_name = request.GET.get('index_name')
        condition = request.GET.get('condition_type')
        past_time, current_time = calculate_start_end_time(condition)
        _limit = request.GET.get('limit')
        location_id = request.user.location_id.id
        plan_idObj = request.user.location_id.activated_plan_id

        if plan_idObj is not None:
            plan_id = plan_idObj.id
        else:
            return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
        
        if _limit is None:
            _limit = 100
        else:
            _limit = int(_limit)
        
        if not index_name:
            return Response({"message_type":"index_name required", "errors": "index_name is not empty"})
        
        if not condition:
            return Response({"message_type":"condition required", "errors": "condition is not empty"})
        
        queryfunc = f"SELECT * FROM {index_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} ORDER BY attack_epoch_time DESC LIMIT {_limit};"
        
        api_response = opensearch_conn_using_db(queryfunc, location_id, plan_id)
        if api_response.get("total") not in [0,None]:
            key_names = []
            for i,n in enumerate(api_response.get('schema')):
                if n.get('name') == 'id':
                    key_names.append('_id')
                else:
                    key_names.append(n.get('name'))

            final_response = []
            for i in range(len(api_response.get('datarows'))):
                row = api_response.get('datarows')[i]
                final_response.append(dict(zip(key_names, row)))
            return Response({"message_type": "success", "data":final_response})
        else:
            return Response({"message_type": "d_not_f"})
        

# To get soar locense management details basis on user id within location_id    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def soar_urls_details(request):
    try:
        client_obj = get_object_or_404(Client_data, id=request.user.id)
        location_obj = client_obj.location_id
        activated_plan_id = location_obj.activated_plan_id
        try:
            soar_query = Soar_License_Management.objects.get(updated_plan_id=activated_plan_id)
        except Soar_License_Management.DoesNotExist:
            return Response({"message_type": "d_not_f"}) # license not found
        serializer = SoarLicenseUrlsPlanStepThreeSerializer(instance=soar_query)
        response_msg = {"message_type": "success","data":serializer.data}
    except Exception:
        response_msg = {"message_type": "d_not_f"}
    return Response(response_msg)

# dynamic filter condition report section
@parser_classes([JSONParser])
class DynamicReportFilter(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        index_name = request.data.get('index_name')
        _limit = request.data.get('limit')
        get_offset = request.data.get("offset")
        offset = f"OFFSET {get_offset}" if get_offset else ''
        time_filter = request.data.get('time_filter')
        query = request.data.get('query')

        past_time, current_time = calculate_start_end_time(time_filter)
        location_id = request.user.location_id.id
        plan_idObj = request.user.location_id.activated_plan_id
        
        if plan_idObj is not None:
            plan_id = plan_idObj.id
        else:
            return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
        
        if _limit is None:
            _limit = 100
        else:
            _limit = int(_limit)
        
        if not index_name:
            return Response({"message_type":"d_not_f", "errors": "index_name_required"})
        
        if not _limit:
            return Response({"message_type":"d_not_f", "errors": "limit_required"})
        
        if not time_filter:
            return Response({"message_type":"d_not_f", "errors": "time_filter_required"})

        if not query:# default query if "query" has empty value in payload
            dynamic_sql = f'''SELECT * FROM {index_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} ORDER BY attack_epoch_time DESC LIMIT {_limit} {offset};'''
        else:
        
            dynamic_sql = f'''SELECT * FROM {index_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}'''

            for condition in query:
                where_clause = condition.get('condition', '')
                
                if where_clause == '':
                    return Response({"message_type":"d_not_f", "errors": "condition_required"})

                field = condition.get('column_name', '')
                
                if field == '':
                    return Response({"message_type":"d_not_f", "errors": "field_required"})
                
                if "value" in condition:
                    match_value = condition.get('value', '')
                
                if (where_clause in ('is', 'is_not')) and (match_value == ''):
                    return Response({"message_type":"d_not_f", "errors": "value_required"})
                
                # converting match value to format with round brackets for sql query
                if (field == 'rule_gpg13'):
                    match_value_tuple = '(' + ', '.join([f"'{str(element)}'" for element in match_value]) + ')'
                else:
                    match_value_tuple = str(match_value).replace("[", "(").replace("]", ")")

                if where_clause == 'is':
                    dynamic_sql += f''' AND {field} IN {match_value_tuple} ''' 

                elif where_clause == 'is_not':
                    dynamic_sql += f''' AND {field} NOT IN {match_value_tuple} '''

                elif where_clause == 'is_not_null':
                    dynamic_sql += f" AND {field} IS NOT NULL"
                elif where_clause == 'is_null':
                    dynamic_sql += f" AND {field} IS NULL"

            dynamic_sql += f" ORDER BY attack_epoch_time DESC LIMIT {_limit} {offset};"

        api_response = opensearch_conn_using_db(dynamic_sql, location_id, plan_id)

        if api_response.get("total") not in [0,None]:
            key_names = []
            for i,n in enumerate(api_response.get('schema')):
                if n.get('name') == 'id':
                    key_names.append('_id')
                else:
                    key_names.append(n.get('name'))

            final_response = []
            for i in range(len(api_response.get('datarows'))):
                row = api_response.get('datarows')[i]
                final_response.append(dict(zip(key_names, row)))

            return Response({"message_type": "success", "data":final_response})
        else:
            return Response({"message_type": "d_not_f"})

# To get report config logs indices name 
class Report_Config_Display_Log_Indice(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_location_obj = request.user.location_id
            page_permission_obj = Page_Permissions.objects.get(location_id=user_location_obj.id)
            user_org_obj = str(request.user.organization_id)
        except ObjectDoesNotExist:
            return Response({"message_type": "location not found"})

        columns_serializers = {
            'env_hids': RpoertAlldataAgentPermissionsSerializer,
            'env_nids': ReportNidsAlldataAgentPermissionsSerializer,
            'env_trace': ReportTraceAlldataAgentPermissionsSerializer,
        }
        true_columns = [column for column in columns_serializers.keys() if getattr(page_permission_obj, column)]
        product_name = request.GET.get('product_name')
        if product_name in true_columns:
            # Fetch the serializer based on the chosen product_name
            column_serializer = columns_serializers[product_name]
            agent_data_objs = Agent_data.objects.filter(org_location=user_location_obj.id, organization_id=user_org_obj)
            indices_data = set()
            for agent_data_obj in agent_data_objs:
                serializer = column_serializer(agent_data_obj)
                indices_data.update(serializer.data.values())

            return Response({"message_type": "success", "indices": indices_data})
        else:
            return Response({"message_type": "env type is not true"})

# To get only column name of indices only
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def report_config_indice_fields_records(request):
    try:
        location_id = request.user.location_id.id
    except AttributeError:
        return Response({"message_type": "d_not_f", "err": "location_id_n_found"})
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id
    index_name= request.GET.get('index_name')
    condition ="last_7_days" # last 7 day recoreds static
    past_time, current_time = report_config_calculate_start_end_time(condition)
    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "err": "plan_id_n_found"})
    
    if not index_name:
        return Response({"message_type":"index_name required", "errors": "index_name is not empty"})
    
    queryfunc = f"SELECT * FROM {index_name}-* where attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time};"
    api_response = opensearch_conn_using_db(queryfunc, location_id, plan_id)
    if api_response.get("total") not in [0,None]:
        key_names = []
        for i, n in enumerate(api_response.get('schema')):
            if n.get('name') == 'id':
                key_names.append('_id')
            else:
                key_names.append(n.get('name'))

        # Return only the column names
        return Response({"message_type": "success", "columns": key_names})
    else:
        return Response({"message_type": "d_not_f"})
    

# Seond method process
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mail_pdf_save_details(request):
    # Get the user from the request
    user = request.user

    # Ensure the user has a valid location_id, either set during registration or profile update
    location_id = user.location_id  # This assumes 'location_id' is an attribute of your user model
    if location_id is None:
        return Response({"message": "User's location is not set"}, status=status.HTTP_400_BAD_REQUEST)

    email_ids = request.data.get('email_ids')

    # Set default values for report_format_id and is_active
    report_format_id = 1  # weekly = 1, monlthly = 2, daily = 3
    is_active = True

    # Create a dictionary with the extracted data
    data = {
        'user': user.id,
        'location_id': location_id.id,
        'plan_id': location_id.activated_plan_id.id,
        'org_id': location_id.org_id.organization_id,
        # 'email_ids': ','.join(email_ids),
        'email_ids': email_ids,
        'report_format_id': report_format_id,
        'is_active': is_active,
    }

    query_update = ReportSchedulerClientDetails.objects.filter(location_id=location_id.id).first()

    # Create a serializer with the extracted data
    serializer = PdfMailDetailsSerializer(data=data)

    if query_update:  # If location_id exists
        if serializer.is_valid():
            # Update the details in the database
            query_update.email_ids = data['email_ids']
            query_update.save()

            return Response({"message": "Details updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:  # If location_id doesn't exist
        if serializer.is_valid():
            # Save the details to the database
            serializer.save()
            return Response({"message": "Details inserted"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mail_pdf_save_details(request):
    # Get the user from the request
    user = request.user

    # Ensure the user has a valid location_id, either set during registration or profile update
    location_id = user.location_id  # This assumes 'location_id' is an attribute of your user model
    if location_id is None:
        return Response({"message": "User's location is not set"}, status=status.HTTP_400_BAD_REQUEST)

    email_ids = request.data.get('email_ids')
    # schedule_name = request.GET.get
    # Set default values for report_format_id and is_active
    report_format_id = 1  # weekly = 1, monlthly = 2, daily = 3
    is_active = True

    # Create a dictionary with the extracted data
    data = {
        'user': user.id,
        'location_id': location_id.id,
        'plan_id': location_id.activated_plan_id.id,
        'org_id': location_id.org_id.organization_id,
        # 'email_ids': ','.join(email_ids),
        'email_ids': email_ids,
        'report_format_id': report_format_id,
        'is_active': is_active,
    }

    query_update = ReportSchedulerClientDetails.objects.filter(location_id=location_id.id).first()

    # Create a serializer with the extracted data
    serializer = PdfMailDetailsSerializer(data=data)

    if query_update:  # If location_id exists
        if serializer.is_valid():
            # Update the details in the database
            query_update.email_ids = data['email_ids']
            query_update.save()

            return Response({"message": "Details updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:  # If location_id doesn't exist
        if serializer.is_valid():
            # Save the details to the database
            serializer.save()
            return Response({"message": "Details inserted"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# To save scheduler name in to date format db
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_date_time(request):
    serializervariable = SaveDateSerializer(data=request.data)
    if serializervariable.is_valid():
        serializervariable.save()
        # api_logs_make(request,"email config","new email added")
        
        return Response({"message_type":"successfully_inserted","message": "Successfully inserted data in db"}, status=status.HTTP_200_OK)
    else:
        return Response({"message_type":"unsuccessful","message": "Data was not inserted"}, status=status.HTTP_400_BAD_REQUEST)

# To get details of scheduler details
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def display_save_date_time(request):
    # Assuming Date_Month_Week_Details is a model in your Django app
    query_scheduler = ReportSchedulerTimeFormat.objects.all()
    # Check if there is any data in the queryset
    if not query_scheduler.exists():
        return Response({"message_type": "d_n_f", "message": "No data found"}, status=status.HTTP_404_NOT_FOUND)
    serializervariable = AllDetailsSaveDateSerializer(query_scheduler, many=True)
    serialized_data = serializervariable.data

    return Response({"message_type": "data_found", "data": serialized_data}, status=status.HTTP_200_OK)

# To get multiple product_name basis details of indcies from agent_details models
class Testing_Display_Log_Indice(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_location_obj = request.user.location_id
            page_permission_obj = Page_Permissions.objects.get(location_id=user_location_obj.id)
            user_org_obj = str(request.user.organization_id)
        except ObjectDoesNotExist:
            return Response({"message_type": "location not found"})

        columns_serializers = {
            'env_hids': AlldataAgentPermissionsSerializer,
            'env_nids': NidsAlldataAgentPermissionsSerializer,
            'env_trace': TraceAlldataAgentPermissionsSerializer,
            'env_wazuh': WazuhAlldataAgentPermissionsSerializer,
            'xdr_live_map': network_map_serializer,
        }

        # Get the 'product_name' parameter
        product_name_param = request.GET.get('product_name', '')
        if product_name_param is None or not product_name_param.strip():
            return Response({"message": "product_name not provided or is empty"}, status=status.HTTP_400_BAD_REQUEST)

        # Split the parameter into a list of product names
        product_names = [name.strip() for name in product_name_param.split(',') if name.strip()]
        # Validate that all product names are valid
        if not all(product_name in columns_serializers for product_name in product_names):
            return Response({"message_type": "Invalid product_name(s)"})

        combined_logs = set()

        for product_name in product_names:
            # Fetch the serializer based on the chosen product_name
            column_serializer = columns_serializers[product_name]
            agent_data_objs = Agent_data.objects.filter(org_location=user_location_obj.id, organization_id=user_org_obj)

            for agent_data_obj in agent_data_objs:
                serializer = column_serializer(agent_data_obj)
                combined_logs.update(serializer.data.values())

        return Response({"message_type": "success", "indices": list(combined_logs)})

# To display api  details from updated_api_export models
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def updated_display_third_party_api(request):
    try:
        results = Updated_Api_export.objects.filter(client_id=request.user.id)
        serializer = all_create_api_serializer(results, many=True)
        product_display_formats = {
            "env_trace": "TRACE",
            "env_wazuh": "WAZUH",
            "env_hids": "HIDS",
            "env_nids": "NIDS"
        }

        response_data = []

        # Process the serializer data
        for data in serializer.data:
            logs_name_str = data.get('product_logs_name')
            product_name_str = data.get('product_name')
            logs_name_list = ast.literal_eval(logs_name_str)
            data['product_logs_name'] = logs_name_list

            # Convert the product_name string to a list
            product_name_list = ast.literal_eval(product_name_str)

            # Process each log name in the logs_name_list
            processed_logs_name = []
            for log_name_item in logs_name_list:
                parts = log_name_item.split('-')
                display_name_parts = []

                for part in parts:
                    if part == 'xdr':
                        continue
                    # Remove the pattern "Whi Whigur4386" from each part
                    part = part.split('-')[0]
                    display_name_parts.append(part.title())  # Capitalize first letter, lowercase rest
                display_name_lower = ' '.join(display_name_parts[:2])
                display_name = display_name_lower.replace(" ", " ")
                processed_logs_name.append(display_name)

            # Format product_name_list using product_display_formats
            formatted_product_names = [product_display_formats.get(name, name) for name in product_name_list]

            data['url'] = "https://xdr-demo.zerohack.in/api/get-third-party-api"
            data['product_logs_name'] = processed_logs_name
            data['product_name'] = formatted_product_names  # Assign the formatted product_names
            response_data.append(data)

        return Response({"message_type": "data_found", "data": response_data})
    except ObjectDoesNotExist:
        return Response({"message_type": "d_not_f"})

# Using this api third persion using details of data behalf of api_key 
class Testing_Updated_Xdr_api(APIView):
    authentication_classes = [UpdatedApiWithKeyAuth]

    def get(self, request, format=None):
        api_key_val = request.headers.get('Key')
        query_api_axport = Updated_Api_export.objects.get(api_key=api_key_val)

        log_name = query_api_axport.product_logs_name
        client_id = query_api_axport.client_id_id
        clientObj = Client_data.objects.get(id=client_id)
        location_id = clientObj.location_id.id
        
        plan_id = clientObj.location_id.activated_plan_id.id
        logs_name_list = ast.literal_eval(log_name)

        # Get the provided start_date and end_date from the request, if available
        start_date_val = request.GET.get("start_date")
        end_date_val = request.GET.get("end_date")

        if start_date_val and end_date_val:
            # If both start_date and end_date are provided, use the provided values
            past_time_epoch = get_time_zone(start_date_val)[1]
            current_time_epoch = get_time_zone(end_date_val)[1]
        else:
            # If either start_date or end_date is missing, calculate past_time and current_time dynamically
            current_time = datetime.now()
            past_time = current_time - timedelta(days=7)
            past_time_epoch = int(past_time.timestamp()) * 1000
            current_time_epoch = int(current_time.timestamp()) * 1000

        get_limit = request.GET.get("limit")
        limit = f"LIMIT {get_limit}" if get_limit else ''

        get_offset = request.GET.get("offset")
        offset = f"OFFSET {get_offset}" if get_offset and get_limit else ''

        start_date = f"WHERE (attack_epoch_time >= {past_time_epoch})"
        end_date = f"AND (attack_epoch_time <= {current_time_epoch})"
        order_by_val = request.GET.get("order_by", "desc")  # Set "desc" as default value for order_by_val
        order_by = f"ORDER BY attack_epoch_time {'ASC' if order_by_val == 'asc' else 'DESC'}"

        final_response = []  # Initialize an empty list to store the final response data

        for log_name_item in logs_name_list:
            if isinstance(log_name_item, dict):
                log_name_item_key = log_name_item.get("key", "")
            else:
                log_name_item_key = log_name_item

            formed_sql = f"SELECT * FROM {log_name_item_key}-* {start_date} {end_date} {order_by} {limit} {offset};"

            try:
                api_response = opensearch_conn_using_db(formed_sql, location_id, plan_id)
            except Exception as e:
                api_response = None

            # Check if the API response is None (error occurred) or empty (no data)
            if api_response is None or not api_response.get('datarows'):
                display_name = self.get_display_name(log_name_item_key)
                final_response.append({
                    "index_name": display_name,
                    "data_len": 0,
                    "index_data": []
                })
                continue

            schema_data = api_response.get('schema')
            if schema_data is None:
                # Handle the case when the 'schema' key is not present or its value is None
                continue

            key_names = [field['name'] for field in schema_data]
            current_index_data = []
            for row in api_response.get('datarows'):
                current_row_data = dict(zip(key_names, row))
                current_index_data.append(current_row_data)

            display_name = self.get_display_name(log_name_item_key)

            # Include the index in the response with an empty list if it has no data
            if current_index_data:
                final_response.append({
                    "index_name": display_name,
                    "data_len": len(current_index_data),
                    "index_data": current_index_data
                })
            else:
                final_response.append({
                    "index_name": display_name,
                    "data_len": 0,
                    "index_data": []
                })

        # Check if any index has data
        has_data = any(response["data_len"] > 0 for response in final_response)

        if has_data:
            return Response({"message_type": "success", "data": final_response})
        else:
            return Response({"message_type": "success", "data": []})

    def get_display_name(self, log_name_item):
        parts = log_name_item.split('-')
        display_name_parts = []

        for part in parts:
            if part == 'xdr':
                continue
            # Remove the pattern "Whi Whigur4386" from each part
            part = part.split('-')[0].lower()
            display_name_parts.append(part)
        display_name_val = ' '.join(display_name_parts)
        val_abc = display_name_val.split()
        display_name_lower = ' '.join(val_abc[:2])
        display_name = display_name_lower.replace(" ", "-")
        return display_name


# To create third party api to save details into updated_api_export models
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def updated_third_party_api_create_api_key(request):
    api_key_gen = str(uuid.uuid4()) + "-" + str(uuid.uuid4())
    product_name_var = request.data.getlist('product_types[]', [])


    api_type = request.data.get('api_type')  # get(1) and post method(2)
    logs_name = request.data.getlist('log_type[]', [])  # Use getlist to get multiple values
    if not product_name_var:
        return Response({"message_type": "product_name_var", "errors": "product_name"}, status=status.HTTP_400_BAD_REQUEST)

    if not api_type:
        return Response({"message_type": "missing_api_type_field", "errors": "api_type field is required"}, status=status.HTTP_400_BAD_REQUEST)

    if not logs_name:
        return Response({"message_type": "missing_logs_name_field", "errors": "logs_name field is required"}, status=status.HTTP_400_BAD_REQUEST)

    req_data = {
        "client_id": request.user.id,
        "api_key": api_key_gen,
        'api_key_status': True,
        'product_name':  str(product_name_var),
        'api_type': api_type,
        'product_logs_name': str(logs_name)  # Save the list directly
    }
    serializer = create_api_serializer(data=req_data)
    if serializer.is_valid():
        serializer.save()
        req_data['product_logs_name'] = ast.literal_eval(req_data['product_logs_name'])
        req_data['product_name'] = ast.literal_eval(req_data['product_name'])

        api_logs_make(request, "create_third_party_api", "Create new third party API key")
        return Response({"message_type": "created", "data": req_data}, status=status.HTTP_200_OK)
    else:
        return Response({"message_type": "form_errors", "errors": serializer.errors}, status=status.HTTP_200_OK)


