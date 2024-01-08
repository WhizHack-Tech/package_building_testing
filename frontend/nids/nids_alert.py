#  ==============================================================================================================================
#  File Name: nids_alert.py
#  Description: It contains all the code for each chart on NIDS Alerts page under NIDS tab on Client Dashboard.
#  Active URL: https://xdr-demo.zerohack.in/nids/alerts

#  ------------------------------------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  =============================================================================================================================
from ..helpers import getIndexNameByLocationId, getPlatformAndBlacklistedItemsByLocationId, getMlDlAccuracyRanges
from ..time_filter_on_queries import calculate_start_end_time
from ..grouping_epoch_time import *
from ..opensearch_config import opensearch_conn_using_db
from rest_framework.decorators import api_view
from rest_framework.response import Response
from collections import defaultdict
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from ..crypt_func import encrypt, decrypt
import json

# list containing values to exclude from each query--> to avoid error on frontend page
exclude_values = [0,None]

#1.a Card Name: Critical Threats---from nids dashboard page
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_critical_threats(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})

    platform_tuple = detail_dict.get("platform_tuple")
    platform_query = f"AND platform IN {platform_tuple} " if platform_tuple is not None else ""

    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    threat_class_tuple = ('Lateral Movement','External Attack','Attack on External Server','Internal Compromised Machine')
    
    sql_query = f"SELECT type_of_threat, attack_epoch_time FROM {indice_name}-* WHERE type_of_threat IN {threat_class_tuple} "+platform_query+s1+s2+f" AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL ORDER BY attack_epoch_time DESC limit 200000;"
    
    search2 = opensearch_conn_using_db(sql_query, location_id, plan_id)
    
    if search2.get("total") not in exclude_values:

    # formatting sql_query query output as (key, value) pairs in dictionary
        key_names = [item['name'] for item in search2.get('schema')]
        
        table_query_list = []
        for i, row in enumerate(search2.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
        
        # to create series
        epoch_interval_group_list = getEpochIntervalGroupList(condition, past_time, current_time)

        if epoch_interval_group_list is None:
            return Response({"message_type":"d_not_f", "errors": "condition_not_f"})
        
        # Create a dictionary with default values of 0 for time interval counts
        response_dict = defaultdict(lambda: [0] * len(epoch_interval_group_list))
        
        response_dict["message_type"] = "success"
        response_dict["total"] = len(table_query_list)
        
        for threat in ('Lateral Movement','Internal Compromised Machine'):
            filtered_dict = [dictionary for dictionary in table_query_list if dictionary.get('type_of_threat') == threat]
            
            if len(filtered_dict) == 0:
                threat_name = threat.lower().replace(" ", "_")
                response_dict[threat_name]
            else:
                for item in filtered_dict:
                    epoch_date = item["attack_epoch_time"]
                    for i, (start, end) in enumerate(epoch_interval_group_list):
                        if start <= epoch_date <= end:
                            threat_name = threat.lower().replace(" ", "_")
                            response_dict[threat_name][i] += 1
        
        
        # updating values for external threat in response_dict
        filtered_dict = [dictionary for dictionary in table_query_list if dictionary.get('type_of_threat') == 'External Attack' or dictionary.get('type_of_threat') == 'Attack on External Server']
        for item in filtered_dict:
            epoch_date = item["attack_epoch_time"]
            for i, (start, end) in enumerate(epoch_interval_group_list):
                if start <= epoch_date <= end:
                    response_dict["external_attack"][i] += 1

        # for grouping according to platform
        sql2 = f"SELECT platform, type_of_threat, count(type_of_threat) threat_count FROM {indice_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} "+platform_query+s1+s2+f" AND type_of_threat IN {threat_class_tuple} AND platform IS NOT NULL AND ids_threat_class IS NOT NULL GROUP BY platform, type_of_threat ORDER BY threat_count desc;"
    
        run_sql2 = opensearch_conn_using_db(sql2, location_id, plan_id)

        if run_sql2.get("total") not in [0, None]:

            key_names = []
            for i,n in enumerate(run_sql2.get('schema')):
                if n.get('name') == 'count(type_of_threat)':
                    key_names.append(n.get('alias'))
                else:
                    key_names.append(n.get('name'))
            
            table_query_list = []
            for i, key_values in enumerate(run_sql2.get('datarows')):
                if key_values[1] == "Attack on External Server":
                    key_values[1] = "External Attack"
                Dict = {}
                Dict.update(dict(zip(key_names, key_values)))
                Dict["past_time"] = past_time
                Dict["current_time"] = current_time

                table_query_list.append(Dict)

            response_dict["filter"] = table_query_list
            
        return Response(response_dict)
    else:
        return Response({"message_type":"d_not_f"})
    
#1.b Critical Threats Table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_critical_threats_table(request):
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    

    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    type_of_threat = request.GET.get('type_of_threat')
    platform_name = request.GET.get('platform')

    if type_of_threat == 'External Attack':
        threat_class_tuple = ('External Attack','Attack on External Server')
    else:
        threat_class_tuple = f"('{type_of_threat}')"
    
    if type_of_threat is None:
        return Response({"message_type": "d_not_f","errors": "type_of_threat_not_found"})
    
    if platform_name is None:
        return Response({"message_type": "d_not_f","errors": "platform_name_not_found"})
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    
    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT platform, type_of_threat, attacker_ip, attacker_mac, attack_timestamp, ids_threat_class, ids_threat_type, ml_threat_class, dl_threat_class, ml_accuracy, dl_accuracy, attacker_port, target_port, target_ip, geoip_city, geoip_country_name, geoip_asn_name FROM {indice_name}-* WHERE type_of_threat IN {threat_class_tuple} "+s1+s2+f" AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform = '{platform_name}' AND ids_threat_class IS NOT NULL ORDER BY attack_epoch_time DESC limit 200000;"
    
    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)

    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [item['name'] for item in run_sql.get('schema')]
    
        table_query_list = []
        for i, row in enumerate(run_sql.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
            
        return Response({"message_type":"success", "count":len(table_query_list), "type_of_threat":type_of_threat,"table":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})



#2.a Card Name: Lateral Movement
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_lateral_mov(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    platform_tuple = detail_dict.get("platform_tuple")
    platform_query = f"AND platform IN {platform_tuple} " if platform_tuple is not None else ""

    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    sql_query = f"SELECT type_of_threat, attack_epoch_time FROM {indice_name}-* WHERE type_of_threat = 'Lateral Movement' "+platform_query+s1+s2+f" AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL ORDER BY attack_epoch_time DESC limit 200000;"
    
    search2 = opensearch_conn_using_db(sql_query, location_id, plan_id)
    
    if search2.get("total") not in exclude_values:

    # # formatting sql_query query output as (key, value) pairs in dictionary
        key_names = [item['name'] for item in search2.get('schema')]
        
        table_query_list = []
        for i, row in enumerate(search2.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
        
        # to create series
        epoch_interval_group_list = getEpochIntervalGroupList(condition, past_time, current_time)

        if epoch_interval_group_list is None:
            return Response({"message_type":"d_not_f", "errors": "condition_not_f"})
        
        # Create a dictionary with default values of 0 for time interval counts
        response_dict = defaultdict(lambda: [0] * len(epoch_interval_group_list))
        # filter_list = []
        
        response_dict["message_type"] = "success"
        response_dict["total"] = len(table_query_list)
        
            
        if len(table_query_list) == 0:
                response_dict["lateral_movement"]
        else:
            for item in table_query_list:
                epoch_date = item["attack_epoch_time"]
                for i, (start, end) in enumerate(epoch_interval_group_list):
                    if start <= epoch_date <= end:
                        response_dict["lateral_movement"][i] += 1

        # for grouping according to platform
        sql2 = f"SELECT platform, type_of_threat, count(type_of_threat) threat_count FROM {indice_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} "+platform_query+s1+s2+f" AND type_of_threat = 'Lateral Movement' AND platform IS NOT NULL AND ids_threat_class IS NOT NULL GROUP BY platform, type_of_threat ORDER BY threat_count desc;"
    
        run_sql2 = opensearch_conn_using_db(sql2, location_id, plan_id)

        if run_sql2.get("total") not in [0, None]:

            key_names = []
            for i,n in enumerate(run_sql2.get('schema')):
                if n.get('name') == 'count(type_of_threat)':
                    key_names.append(n.get('alias'))
                else:
                    key_names.append(n.get('name'))
            
            table_query_list = []
            for i, key_values in enumerate(run_sql2.get('datarows')):
                Dict = {}
                Dict.update(dict(zip(key_names, key_values)))
                Dict["past_time"] = past_time
                Dict["current_time"] = current_time

                table_query_list.append(Dict)

            response_dict["filter"] = table_query_list
            
        return Response(response_dict)
    else:
        return Response({"message_type":"d_not_f"})

#2.b Lateral Movement table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_lateral_mov_table(request):
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    platform_name = request.GET.get('platform')
    
    if past_time is None:
        return Response({"message_type": "d_not_f","errors":"past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f","errors":"current_time_not_found"})
    
    if platform_name is None:
        return Response({"message_type": "d_not_f","errors": "platform_name_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT platform, type_of_threat, attacker_ip, attacker_mac, attack_timestamp, ids_threat_class, ids_threat_type, ml_threat_class, dl_threat_class, ml_accuracy, dl_accuracy, attacker_port, target_port, target_ip, geoip_city, geoip_country_name, geoip_asn_name FROM {indice_name}-* WHERE type_of_threat = 'Lateral Movement' "+s1+s2+f" AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform = '{platform_name}' AND ids_threat_class IS NOT NULL ORDER BY attack_epoch_time DESC limit 200000;"
    
    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)

    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [item['name'] for item in run_sql.get('schema')]
    
        table_query_list = []
        for i, row in enumerate(run_sql.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
            
        return Response({"message_type":"success", "count":len(table_query_list), "type_of_threat":'Lateral Movement',"table":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

#3.a Card Name: Internal Attacks (Internal Compromised Machine chart)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_int_compr(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    platform_tuple = detail_dict.get("platform_tuple")
    platform_query = f"AND platform IN {platform_tuple} " if platform_tuple is not None else ""
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    sql_query = f"SELECT type_of_threat, attack_epoch_time FROM {indice_name}-* WHERE type_of_threat = 'Internal Compromised Machine' "+platform_query+s1+s2+f" AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL ORDER BY attack_epoch_time DESC limit 200000;"
    
    run_sql_query = opensearch_conn_using_db(sql_query, location_id, plan_id)
    
    if run_sql_query.get("total") not in exclude_values:
    # formatting sql_query query output as (key, value) pairs in dictionary
        key_names = [item['name'] for item in run_sql_query.get('schema')]
        
        table_query_list = []
        for i, row in enumerate(run_sql_query.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
        
        # to create series
        epoch_interval_group_list = getEpochIntervalGroupList(condition, past_time, current_time)

        if epoch_interval_group_list is None:
            return Response({"message_type":"d_not_f", "errors": "condition_not_f"})
        
        # Create a dictionary with default values of 0 for time interval counts
        response_dict = defaultdict(lambda: [0] * len(epoch_interval_group_list))
        
        response_dict["message_type"] = "success"
        response_dict["total"] = len(table_query_list)
        
            
        if len(table_query_list) == 0:
                response_dict["internal_compromised_machine"]
        else:
            for item in table_query_list:
                epoch_date = item["attack_epoch_time"]
                for i, (start, end) in enumerate(epoch_interval_group_list):
                    if start <= epoch_date <= end:
                        response_dict["internal_compromised_machine"][i] += 1
        

        # for grouping according to platform
        sql2 = f"SELECT platform, type_of_threat, count(type_of_threat) threat_count FROM {indice_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} "+platform_query+s1+s2+f" AND type_of_threat = 'Internal Compromised Machine' AND platform IS NOT NULL AND ids_threat_class IS NOT NULL GROUP BY platform, type_of_threat ORDER BY threat_count desc;"
    
        run_sql2 = opensearch_conn_using_db(sql2, location_id, plan_id)

        if run_sql2.get("total") not in [0, None]:

            key_names = []
            for i,n in enumerate(run_sql2.get('schema')):
                if n.get('name') == 'count(type_of_threat)':
                    key_names.append(n.get('alias'))
                else:
                    key_names.append(n.get('name'))
            
            table_query_list = []
            for i, key_values in enumerate(run_sql2.get('datarows')):
                Dict = {}
                Dict.update(dict(zip(key_names, key_values)))
                Dict["past_time"] = past_time
                Dict["current_time"] = current_time

                table_query_list.append(Dict)

            response_dict["filter"] = table_query_list
            
        return Response(response_dict)
    else:
        return Response({"message_type":"d_not_f"})

#3.b Internal Compromised Machine Table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_int_compr_table(request):
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    platform_name = request.GET.get('platform')
    
    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})
    
    if platform_name is None:
        return Response({"message_type": "d_not_f","errors": "platform_name_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT platform, type_of_threat, attacker_ip, attacker_mac, attack_timestamp, ids_threat_class, ids_threat_type, ml_threat_class, dl_threat_class, ml_accuracy, dl_accuracy, attacker_port, target_port, target_ip, geoip_city, geoip_country_name, geoip_asn_name FROM {indice_name}-* WHERE type_of_threat = 'Internal Compromised Machine' "+s1+s2+f" AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform = '{platform_name}' AND ids_threat_class IS NOT NULL ORDER BY attack_epoch_time DESC limit 200000;"
    
    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)

    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [item['name'] for item in run_sql.get('schema')]
    
        table_query_list = []
        for i, row in enumerate(run_sql.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
            
        return Response({"message_type":"success", "count":len(table_query_list), "type_of_threat":'Internal Compromised Machine',"table":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})


#4.a Card Name: External Attacks
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_ext(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    platform_tuple = detail_dict.get("platform_tuple")
    platform_query = f"AND platform IN {platform_tuple} " if platform_tuple is not None else ""
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    threat_class_tuple = ('External Attack','Attack on External Server')
    
    sql_query = f"SELECT type_of_threat, attack_epoch_time FROM {indice_name}-* WHERE type_of_threat IN {threat_class_tuple} "+platform_query+s1+s2+f" AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL ORDER BY attack_epoch_time DESC limit 200000;"
    
    search2 = opensearch_conn_using_db(sql_query, location_id, plan_id)
    
    if search2.get("total") not in exclude_values:

    # # formatting sql_query query output as (key, value) pairs in dictionary
        key_names = [item['name'] for item in search2.get('schema')]
        
        table_query_list = []
        for i, row in enumerate(search2.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
        
        # to create series
        epoch_interval_group_list = getEpochIntervalGroupList(condition, past_time, current_time)

        if epoch_interval_group_list is None:
            return Response({"message_type":"d_not_f", "errors": "condition_not_f"})
        
        # Create a dictionary with default values of 0 for time interval counts
        response_dict = defaultdict(lambda: [0] * len(epoch_interval_group_list))
        
        response_dict["message_type"] = "success"
        response_dict["total"] = len(table_query_list)
        
        if len(table_query_list) == 0:
            response_dict["external_attack"]
        else:
            for item in table_query_list:
                epoch_date = item["attack_epoch_time"]
                for i, (start, end) in enumerate(epoch_interval_group_list):
                    if start <= epoch_date <= end:
                        response_dict["external_attack"][i] += 1

        # for grouping according to platform
        sql2 = f"SELECT platform, type_of_threat, count(type_of_threat) threat_count FROM {indice_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} "+platform_query+s1+s2+f" AND type_of_threat IN {threat_class_tuple} AND platform IS NOT NULL AND ids_threat_class IS NOT NULL GROUP BY platform, type_of_threat ORDER BY threat_count desc;"
    
        run_sql2 = opensearch_conn_using_db(sql2, location_id, plan_id)

        if run_sql2.get("total") not in [0, None]:

            key_names = []
            for i,n in enumerate(run_sql2.get('schema')):
                if n.get('name') == 'count(type_of_threat)':
                    key_names.append(n.get('alias'))
                else:
                    key_names.append(n.get('name'))
            
            table_query_list = []
            for i, key_values in enumerate(run_sql2.get('datarows')):
                if key_values[1] == "Attack on External Server":
                    key_values[1] = "External Attack"
                Dict = {}
                Dict.update(dict(zip(key_names, key_values)))
                Dict["past_time"] = past_time
                Dict["current_time"] = current_time

                table_query_list.append(Dict)

            response_dict["filter"] = table_query_list
            
        return Response(response_dict)
    else:
        return Response({"message_type":"d_not_f"})

#4.b External Attack Table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_ext_table(request):
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    platform_name = request.GET.get('platform')
    
    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})
    
    if platform_name is None:
        return Response({"message_type": "d_not_f","errors": "platform_name_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT platform, type_of_threat, attacker_ip, attacker_mac, attack_timestamp, ids_threat_class, ids_threat_type, ml_threat_class, dl_threat_class, ml_accuracy, dl_accuracy, attacker_port, target_port, target_ip, geoip_city, geoip_country_name, geoip_asn_name FROM {indice_name}-* WHERE type_of_threat IN ('External Attack','Attack on External Server') "+s1+s2+f" AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform = '{platform_name}' AND ids_threat_class IS NOT NULL ORDER BY attack_epoch_time DESC limit 200000;"
    
    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)

    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [item['name'] for item in run_sql.get('schema')]
    
        table_query_list = []
        for i, row in enumerate(run_sql.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
            
        return Response({"message_type":"success", "count":len(table_query_list), "type_of_threat":'External Attack',"table":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 5 Card Name: Most Attacked Host, Card Name: Target Host --only table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_freq_targetted_host(request):
    condition = request.GET.get('condition')
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    platform_tuple = detail_dict.get("platform_tuple")
    platform_query = f"AND platform IN {platform_tuple}" if platform_tuple is not None else ""
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    sql_query = f"SELECT target_ip,target_mac,type_of_threat, count(target_ip) target_ip_count FROM {indice_name}-* WHERE target_ip IS NOT NULL AND type_of_threat IS NOT NULL "+s1+s2+f" AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} AND ids_threat_class IS NOT NULL "+platform_query+" GROUP BY target_ip,target_mac,type_of_threat ORDER BY target_ip_count DESC LIMIT 50;"
    
    api_response = opensearch_conn_using_db(sql_query, location_id, plan_id)
    
    if api_response.get("total") not in exclude_values:
        key_names = [item['alias'] if (item['name'] == "count(target_ip)") else item['name'] for item in api_response.get('schema')]
        
        final_response = []
        for i in range(len(api_response.get('datarows'))):
            row = api_response.get('datarows')[i]
            final_response.append(dict(zip(key_names, row)))
        
        return Response({"message_type":"success", "data":final_response})
    else:
        return Response({"message_type":"d_not_f"})

# 6.a. Card Name: Attack Frequency 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_attack_frequency(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    platform_tuple = detail_dict.get("platform_tuple")
    platform_query = f"AND platform IN {platform_tuple} " if platform_tuple is not None else ""

    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    sql_query = f"SELECT attack_epoch_time, platform FROM {indice_name}-* WHERE (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL "+platform_query+s1+s2+f" ORDER BY attack_epoch_time DESC limit 200000;"

    run_sql = opensearch_conn_using_db(sql_query, location_id, plan_id)
    
    if run_sql.get("total") not in exclude_values:
        key_names = [item['name'] for item in run_sql.get('schema')]
        
        table_query_list = []
        for i, row in enumerate(run_sql.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
        
        # to create series
        epoch_interval_group_list = getEpochIntervalGroupList(condition, past_time, current_time)

        if epoch_interval_group_list is None:
            return Response({"message_type":"d_not_f", "errors": "condition_not_f"})
        
        # Create a dictionary with default values of 0 for time interval counts
        attack_frequency_dict = defaultdict(lambda: [0] * len(epoch_interval_group_list))
        
        # list containing groupings
        new_lables = []
        for start_time, end_time in epoch_interval_group_list:
            formatted_start_time = format_epoch_time(start_time)
            formatted_end_time = format_epoch_time(end_time)
            new_lables.append("{}".format(formatted_start_time))
        new_lables.append("{}".format(formatted_end_time))
        
        
        attack_frequency_dict["categories"] = new_lables
        
        for item in table_query_list:
            epoch_date = item["attack_epoch_time"]
            for i, (start, end) in enumerate(epoch_interval_group_list):
                if start <= epoch_date <= end:
                    attack_frequency_dict["series"][i] += 1
        
        filter_list = []
        for date, count in zip(attack_frequency_dict["categories"], attack_frequency_dict["series"]):
            threat_dict = {
                    "name": date,
                    "val": count,
                    # "past_time": past_time,
                    # "current_time": current_time
                }
            filter_list.append(threat_dict)
        
        for threat, epoch_time in zip(filter_list, epoch_interval_group_list):
            threat["past_time"] = epoch_time[0]
            threat["current_time"] = epoch_time[1]

        # col_val = str(new_lables).strip("[]")
        # epoch_time_tuple = "(" + col_val + ")"

        # for grouping according to platform
        # sql2 = f"SELECT platform, attack_epoch_time, count(attack_epoch_time) threat_count FROM {indice_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} "+s1+s2+f" AND attack_epoch_time IN {epoch_time_tuple} AND platform IS NOT NULL AND ids_threat_class IS NOT NULL GROUP BY platform, attack_epoch_time ORDER BY threat_count desc;"
    
        # run_sql2 = opensearch_conn_using_db(sql2, location_id, plan_id)

        # if run_sql2.get("total") not in [0, None]:

        #     key_names = []
        #     for i,n in enumerate(run_sql2.get('schema')):
        #         if n.get('name') == 'count(attack_epoch_time)':
        #             key_names.append(n.get('alias'))
        #         else:
        #             key_names.append(n.get('name'))
            
        #     table_query_list = []
        #     for i, key_values in enumerate(run_sql2.get('datarows')):
        #         Dict = {}
        #         Dict.update(dict(zip(key_names, key_values)))
        #         Dict["past_time"] = past_time
        #         Dict["current_time"] = current_time

        #         table_query_list.append(Dict)

            # response_dict["filter"] = table_query_list
        
        return Response({"message_type":"success", "attack_frequency":attack_frequency_dict, "filter":filter_list})
    else:
        return Response({"message_type":"d_not_f"})

# 6.b. Attack Frequency Table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_attack_freq_table(request):
    attack_date = request.GET.get('name')
    if attack_date is None:
        return Response({"message_type": "d_not_f", "errors": "name_not_found"})
    
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    platform_tuple = detail_dict.get("platform_tuple")
    platform_query = f"AND platform IN {platform_tuple}" if platform_tuple is not None else ""
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    
    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT platform, type_of_threat, attacker_ip, attacker_mac, attack_timestamp, ids_threat_class, ids_threat_type, ml_threat_class, dl_threat_class, ml_accuracy, dl_accuracy, attacker_port, target_port, target_ip, geoip_city, geoip_country_name, geoip_asn_name FROM {indice_name}-* WHERE (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) "+s1+s2+f" AND ids_threat_class IS NOT NULL "+platform_query+" ORDER BY attack_epoch_time DESC limit 200000;"
    
    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)
    
    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [item['name'] for item in run_sql.get('schema')]
        
        table_query_list = []
        
        for i, row in enumerate(run_sql.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
            
        return Response({"message_type":"success", "attack_count":len(table_query_list), "attack_date":attack_date, "table":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

#7.a Card Name: Attacker IPs (Line chart)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_line_chart(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    platform_tuple = detail_dict.get("platform_tuple")
    platform_query = f"AND platform IN {platform_tuple} " if platform_tuple is not None else ""

    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)
    
    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    sql1 = f"SELECT attacker_ip,count(attacker_ip) count FROM {indice_name}-* WHERE attacker_ip IS NOT NULL AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL "+platform_query+s1+s2+f" GROUP BY attacker_ip ORDER BY count desc LIMIT 7;"  
    
    search1 = opensearch_conn_using_db(sql1, location_id, plan_id)
    
    if search1.get("total") not in exclude_values:
        unique_IP, unique_IP_count = map(list, zip(*search1['datarows']))
        attacker_ip_tuple = tuple(unique_IP)
        updated_tuple = attacker_ip_tuple
        if len(attacker_ip_tuple) == 1:
            updated_tuple = attacker_ip_tuple+('0',)
    else:
        return Response({"message_type":"d_not_f"})

    # date wise count of a single attacker_ip
    sql2 = f"SELECT attacker_ip, attack_epoch_time FROM {indice_name}-* WHERE attacker_ip IN {updated_tuple} AND attacker_ip IS NOT NULL AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL "+platform_query+s1+s2+f" ORDER BY attack_epoch_time limit 500000;"
    
    search2 = opensearch_conn_using_db(sql2, location_id, plan_id)
    
    if search2.get("total") not in exclude_values:
        
        # formatting sql2 query output as (key, value) pairs in dictionary
        key_names = [item['name'] for item in search2.get('schema')]
        
        table_query_list = []
        for i, key_values in enumerate(search2.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, key_values)))
            table_query_list.append(Dict)
        
        epoch_interval_group_list = getEpochIntervalGroupList(condition, past_time, current_time)

        if epoch_interval_group_list is None:
            return Response({"message_type":"d_not_f", "errors": "condition_not_f"})
        
        # list containing groupings
        new_lables = []
        for start_time, end_time in epoch_interval_group_list:
            formatted_start_time = format_epoch_time(start_time)
            formatted_end_time = format_epoch_time(end_time)
            new_lables.append("{}".format(formatted_start_time))
        new_lables.append("{}".format(formatted_end_time))
        
        series = [] 
        for ip_value in unique_IP:
            filtered_dict = [dictionary for dictionary in table_query_list if dictionary.get('attacker_ip') == ip_value]
            
            interval_counts = [0] * len(epoch_interval_group_list)  # Initialize count for each interval to 0

            for item in filtered_dict:
                epoch_date = item["attack_epoch_time"]
                for i,interval in enumerate(epoch_interval_group_list):
                    start, end = interval
                    if start <= epoch_date <= end:
                        interval_counts[i] += 1
                        # break  # No need to check further intervals
            ip_dict = {
                "name": ip_value,
                "data": [None if count == 0 else count for count in interval_counts]
                # "sum": sum(interval_counts)#added only for testing purpose
                
            }
            series.append(ip_dict)
        
        # creating line_chart dictionary in given format
        line_chart = {"labels":new_lables, "series":series}
        
    else:
        return Response({"message_type":"d_not_f"})
    
    # for grouping according to platform
    sql3 = f"SELECT platform, attacker_ip, count(attacker_ip) attacker_ip_count FROM {indice_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} "+platform_query+s1+s2+f" AND attacker_ip IN {updated_tuple} AND platform IS NOT NULL AND ids_threat_class IS NOT NULL GROUP BY platform, attacker_ip ORDER BY attacker_ip_count desc;"
    
    run_sql3 = opensearch_conn_using_db(sql3, location_id, plan_id)

    if run_sql3.get("total") not in [0, None]:
        # formatting sql2 query output as (key, value) pairs in dictionary

        key_names = []
        for i,n in enumerate(run_sql3.get('schema')):
            if n.get('name') == 'count(attacker_ip)':
                key_names.append(n.get('alias'))
            else:
                key_names.append(n.get('name'))
        
        table_query_list = []
        for i, key_values in enumerate(run_sql3.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, key_values)))
            Dict["past_time"] = past_time
            Dict["current_time"] = current_time

            table_query_list.append(Dict)
        
        return Response({"message_type":"success","line_chart":line_chart, "filter":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})


#7.b. Attacker IPs Table 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_line_table(request):
    attacker_ip = request.GET.get('attacker_ip')
    if attacker_ip is None:
        return Response({"message_type": "d_not_f","errors": "attacker_ip_not_found"})
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    platform_name = request.GET.get('platform')
    
    if past_time is None:
        return Response({"message_type": "d_not_f","errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f","errors": "current_time_not_found"})
    
    if platform_name is None:
        return Response({"message_type": "d_not_f","errors": "platform_name_not_found"})
    
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""

    # sql query to get table data
    table_query = f"SELECT platform, type_of_threat, attacker_ip, attacker_mac, attack_timestamp, ids_threat_class, ids_threat_type, ml_threat_class, dl_threat_class, ml_accuracy, dl_accuracy, attacker_port, target_port, target_ip, geoip_city, geoip_country_name, geoip_asn_name FROM {indice_name}-* WHERE attacker_ip = '{attacker_ip}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform = '{platform_name}' AND ids_threat_class IS NOT NULL "+s1+s2+f" ORDER BY attack_epoch_time DESC limit 200000;"
        
    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)
    
    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:    
        key_names = [item['name'] for item in run_sql.get('schema')]

        table_query_list = []
        for i, row in enumerate(run_sql.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
        
        return Response({"message_type":"success", "count":len(table_query_list), "attacker_ip":attacker_ip,"table":table_query_list})
    else:
        return Response({"message_type":"d_n_f"})

# 8.a Card Name: Service Names (Bar chart on service_name column)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_service_name_bar_chart(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    platform_tuple = detail_dict.get("platform_tuple")
    platform_query = f"AND platform IN {platform_tuple} " if platform_tuple is not None else ""

    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    sql = f"SELECT service_name, COUNT(service_name) FROM {indice_name}-* WHERE service_name NOT LIKE 'NA' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL "+platform_query+s1+s2+f" GROUP BY service_name ORDER BY COUNT(service_name) desc LIMIT 7;"
    
    run_sql_query = opensearch_conn_using_db(sql, location_id, plan_id)
    
    if run_sql_query.get("total") not in exclude_values:
        service_name, service_name_count = map(list, zip(*run_sql_query['datarows']))
        bar_chart_dict = {"series": service_name_count, "labels": service_name}

        col_val = str(service_name).strip("[]")
        service_name_tuple = "(" + col_val + ")"

        # for grouping according to platform
        sql2 = f"SELECT platform, service_name, count(service_name) service_name_count FROM {indice_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} "+platform_query+s1+s2+f" AND service_name IN {service_name_tuple} AND platform IS NOT NULL AND ids_threat_class IS NOT NULL GROUP BY platform, service_name ORDER BY service_name_count desc;"
        
        run_sql2 = opensearch_conn_using_db(sql2, location_id, plan_id)

        if run_sql2.get("total") not in [0, None]:
            # formatting sql2 query output as (key, value) pairs in dictionary

            key_names = []
            for i,n in enumerate(run_sql2.get('schema')):
                if n.get('name') == 'count(service_name)':
                    key_names.append(n.get('alias'))
                else:
                    key_names.append(n.get('name'))
            
            table_query_list = []
            for i, key_values in enumerate(run_sql2.get('datarows')):
                Dict = {}
                Dict.update(dict(zip(key_names, key_values)))
                Dict["past_time"] = past_time
                Dict["current_time"] = current_time

                table_query_list.append(Dict)
        else:
            return Response({"message_type":"d_not_f"})
        
        return Response({"message_type":"success", "bar_chart":bar_chart_dict, "filter":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 8.b Bar chart on service_name column--Table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_service_name_bar_table(request):
    service_name = request.GET.get('service_name')
    if service_name is None:
        return Response({"message_type": "d_not_f","errors": "service_name_not_found"})
    
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    platform_name = request.GET.get('platform')
    
    if past_time is None:
        return Response({"message_type": "d_not_f","errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f","errors": "current_time_not_found"})
    
    if platform_name is None:
        return Response({"message_type": "d_not_f","errors": "platform_name_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT platform, type_of_threat, attacker_ip, attacker_mac, attack_timestamp, ids_threat_class, ids_threat_type, ml_threat_class, dl_threat_class, ml_accuracy, dl_accuracy, attacker_port, target_port, target_ip, geoip_city, geoip_country_name, geoip_asn_name FROM {indice_name}-* WHERE service_name = '{service_name}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform = '{platform_name}' AND ids_threat_class IS NOT NULL "+s1+s2+f" ORDER BY attack_epoch_time DESC limit 200000;"
    
    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)
    
    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [item['name'] for item in run_sql.get('schema')]
        
        table_query_list = []
        for i, row in enumerate(run_sql.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
            
        return Response({"message_type":"success", "count":len(table_query_list), "service_name":service_name,"table":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 9.a Card Name: Attacker Port (Pie chart on attacker_port column)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_attacker_port_pie_chart(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    platform_tuple = detail_dict.get("platform_tuple")
    platform_query = f"AND platform IN {platform_tuple} " if platform_tuple is not None else ""

    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    sql = f"SELECT attacker_port, COUNT(attacker_port) FROM {indice_name}-* WHERE attacker_port IS NOT NULL AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL "+platform_query+s1+s2+f" GROUP BY attacker_port ORDER BY COUNT(attacker_port) desc LIMIT 7;"
    
    run_sql_query = opensearch_conn_using_db(sql, location_id, plan_id)
    
    if run_sql_query.get("total") not in exclude_values:
        attacker_port, attacker_port_count = map(list, zip(*run_sql_query['datarows']))

        pie_chart_dict = {"series": attacker_port_count, "labels": attacker_port}

        col_val = str(attacker_port).strip("[]")
        attacker_port_tuple = "(" + col_val + ")"

        # for grouping according to platform
        sql2 = f"SELECT platform, attacker_port, count(attacker_port) attacker_port_count FROM {indice_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} "+platform_query+s1+s2+f" AND attacker_port IN {attacker_port_tuple} AND platform IS NOT NULL AND ids_threat_class IS NOT NULL GROUP BY platform, attacker_port ORDER BY attacker_port_count desc;"
        
        run_sql2 = opensearch_conn_using_db(sql2, location_id, plan_id)

        if run_sql2.get("total") not in [0, None]:
            # formatting sql2 query output as (key, value) pairs in dictionary

            key_names = []
            for i,n in enumerate(run_sql2.get('schema')):
                if n.get('name') == 'count(attacker_port)':
                    key_names.append(n.get('alias'))
                else:
                    key_names.append(n.get('name'))
            
            table_query_list = []
            for i, key_values in enumerate(run_sql2.get('datarows')):
                Dict = {}
                Dict.update(dict(zip(key_names, key_values)))
                Dict["past_time"] = past_time
                Dict["current_time"] = current_time

                table_query_list.append(Dict)
        else:
            return Response({"message_type":"d_not_f"})

        return Response({"message_type":"success", "bar_chart":pie_chart_dict, "filter":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 9.b Pie chart on attacker_port column--Table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_attacker_port_pie_table(request):
    attacker_port = request.GET.get('attacker_port')
    if attacker_port is None:
        return Response({"message_type": "d_not_f", "errors": "attacker_port_not_found"})
    
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    platform_name = request.GET.get('platform')
    
    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})
    
    if platform_name is None:
        return Response({"message_type": "d_not_f","errors": "platform_name_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT platform, type_of_threat, attacker_ip, attacker_mac, attack_timestamp, ids_threat_class, ids_threat_type, ml_threat_class, dl_threat_class, ml_accuracy, dl_accuracy, attacker_port, target_port, target_ip, geoip_city, geoip_country_name, geoip_asn_name FROM {indice_name}-* WHERE attacker_port = {attacker_port} AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform = '{platform_name}' AND ids_threat_class IS NOT NULL "+s1+s2+f" ORDER BY attack_epoch_time DESC limit 200000;"
    
    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)
    
    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [item['name'] for item in run_sql.get('schema')]
        
        table_query_list = []
        for i, row in enumerate(run_sql.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
            
        return Response({"message_type":"success", "count":len(table_query_list), "attacker_port":attacker_port,"table":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})


# 10.a Card Name: Threat Class (Bar chart on ids_threat_class column)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_ids_class_bar_chart(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    platform_tuple = detail_dict.get("platform_tuple")
    platform_query = f"AND platform IN {platform_tuple} " if platform_tuple is not None else ""

    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    sql = f"SELECT ids_threat_class, COUNT(ids_threat_class) FROM {indice_name}-* WHERE ids_threat_class NOT LIKE 'NA' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL "+platform_query+s1+s2+f" GROUP BY ids_threat_class ORDER BY COUNT(ids_threat_class) desc LIMIT 7;"
    
    run_sql_query = opensearch_conn_using_db(sql, location_id, plan_id)
    
    if run_sql_query.get("total") not in exclude_values:
        ids_threat_class, threat_count = map(list, zip(*run_sql_query['datarows']))

        bar_chart_dict = {"series": threat_count, "labels": ids_threat_class}

        col_val = str(ids_threat_class).strip("[]")
        ids_threat_class_tuple = "(" + col_val + ")"

        # for grouping according to platform
        sql2 = f"SELECT platform, ids_threat_class, count(ids_threat_class) ids_threat_class_count FROM {indice_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} "+platform_query+s1+s2+f" AND ids_threat_class IN {ids_threat_class_tuple} AND platform IS NOT NULL AND ids_threat_class IS NOT NULL GROUP BY platform, ids_threat_class ORDER BY ids_threat_class_count desc;"
        
        run_sql2 = opensearch_conn_using_db(sql2, location_id, plan_id)

        if run_sql2.get("total") not in [0, None]:
            # formatting sql2 query output as (key, value) pairs in dictionary

            key_names = []
            for i,n in enumerate(run_sql2.get('schema')):
                if n.get('name') == 'count(ids_threat_class)':
                    key_names.append(n.get('alias'))
                else:
                    key_names.append(n.get('name'))
            
            table_query_list = []
            for i, key_values in enumerate(run_sql2.get('datarows')):
                Dict = {}
                Dict.update(dict(zip(key_names, key_values)))
                Dict["past_time"] = past_time
                Dict["current_time"] = current_time

                table_query_list.append(Dict)
        else:
            return Response({"message_type":"d_not_f"})
        
        return Response({"message_type":"success", "bar_chart":bar_chart_dict, "filter":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 10.b Bar chart on ids_threat_class column--Table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_ids_class_bar_table(request):
    ids_threat_class = request.GET.get('ids_threat_class')
    if ids_threat_class is None:
        return Response({"message_type": "d_not_f", "errors": "ids_threat_class_not_found"})
    
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    platform_name = request.GET.get('platform')
    
    if past_time is None:
        return Response({"message_type": "d_not_f","errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "current_time_not_found"})
    
    if platform_name is None:
        return Response({"message_type": "d_not_f","errors": "platform_name_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT platform, type_of_threat, attacker_ip, attacker_mac, attack_timestamp, ids_threat_class, ids_threat_type, ml_threat_class, dl_threat_class, ml_accuracy, dl_accuracy, attacker_port, target_port, target_ip, geoip_city, geoip_country_name, geoip_asn_name FROM {indice_name}-* WHERE ids_threat_class = '{ids_threat_class}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform = '{platform_name}' AND ids_threat_class IS NOT NULL "+s1+s2+f" ORDER BY attack_epoch_time DESC limit 200000;"
    
    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)
    
    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [item['name'] for item in run_sql.get('schema')]
        
        table_query_list = []
        for i, row in enumerate(run_sql.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
            
        return Response({"message_type":"success", "count":len(table_query_list), "ids_threat_class":ids_threat_class,"table":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 11.a Card Name: Malware Threats Type (Pie chart on malware_type column)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_malware_type_pie_chart(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    platform_tuple = detail_dict.get("platform_tuple")
    platform_query = f"AND platform IN {platform_tuple} " if platform_tuple is not None else ""

    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    sql = f"SELECT malware_type, COUNT(malware_type) FROM {indice_name}-* WHERE malware_type IS NOT NULL AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL "+platform_query+s1+s2+f" GROUP BY malware_type ORDER BY COUNT(malware_type) desc LIMIT 7;"
    
    run_sql_query = opensearch_conn_using_db(sql, location_id, plan_id)
    
    if run_sql_query.get("total") not in exclude_values:
        malware_type, malware_type_count = map(list, zip(*run_sql_query['datarows']))

        pie_chart_dict = {"series": malware_type_count, "labels": malware_type}

        col_val = str(malware_type).strip("[]")
        malware_type_tuple = "(" + col_val + ")"

        # for grouping according to platform
        sql2 = f"SELECT platform, malware_type, count(malware_type) malware_type_count FROM {indice_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} "+platform_query+s1+s2+f" AND malware_type IN {malware_type_tuple} AND platform IS NOT NULL AND ids_threat_class IS NOT NULL GROUP BY platform, malware_type ORDER BY malware_type_count desc;"
        
        run_sql2 = opensearch_conn_using_db(sql2, location_id, plan_id)

        if run_sql2.get("total") not in [0, None]:
            # formatting sql2 query output as (key, value) pairs in dictionary

            key_names = []
            for i,n in enumerate(run_sql2.get('schema')):
                if n.get('name') == 'count(malware_type)':
                    key_names.append(n.get('alias'))
                else:
                    key_names.append(n.get('name'))
            
            table_query_list = []
            for i, key_values in enumerate(run_sql2.get('datarows')):
                Dict = {}
                Dict.update(dict(zip(key_names, key_values)))
                Dict["past_time"] = past_time
                Dict["current_time"] = current_time

                table_query_list.append(Dict)
        else:
            return Response({"message_type":"d_not_f"})

        return Response({"message_type":"success", "bar_chart":pie_chart_dict, "filter":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 11.b Pie chart on malware_type column--Table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_malware_type_pie_table(request):
    malware_type = request.GET.get('malware_type')
    if malware_type is None:
        return Response({"message_type": "d_not_f", "errors": "malware_type_not_found"})
    
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    platform_name = request.GET.get('platform')
    
    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})
    
    if platform_name is None:
        return Response({"message_type": "d_not_f","errors": "platform_name_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT platform, type_of_threat, attacker_ip, attacker_mac, attack_timestamp, ids_threat_class, ids_threat_type, ml_threat_class, dl_threat_class, ml_accuracy, dl_accuracy, attacker_port, target_port, target_ip, geoip_city, geoip_country_name, geoip_asn_name FROM {indice_name}-* WHERE malware_type = '{malware_type}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform = '{platform_name}' AND ids_threat_class IS NOT NULL "+s1+s2+f" ORDER BY attack_epoch_time DESC limit 200000;"
    
    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)
    
    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [item['name'] for item in run_sql.get('schema')]
        
        table_query_list = []
        for i, row in enumerate(run_sql.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
            
        return Response({"message_type":"success", "count":len(table_query_list), "malware_type":malware_type,"table":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 12.a Card Name: Mitre Att&ck Tactics (Bar chart on mitre_tactics_name column)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_mitre_tactics_bar_chart(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    platform_tuple = detail_dict.get("platform_tuple")
    platform_query = f"AND platform IN {platform_tuple} " if platform_tuple is not None else ""

    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    sql = f"SELECT mitre_tactics_name, COUNT(mitre_tactics_name) FROM {indice_name}-* WHERE mitre_tactics_name IS NOT NULL AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL "+platform_query+s1+s2+f" GROUP BY mitre_tactics_name ORDER BY COUNT(mitre_tactics_name) desc LIMIT 7;"
    
    run_sql_query = opensearch_conn_using_db(sql, location_id, plan_id)
    
    if run_sql_query.get("total") not in exclude_values:
        mitre_tactics_name, mitre_tactics_count = map(list, zip(*run_sql_query['datarows']))

        bar_chart_dict = {"series": mitre_tactics_count, "labels": mitre_tactics_name}

        col_val = str(mitre_tactics_name).strip("[]")
        mitre_tactics_tuple = "(" + col_val + ")"
        
        # for grouping according to platform
        sql2 = f"SELECT platform, mitre_tactics_name, count(mitre_tactics_name) mitre_tactics_name_count FROM {indice_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} "+platform_query+s1+s2+f" AND mitre_tactics_name IN {mitre_tactics_tuple} AND platform IS NOT NULL AND mitre_tactics_name IS NOT NULL GROUP BY platform, mitre_tactics_name ORDER BY mitre_tactics_name_count desc;"
        
        run_sql2 = opensearch_conn_using_db(sql2, location_id, plan_id)

        if run_sql2.get("total") not in [0, None]:
            # formatting sql2 query output as (key, value) pairs in dictionary

            key_names = []
            for i,n in enumerate(run_sql2.get('schema')):
                if n.get('name') == 'count(mitre_tactics_name)':
                    key_names.append(n.get('alias'))
                else:
                    key_names.append(n.get('name'))
            
            table_query_list = []
            for i, key_values in enumerate(run_sql2.get('datarows')):
                Dict = {}
                Dict.update(dict(zip(key_names, key_values)))
                Dict["past_time"] = past_time
                Dict["current_time"] = current_time

                table_query_list.append(Dict)
        else:
            return Response({"message_type":"d_not_f"})
        
        return Response({"message_type":"success", "bar_chart":bar_chart_dict, "filter":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 12.b Bar chart on mitre_tactics_name column--Table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_mitre_tactics_bar_table(request):
    mitre_tactics_name = request.GET.get('mitre_tactics_name')
    if mitre_tactics_name is None:
        return Response({"message_type": "d_not_f", "errors": "mitre_tactics_name_not_found"})
    
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    platform_name = request.GET.get('platform')
    
    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})
    
    if platform_name is None:
        return Response({"message_type": "d_not_f","errors": "platform_name_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT platform, type_of_threat, attacker_ip, attacker_mac, attack_timestamp, ids_threat_class, ids_threat_type, ml_threat_class, dl_threat_class, ml_accuracy, dl_accuracy, attacker_port, target_port, target_ip, geoip_city, geoip_country_name, geoip_asn_name FROM {indice_name}-* WHERE mitre_tactics_name = '{mitre_tactics_name}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform = '{platform_name}' AND ids_threat_class IS NOT NULL "+s1+s2+f" ORDER BY attack_epoch_time DESC limit 200000;"
    
    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)
    
    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [item['name'] for item in run_sql.get('schema')]
        
        table_query_list = []
        for i, row in enumerate(run_sql.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
            
        return Response({"message_type":"success", "count":len(table_query_list), "mitre_tactics_name":mitre_tactics_name,"table":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 13.a Card Name: Mitre Att&ck Techniques (Bar chart on mitre_techniques_name column)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_mitre_techniq_bar_chart(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    platform_tuple = detail_dict.get("platform_tuple")
    platform_query = f"AND platform IN {platform_tuple} " if platform_tuple is not None else ""

    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    sql = f"SELECT mitre_techniques_name, COUNT(mitre_techniques_name) FROM {indice_name}-* WHERE mitre_techniques_name IS NOT NULL AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL "+platform_query+s1+s2+f" GROUP BY mitre_techniques_name ORDER BY COUNT(mitre_techniques_name) desc LIMIT 7;"
    
    run_sql_query = opensearch_conn_using_db(sql, location_id, plan_id)
    
    if run_sql_query.get("total") not in exclude_values:
        mitre_techniques_name, mitre_techniques_count = map(list, zip(*run_sql_query['datarows']))

        bar_chart_dict = {"series": mitre_techniques_count, "labels": mitre_techniques_name}

        col_val = str(mitre_techniques_name).strip("[]")
        mitre_techniques_tuple = "(" + col_val + ")"
        
        # for grouping according to platform
        sql2 = f"SELECT platform, mitre_techniques_name, count(mitre_techniques_name) mitre_techniques_name_count FROM {indice_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} "+platform_query+s1+s2+f" AND mitre_techniques_name IN {mitre_techniques_tuple} AND platform IS NOT NULL AND mitre_techniques_name IS NOT NULL GROUP BY platform, mitre_techniques_name ORDER BY mitre_techniques_name_count desc;"
        
        run_sql2 = opensearch_conn_using_db(sql2, location_id, plan_id)

        if run_sql2.get("total") not in [0, None]:
            # formatting sql2 query output as (key, value) pairs in dictionary

            key_names = []
            for i,n in enumerate(run_sql2.get('schema')):
                if n.get('name') == 'count(mitre_techniques_name)':
                    key_names.append(n.get('alias'))
                else:
                    key_names.append(n.get('name'))
            
            table_query_list = []
            for i, key_values in enumerate(run_sql2.get('datarows')):
                Dict = {}
                Dict.update(dict(zip(key_names, key_values)))
                Dict["past_time"] = past_time
                Dict["current_time"] = current_time

                table_query_list.append(Dict)
        else:
            return Response({"message_type":"d_not_f"})

        return Response({"message_type":"success", "bar_chart":bar_chart_dict, "filter":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 13.b Bar chart on mitre_techniques_name column--Table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_mitre_techniq_bar_table(request):
    mitre_techniques_name = request.GET.get('mitre_techniques_name')
    if mitre_techniques_name is None:
        return Response({"message_type": "d_not_f", "errors": "mitre_techniques_name_not_found"})
    
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    platform_name = request.GET.get('platform')
    
    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})
    
    if platform_name is None:
        return Response({"message_type": "d_not_f","errors": "platform_name_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT platform, type_of_threat, attacker_ip, attacker_mac, attack_timestamp, ids_threat_class, ids_threat_type, ml_threat_class, dl_threat_class, ml_accuracy, dl_accuracy, attacker_port, target_port, target_ip, geoip_city, geoip_country_name, geoip_asn_name FROM {indice_name}-* WHERE mitre_techniques_name = '{mitre_techniques_name}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform = '{platform_name}' AND ids_threat_class IS NOT NULL "+s1+s2+f" ORDER BY attack_epoch_time DESC limit 200000;"
    
    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)
    
    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [item['name'] for item in run_sql.get('schema')]
        
        table_query_list = []
        for i, row in enumerate(run_sql.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
            
        return Response({"message_type":"success", "count":len(table_query_list), "mitre_techniques_name":mitre_techniques_name,"table":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})


# 14.a. Card Name: Detected Threat Type -----(i).ML (ii).DL (iii). IDS
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_detected_threat_type(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    platform_tuple = detail_dict.get("platform_tuple")
    platform_query = f"AND platform IN {platform_tuple} " if platform_tuple is not None else ""
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple} " if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
     
    ml_sql_query = f"SELECT platform, ml_threat_class, count(ml_threat_class) count FROM {indice_name}-* WHERE ml_threat_class IS NOT NULL AND ids_threat_class IS NOT NULL AND ml_threat_class !='undefined class' and platform IS NOT NULL AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) "+platform_query+s1+s2+f" GROUP BY platform, ml_threat_class ORDER BY count desc LIMIT 7;"
    
    dl_sql_query = f"SELECT platform, dl_threat_class, count(dl_threat_class) count FROM {indice_name}-* WHERE dl_threat_class IS NOT NULL AND ids_threat_class IS NOT NULL AND dl_threat_class !='undefined class' and platform IS NOT NULL AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) "+platform_query+s1+s2+f" GROUP BY platform, dl_threat_class ORDER BY count desc LIMIT 7;"
    
    ids_sql_query = f"SELECT platform, ids_threat_class, count(ids_threat_class) count FROM {indice_name}-* WHERE ids_threat_class IS NOT NULL AND ids_threat_class !='undefined class' and platform IS NOT NULL AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) "+platform_query+s1+s2+f" GROUP BY platform, ids_threat_class ORDER BY count desc LIMIT 7;"
    
    ml_query_output = opensearch_conn_using_db(ml_sql_query, location_id, plan_id)
    dl_query_output = opensearch_conn_using_db(dl_sql_query, location_id, plan_id)
    ids_query_output = opensearch_conn_using_db(ids_sql_query, location_id, plan_id)
    
    # Check if all "total" values are in the exclude_values set
    if all(value.get("total") not in exclude_values for value in [ml_query_output, dl_query_output, ids_query_output]):
        
        ml_threat_list = []
        platform, ml_threat_class_list,ml_threat_class_count= map(list, zip(*ml_query_output['datarows']))
        
        ml_threat_list = [{
            "name": name,
            "platform": platform,
            "value": count,
            "past_time": past_time,
            "current_time": current_time
        } for platform, name, count in zip(platform,ml_threat_class_list, ml_threat_class_count)]
        
        
        dl_threat_list = []
        platform, dl_threat_class_list,dl_threat_class_count= map(list, zip(*dl_query_output['datarows']))
        
        dl_threat_list = [{
            "name": name,
            "platform": platform,
            "value": count,
            "past_time": past_time,
            "current_time": current_time
        } for platform, name, count in zip(platform, dl_threat_class_list, dl_threat_class_count)]

    
        ids_threat_list = []
        platform, ids_threat_class_list,ids_threat_class_count= map(list, zip(*ids_query_output['datarows']))
        
        ids_threat_list = [{
            "name": name,
            "platform": platform,
            "value": count,
            "past_time": past_time,
            "current_time": current_time
        } for platform, name, count in zip(platform, ids_threat_class_list, ids_threat_class_count)]
        
    
    # response dictionary
        response_dict = {"ml":ml_threat_list, "dl":dl_threat_list, "ids":ids_threat_list} 
        
        return Response({"message_type":"success", "detected_threat_type":response_dict})
    else:
        return Response({"message_type":"d_not_f"})


# 14.b. Detected Threat Type card---Table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_detected_threat_type_table(request):
    threat_class_type = request.GET.get('type')
    if threat_class_type is None:
        return Response({"message_type": "d_not_f", "errors": "type_not_f"})    
    
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    ids_threat_class = request.GET.get('name')
    if ids_threat_class is None:
        return Response({"message_type": "d_not_f", "errors": "name_not_f"})
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    platform_name = request.GET.get('platform')

    if platform_name is None:
        return Response({"message_type": "d_not_f","errors": "platform_name_not_found"})
    
    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_f"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_f"})
    
    threat_class_type_dict = {
        "ml": "ml_threat_class",
        "dl": "dl_threat_class",
        "ids": "ids_threat_class"
    }
    
    if threat_class_type in threat_class_type_dict:
        
        # sql query to get table data
        table_query = f"SELECT platform, type_of_threat, attacker_ip, attacker_mac, attack_timestamp, ids_threat_class, ids_threat_type, ml_threat_class, dl_threat_class, ml_accuracy, dl_accuracy, attacker_port, target_port, target_ip, geoip_city, geoip_country_name, geoip_asn_name FROM {indice_name}-* WHERE {threat_class_type_dict[threat_class_type]} = '{ids_threat_class}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL AND platform = '{platform_name}' "+s1+s2+f" ORDER BY attack_epoch_time DESC limit 200000;"

        run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)
    
        # formatting above query output to {column_name: column_value}
        if run_sql.get("total") not in exclude_values:
            key_names = [item['name'] for item in run_sql.get('schema')]
        
            table_query_list = []
            for i, row in enumerate(run_sql.get('datarows')):
                Dict = {}
                Dict.update(dict(zip(key_names, row)))
                table_query_list.append(Dict)
                
            return Response({"message_type":"success", "count":len(table_query_list), f"{threat_class_type_dict[threat_class_type]}":ids_threat_class,"table":table_query_list})
        else:
            return Response({"message_type":"d_not_f"})
    else:
        return Response({"message_type": "d_not_f", "errors": "type_not_f"})



# 15.a. Card Name: Attacker Geo-Locations
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_geolocation(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    platform_tuple = detail_dict.get("platform_tuple")
    platform_query = f"AND platform IN {platform_tuple} " if platform_tuple is not None else ""

    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})

    sql = f"SELECT geoip_city, geoip_latitude,geoip_longitude, count(*) count FROM {indice_name}-* WHERE geoip_country_name IS NOT NULL AND geoip_latitude IS NOT NULL AND geoip_longitude IS NOT NULL AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL "+platform_query+s1+s2+f" GROUP BY geoip_city,geoip_latitude,geoip_longitude ORDER BY count desc LIMIT 20;"
    
    run_sql = opensearch_conn_using_db(sql, location_id, plan_id)
    
    map_value = []
    if run_sql.get("total") not in exclude_values:
        geoip_city, geoip_latitude, geoip_longitude, attack_count = map(list, zip(*run_sql['datarows']))
        latandlon = zip(geoip_longitude, geoip_latitude)
        for (m, n) in zip(latandlon, geoip_city):
            map_value.append({"position": m, "title": n})

        col_val = str(geoip_city).strip("[]")
        geoip_city_tuple = "(" + col_val + ")"
    
        # for grouping according to platform
        sql2 = f"SELECT platform, geoip_city, count(geoip_city) geoip_city_count FROM {indice_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} "+platform_query+s1+s2+f" AND geoip_city IN {geoip_city_tuple} AND platform IS NOT NULL AND ids_threat_class IS NOT NULL GROUP BY platform, geoip_city ORDER BY geoip_city_count desc;"
        
        run_sql2 = opensearch_conn_using_db(sql2, location_id, plan_id)

        if run_sql2.get("total") not in [0, None]:
            # formatting sql2 query output as (key, value) pairs in dictionary

            key_names = []
            for i,n in enumerate(run_sql2.get('schema')):
                if n.get('name') == 'count(geoip_city)':
                    key_names.append(n.get('alias'))
                else:
                    key_names.append(n.get('name'))
            
            table_query_list = []
            for i, key_values in enumerate(run_sql2.get('datarows')):
                Dict = {}
                Dict.update(dict(zip(key_names, key_values)))
                Dict["past_time"] = past_time
                Dict["current_time"] = current_time

                table_query_list.append(Dict)
        else:
            return Response({"message_type":"d_not_f"})
        
        return Response({"message_type":"success", "geolocation":map_value, "filter":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})


# 15.b. geolocation Table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_geolocation_table(request):
    city_name = request.GET.get('geoip_city')
    if city_name is None:
        return Response({"message_type": "d_not_f", "errors": "geoip_city_not_found"})
    
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type": "d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    platform_name = request.GET.get('platform')

    if platform_name is None:
        return Response({"message_type": "d_not_f","errors": "platform_name_not_found"})
    
    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f'''SELECT platform, type_of_threat, attacker_ip, attacker_mac, attack_timestamp, ids_threat_class, ids_threat_type, ml_threat_class, dl_threat_class, ml_accuracy, dl_accuracy, attacker_port, target_port, target_ip, geoip_city, geoip_country_name, geoip_asn_name FROM {indice_name}-* WHERE geoip_city = "{city_name}" AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform = '{platform_name}' AND ids_threat_class IS NOT NULL '''+s1+s2+f''' ORDER BY attack_epoch_time DESC limit 200000;'''
      
    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)
    
    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [item['name'] for item in run_sql.get('schema')]
        
        table_query_list = []
        for i, row in enumerate(run_sql.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
            
        return Response({"message_type":"success", "count":len(table_query_list), "city_name":city_name,"table":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 16.a Card Name: Top Source Attack Countries (Bar chart on geoip_country_name column)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_country_bar_chart(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    platform_tuple = detail_dict.get("platform_tuple")
    platform_query = f"AND platform IN {platform_tuple} " if platform_tuple is not None else ""

    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    sql = f"SELECT geoip_country_name, COUNT(geoip_country_name) FROM {indice_name}-* WHERE geoip_country_name NOT LIKE 'NA' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL "+platform_query+s1+s2+f" GROUP BY geoip_country_name ORDER BY COUNT(geoip_country_name) desc LIMIT 7;"
    
    run_sql_query = opensearch_conn_using_db(sql, location_id, plan_id)
    
    if run_sql_query.get("total") not in exclude_values:
        geoip_country, country_count = map(list, zip(*run_sql_query['datarows']))
        bar_chart_dict = {"series": country_count, "labels": geoip_country}

        col_val = str(geoip_country).strip("[]")
        geoip_country_tuple = "(" + col_val + ")"
    
        # for grouping according to platform
        sql2 = f"SELECT platform, geoip_country_name, count(geoip_country_name) geoip_country_name_count FROM {indice_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} "+platform_query+s1+s2+f" AND geoip_country_name IN {geoip_country_tuple} AND platform IS NOT NULL AND ids_threat_class IS NOT NULL GROUP BY platform, geoip_country_name ORDER BY geoip_country_name_count desc;"
        
        run_sql2 = opensearch_conn_using_db(sql2, location_id, plan_id)

        if run_sql2.get("total") not in [0, None]:
            # formatting sql2 query output as (key, value) pairs in dictionary

            key_names = []
            for i,n in enumerate(run_sql2.get('schema')):
                if n.get('name') == 'count(geoip_country_name)':
                    key_names.append(n.get('alias'))
                else:
                    key_names.append(n.get('name'))
            
            table_query_list = []
            for i, key_values in enumerate(run_sql2.get('datarows')):
                Dict = {}
                Dict.update(dict(zip(key_names, key_values)))
                Dict["past_time"] = past_time
                Dict["current_time"] = current_time

                table_query_list.append(Dict)
        else:
            return Response({"message_type":"d_not_f"})
        
        return Response({"message_type":"success", "bar_chart":bar_chart_dict, "filter":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 16.b Bar chart on geoip_country_name column--Table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_country_bar_table(request):
    country_name = request.GET.get('geoip_country_name')
    if country_name is None:
        return Response({"message_type": "d_not_f", "errors": "geoip_country_name_not_found"})
    
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    platform_name = request.GET.get('platform')

    if platform_name is None:
        return Response({"message_type": "d_not_f","errors": "platform_name_not_found"})
    
    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f'''SELECT platform, type_of_threat, attacker_ip, attacker_mac, attack_timestamp, ids_threat_class, ids_threat_type, ml_threat_class, dl_threat_class, ml_accuracy, dl_accuracy, attacker_port, target_port, target_ip, geoip_city, geoip_country_name, geoip_asn_name FROM {indice_name}-* WHERE geoip_country_name = "{country_name}" AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform = '{platform_name}' AND ids_threat_class IS NOT NULL '''+s1+s2+f''' ORDER BY attack_epoch_time DESC limit 200000;'''
    
    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)
    
    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [item['name'] for item in run_sql.get('schema')]
        
        table_query_list = []
        for i, row in enumerate(run_sql.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
            
        return Response({"message_type":"success", "count":len(table_query_list), "country_name":country_name,"table":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})


# 17.a Card Name: Top Attacker City (Pie chart on geoip_city column)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_city_pie_chart(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    platform_tuple = detail_dict.get("platform_tuple")
    platform_query = f"AND platform IN {platform_tuple} " if platform_tuple is not None else ""

    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    sql = f"SELECT geoip_city, COUNT(geoip_city) FROM {indice_name}-* WHERE geoip_city NOT LIKE 'NA' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL AND geoip_city IS NOT NULL "+platform_query+s1+s2+f" GROUP BY geoip_city ORDER BY COUNT(geoip_city) desc LIMIT 7;"
    
    run_sql_query = opensearch_conn_using_db(sql, location_id, plan_id)
    
    if run_sql_query.get("total") not in exclude_values:
        geoip_city, city_count = map(list, zip(*run_sql_query['datarows']))
        pie_chart_dict = {"series": city_count, "labels": geoip_city}
        
        
        col_val = str(geoip_city).strip("[]")
        geoip_city_tuple = "(" + col_val + ")"
    
        # for grouping according to platform
        sql2 = f"SELECT platform, geoip_city, count(geoip_city) geoip_city_count FROM {indice_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} "+platform_query+s1+s2+f" AND geoip_city IN {geoip_city_tuple} AND platform IS NOT NULL AND ids_threat_class IS NOT NULL GROUP BY platform, geoip_city ORDER BY geoip_city_count desc;"
        
        run_sql2 = opensearch_conn_using_db(sql2, location_id, plan_id)

        if run_sql2.get("total") not in [0, None]:
            # formatting sql2 query output as (key, value) pairs in dictionary

            key_names = []
            for i,n in enumerate(run_sql2.get('schema')):
                if n.get('name') == 'count(geoip_city)':
                    key_names.append(n.get('alias'))
                else:
                    key_names.append(n.get('name'))
            
            table_query_list = []
            for i, key_values in enumerate(run_sql2.get('datarows')):
                Dict = {}
                Dict.update(dict(zip(key_names, key_values)))
                Dict["past_time"] = past_time
                Dict["current_time"] = current_time

                table_query_list.append(Dict)
        else:
            return Response({"message_type":"d_not_f"})
        
        return Response({"message_type":"success", "pie_chart":pie_chart_dict, "filter":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 17.b Pie chart on geoip_city column--Table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_city_pie_table(request):
    city_name = request.GET.get('geoip_city')
    if city_name is None:
        return Response({"message_type": "d_not_f", "errors": "geoip_city_not_found"})
    
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    platform_name = request.GET.get('platform')

    if platform_name is None:
        return Response({"message_type": "d_not_f","errors": "platform_name_not_found"})
    
    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f'''SELECT platform, type_of_threat, attacker_ip, attacker_mac, attack_timestamp, ids_threat_class, ids_threat_type, ml_threat_class, dl_threat_class, ml_accuracy, dl_accuracy, attacker_port, target_port, target_ip, geoip_city, geoip_country_name, geoip_asn_name FROM {indice_name}-* WHERE geoip_city = "{city_name}" AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform = '{platform_name}' AND ids_threat_class IS NOT NULL '''+s1+s2+f''' ORDER BY attack_epoch_time DESC limit 200000;'''
    
    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)
    
    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [item['name'] for item in run_sql.get('schema')]
        
        table_query_list = []
        for i, row in enumerate(run_sql.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
            
        return Response({"message_type":"success", "count":len(table_query_list), "city_name":city_name,"table":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 18.a Card Name: Attacker ASN (Bar chart on geoip_asn_name column)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_asn_bar_chart(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    platform_tuple = detail_dict.get("platform_tuple")
    platform_query = f"AND platform IN {platform_tuple} " if platform_tuple is not None else ""

    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    sql = f"SELECT geoip_asn_name, COUNT(geoip_asn_name) FROM {indice_name}-* WHERE geoip_asn_name NOT LIKE 'NA' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL "+platform_query+s1+s2+f" GROUP BY geoip_asn_name ORDER BY COUNT(geoip_asn_name) desc LIMIT 7;"
    
    run_sql_query = opensearch_conn_using_db(sql, location_id, plan_id)
    
    if run_sql_query.get("total") not in exclude_values:
        geoip_asn, asn_count = map(list, zip(*run_sql_query['datarows']))
        bar_chart_dict = {"series": asn_count, "labels": geoip_asn}

        col_val = str(geoip_asn).strip("[]")
        geoip_asn_tuple = "(" + col_val + ")"
    
        # for grouping according to platform
        sql2 = f"SELECT platform, geoip_asn_name, count(geoip_asn_name) geoip_asn_name_count FROM {indice_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} "+platform_query+s1+s2+f" AND geoip_asn_name IN {geoip_asn_tuple} AND platform IS NOT NULL AND ids_threat_class IS NOT NULL GROUP BY platform, geoip_asn_name ORDER BY geoip_asn_name_count desc;"
        
        run_sql2 = opensearch_conn_using_db(sql2, location_id, plan_id)

        if run_sql2.get("total") not in [0, None]:
            # formatting sql2 query output as (key, value) pairs in dictionary

            key_names = []
            for i,n in enumerate(run_sql2.get('schema')):
                if n.get('name') == 'count(geoip_asn_name)':
                    key_names.append(n.get('alias'))
                else:
                    key_names.append(n.get('name'))
            
            table_query_list = []
            for i, key_values in enumerate(run_sql2.get('datarows')):
                Dict = {}
                Dict.update(dict(zip(key_names, key_values)))
                Dict["past_time"] = past_time
                Dict["current_time"] = current_time

                table_query_list.append(Dict)
        else:
            return Response({"message_type":"d_not_f"})
        
        return Response({"message_type":"success", "bar_chart":bar_chart_dict, "filter":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 18.b Bar chart on geoip_asn_name column--Table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_asn_bar_table(request):
    asn_name = request.GET.get('geoip_asn_name')
    if asn_name is None:
        return Response({"message_type": "d_not_f", "errors": "geoip_asn_name_not_found"})
    
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    platform_name = request.GET.get('platform')

    if platform_name is None:
        return Response({"message_type": "d_not_f","errors": "platform_name_not_found"})
    
    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT platform, type_of_threat, attacker_ip, attacker_mac, attack_timestamp, ids_threat_class, ids_threat_type, ml_threat_class, dl_threat_class, ml_accuracy, dl_accuracy, attacker_port, target_port, target_ip, geoip_city, geoip_country_name, geoip_asn_name FROM {indice_name}-* WHERE geoip_asn_name = '{asn_name}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform = '{platform_name}' AND ids_threat_class IS NOT NULL "+s1+s2+f" ORDER BY attack_epoch_time DESC limit 200000;"
    
    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)
    
    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [item['name'] for item in run_sql.get('schema')]
        
        table_query_list = []
        for i, row in enumerate(run_sql.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
            
        return Response({"message_type":"success", "count":len(table_query_list), "asn_name":asn_name,"table":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 19.a Card Name: Target IP (Pie chart on target_ip column)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_target_ip_pie_chart(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    platform_tuple = detail_dict.get("platform_tuple")
    platform_query = f"AND platform IN {platform_tuple} " if platform_tuple is not None else ""

    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    sql = f"SELECT target_ip, COUNT(target_ip) FROM {indice_name}-* WHERE (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL "+platform_query+s1+s2+f" GROUP BY target_ip ORDER BY COUNT(target_ip) desc LIMIT 7;"
    
    run_sql_query = opensearch_conn_using_db(sql, location_id, plan_id)
    
    if run_sql_query.get("total") not in exclude_values:
        target_ip, target_ip_count = map(list, zip(*run_sql_query['datarows']))

        bar_chart_dict = {"series": target_ip_count, "labels": target_ip}
        
        
        col_val = str(target_ip).strip("[]")
        target_ip_tuple = "(" + col_val + ")"
    
        # for grouping according to platform
        sql2 = f"SELECT platform, target_ip, count(target_ip) target_ip_count FROM {indice_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} "+platform_query+s1+s2+f" AND target_ip IN {target_ip_tuple} AND platform IS NOT NULL AND ids_threat_class IS NOT NULL GROUP BY platform, target_ip ORDER BY target_ip_count desc;"
        
        run_sql2 = opensearch_conn_using_db(sql2, location_id, plan_id)

        if run_sql2.get("total") not in [0, None]:
            # formatting sql2 query output as (key, value) pairs in dictionary

            key_names = []
            for i,n in enumerate(run_sql2.get('schema')):
                if n.get('name') == 'count(target_ip)':
                    key_names.append(n.get('alias'))
                else:
                    key_names.append(n.get('name'))
            
            table_query_list = []
            for i, key_values in enumerate(run_sql2.get('datarows')):
                Dict = {}
                Dict.update(dict(zip(key_names, key_values)))
                Dict["past_time"] = past_time
                Dict["current_time"] = current_time

                table_query_list.append(Dict)
        else:
            return Response({"message_type":"d_not_f"})
        
        return Response({"message_type":"success", "bar_chart":bar_chart_dict, "filter":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 19.b Pie chart on target_ip column--Table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_target_ip_table(request):
    target_ip = request.GET.get('target_ip')
    if target_ip is None:
        return Response({"message_type": "d_not_f", "errors": "target_ip_not_found"})
    
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    platform_name = request.GET.get('platform')

    if platform_name is None:
        return Response({"message_type": "d_not_f","errors": "platform_name_not_found"})
    
    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT platform, type_of_threat, attacker_ip, attacker_mac, attack_timestamp, ids_threat_class, ids_threat_type, ml_threat_class, dl_threat_class, ml_accuracy, dl_accuracy, attacker_port, target_port, target_ip, geoip_city, geoip_country_name, geoip_asn_name FROM {indice_name}-* WHERE target_ip = '{target_ip}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform = '{platform_name}' AND ids_threat_class IS NOT NULL "+s1+s2+f" ORDER BY attack_epoch_time DESC limit 200000;"
    
    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)
    
    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [item['name'] for item in run_sql.get('schema')]
        
        table_query_list = []
        for i, row in enumerate(run_sql.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
            
        return Response({"message_type":"success", "count":len(table_query_list), "target_ip":target_ip,"table":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 20.a Card Name: Target MAC (Pie chart on target_mac column)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_target_mac_pie_chart(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    platform_tuple = detail_dict.get("platform_tuple")
    platform_query = f"AND platform IN {platform_tuple} " if platform_tuple is not None else ""

    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    sql = f"SELECT target_mac, COUNT(target_mac) FROM {indice_name}-* WHERE (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL AND target_mac IS NOT NULL "+platform_query+s1+s2+f" GROUP BY target_mac ORDER BY COUNT(target_mac) desc LIMIT 7;"
    
    run_sql_query = opensearch_conn_using_db(sql, location_id, plan_id)
    
    if run_sql_query.get("total") not in exclude_values:
        target_mac, target_mac_count = map(list, zip(*run_sql_query['datarows']))
        bar_chart_dict = {"series": target_mac_count, "labels": target_mac}
        
        
        col_val = str(target_mac).strip("[]")
        target_mac_tuple = "(" + col_val + ")"
    
        # for grouping according to platform
        sql2 = f"SELECT platform, target_mac, count(target_mac) target_mac_count FROM {indice_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} "+platform_query+s1+s2+f" AND target_mac IN {target_mac_tuple} AND platform IS NOT NULL AND ids_threat_class IS NOT NULL GROUP BY platform, target_mac ORDER BY target_mac_count desc;"
        
        run_sql2 = opensearch_conn_using_db(sql2, location_id, plan_id)

        if run_sql2.get("total") not in [0, None]:
            # formatting sql2 query output as (key, value) pairs in dictionary

            key_names = []
            for i,n in enumerate(run_sql2.get('schema')):
                if n.get('name') == 'count(target_mac)':
                    key_names.append(n.get('alias'))
                else:
                    key_names.append(n.get('name'))
            
            table_query_list = []
            for i, key_values in enumerate(run_sql2.get('datarows')):
                Dict = {}
                Dict.update(dict(zip(key_names, key_values)))
                Dict["past_time"] = past_time
                Dict["current_time"] = current_time

                table_query_list.append(Dict)
        else:
            return Response({"message_type":"d_not_f"})
        
        return Response({"message_type":"success", "bar_chart":bar_chart_dict, "filter":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 20.b Pie chart on target_mac column--Table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_target_mac_table(request):
    target_mac = request.GET.get('target_mac')
    if target_mac is None:
        return Response({"message_type": "d_not_f", "errors": "target_mac_not_found"})
    
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type": "d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    platform_name = request.GET.get('platform')

    if platform_name is None:
        return Response({"message_type": "d_not_f","errors": "platform_name_not_found"})
    
    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT platform, type_of_threat, attacker_ip, attacker_mac, attack_timestamp, ids_threat_class, ids_threat_type, ml_threat_class, dl_threat_class, ml_accuracy, dl_accuracy, attacker_port, target_port, target_ip, geoip_city, geoip_country_name, geoip_asn_name FROM {indice_name}-* WHERE target_mac = '{target_mac}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform = '{platform_name}' AND ids_threat_class IS NOT NULL "+s1+s2+f" ORDER BY attack_epoch_time DESC limit 200000;"
    
    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)
    
    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [item['name'] for item in run_sql.get('schema')]
        
        table_query_list = []
        for i, row in enumerate(run_sql.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
            
        return Response({"message_type":"success", "count":len(table_query_list), "target_mac":target_mac,"table":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 21.a Card Name: Target Port (Pie chart on target_port column)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_target_port_pie_chart(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    platform_tuple = detail_dict.get("platform_tuple")
    platform_query = f"AND platform IN {platform_tuple} " if platform_tuple is not None else ""

    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    sql = f"SELECT target_port, COUNT(target_port) FROM {indice_name}-* WHERE (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL AND target_port IS NOT NULL "+platform_query+s1+s2+f" GROUP BY target_port ORDER BY COUNT(target_port) desc LIMIT 7;"
    
    run_sql_query = opensearch_conn_using_db(sql, location_id, plan_id)
    
    if run_sql_query.get("total") not in exclude_values:
        target_port, target_port_count = map(list, zip(*run_sql_query['datarows']))
        bar_chart_dict = {"series": target_port_count, "labels": target_port}

        col_val = str(target_port).strip("[]")
        target_port_tuple = "(" + col_val + ")"
    
        # for grouping according to platform
        sql2 = f"SELECT platform, target_port, count(target_port) target_port_count FROM {indice_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} "+platform_query+s1+s2+f" AND target_port IN {target_port_tuple} AND platform IS NOT NULL AND ids_threat_class IS NOT NULL GROUP BY platform, target_port ORDER BY target_port_count desc;"
        
        run_sql2 = opensearch_conn_using_db(sql2, location_id, plan_id)

        if run_sql2.get("total") not in [0, None]:
            # formatting sql2 query output as (key, value) pairs in dictionary

            key_names = []
            for i,n in enumerate(run_sql2.get('schema')):
                if n.get('name') == 'count(target_port)':
                    key_names.append(n.get('alias'))
                else:
                    key_names.append(n.get('name'))
            
            table_query_list = []
            for i, key_values in enumerate(run_sql2.get('datarows')):
                Dict = {}
                Dict.update(dict(zip(key_names, key_values)))
                Dict["past_time"] = past_time
                Dict["current_time"] = current_time

                table_query_list.append(Dict)
        else:
            return Response({"message_type":"d_not_f"})
        
        return Response({"message_type":"success", "bar_chart":bar_chart_dict, "filter":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 21.b Pie chart on target_port column--Table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_target_port_table(request):
    target_port = request.GET.get('target_port')
    if target_port is None:
        return Response({"message_type": "d_not_f", "errors": "target_port_not_found"})
    
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    platform_name = request.GET.get('platform')

    if platform_name is None:
        return Response({"message_type": "d_not_f","errors": "platform_name_not_found"})
    
    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT platform, type_of_threat, attacker_ip, attacker_mac, attack_timestamp, ids_threat_class, ids_threat_type, ml_threat_class, dl_threat_class, ml_accuracy, dl_accuracy, attacker_port, target_port, target_ip, geoip_city, geoip_country_name, geoip_asn_name FROM {indice_name}-* WHERE target_port = {target_port} AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform = '{platform_name}' AND ids_threat_class IS NOT NULL "+s1+s2+f" ORDER BY attack_epoch_time DESC limit 200000;"
    
    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)
    
    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [item['name'] for item in run_sql.get('schema')]
        
        table_query_list = []
        for i, row in enumerate(run_sql.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
            
        return Response({"message_type":"success", "count":len(table_query_list), "target_port":target_port,"table":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 22 Card Name: Frequent Attacker Details--only table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_freq_attacker(request):
    condition = request.GET.get('condition')
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id
    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    platform_tuple = detail_dict.get("platform_tuple")
    platform_query = f"AND platform IN {platform_tuple} " if platform_tuple is not None else ""

    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    sql_query = f"SELECT attacker_ip,target_mac,type_of_threat, count(attacker_ip) attacker_ip_count FROM {indice_name}-* WHERE attacker_ip IS NOT NULL AND type_of_threat IS NOT NULL "+platform_query+s1+s2+f" AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} AND ids_threat_class IS NOT NULL GROUP BY attacker_ip,target_mac,type_of_threat ORDER BY attacker_ip_count DESC LIMIT 50;"
    
    api_response = opensearch_conn_using_db(sql_query, location_id, plan_id)
    
    if api_response.get("total") not in exclude_values:
        key_names = [item['alias'] if (item['name'] == "count(attacker_ip)") else item['name'] for item in api_response.get('schema')]
        
        final_response = []
        for i in range(len(api_response.get('datarows'))):
            row = api_response.get('datarows')[i]
            final_response.append(dict(zip(key_names, row)))
        
        return Response({"message_type":"success", "data":final_response})
    else:
        return Response({"message_type":"d_not_f"})

# 23 Card Name: Top Attacked Services --only table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_attacked_service_details(request):
    condition = request.GET.get('condition')
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    platform_tuple = detail_dict.get("platform_tuple")
    platform_query = f"AND platform IN {platform_tuple} " if platform_tuple is not None else ""

    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""

    sql_query = f"SELECT attacker_ip, service_name, count(*) service_name_count FROM {indice_name}-* WHERE attacker_ip IS NOT NULL AND service_name NOT LIKE 'NA' AND type_of_threat IS NOT NULL "+platform_query+s1+s2+f" AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} AND ids_threat_class IS NOT NULL GROUP BY attacker_ip,service_name ORDER BY service_name_count DESC LIMIT 50;"
    
    api_response = opensearch_conn_using_db(sql_query, location_id, plan_id)
    
    if api_response.get("total") not in exclude_values:
        key_names = [item['alias'] if (item['name'] == "count(*)") else item['name'] for item in api_response.get('schema')]
        
        final_response = []
        for i in range(len(api_response.get('datarows'))):
            row = api_response.get('datarows')[i]
            final_response.append(dict(zip(key_names, row)))
        
        return Response({"message_type":"success", "data":final_response})
    else:
        return Response({"message_type":"d_not_f"})

############################################ IDS Cards END ###########################################################################

# ML DL range cards
# 24.a. Card Name:  Detected Threat Type -----(i).ML (ii).DL (iii). IDS
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_ml_detected_threat(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type": "d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    platform_tuple = detail_dict.get("platform_tuple")
    platform_query = f"AND platform IN {platform_tuple}" if platform_tuple is not None else ""

    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    accuracy_val = detail_dict.get("accuracy_val")
    accuracy1, accuracy2 = getMlDlAccuracyRanges(accuracy_val)
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
     
    ml_sql_query = f"SELECT platform, ml_threat_class, count(ml_threat_class) ml_count FROM {indice_name}-* WHERE ml_threat_class IS NOT NULL AND ml_threat_class !='undefined class' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NULL and ((ml_accuracy>{accuracy1} AND ml_accuracy<={accuracy2}) OR (dl_accuracy>{accuracy1} AND dl_accuracy<={accuracy2})) "+platform_query+s1+s2+f" GROUP BY platform, ml_threat_class ORDER BY ml_count desc LIMIT 7;"
    
    dl_sql_query = f"SELECT platform, dl_threat_class, count(dl_threat_class) dl_count FROM {indice_name}-* WHERE dl_threat_class IS NOT NULL AND dl_threat_class !='undefined class' and (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NULL and ((ml_accuracy>{accuracy1} AND ml_accuracy<={accuracy2}) OR (dl_accuracy>{accuracy1} AND dl_accuracy<={accuracy2})) "+platform_query+s1+s2+f" GROUP BY platform, dl_threat_class ORDER BY dl_count desc LIMIT 7;"

    ml_query_output = opensearch_conn_using_db(ml_sql_query, location_id, plan_id)
    dl_query_output = opensearch_conn_using_db(dl_sql_query, location_id, plan_id)
    
    # Check if all "total" values are in the exclude_values set
    if all(value.get("total") not in exclude_values for value in [ml_query_output, dl_query_output]):
        
        ml_threat_list = []
        platform, ml_threat_class_list,ml_threat_class_count= map(list, zip(*ml_query_output['datarows']))
        
        ml_threat_list = [{
            "name": name,
            "platform": platform,
            "value": count,
            "past_time": past_time,
            "current_time": current_time
        } for platform, name, count in zip(platform, ml_threat_class_list, ml_threat_class_count)]
        
        
        dl_threat_list = []
        platform, dl_threat_class_list,dl_threat_class_count= map(list, zip(*dl_query_output['datarows']))
        
        dl_threat_list = [{
            "name": name,
            "platform": platform,
            "value": count,
            "past_time": past_time,
            "current_time": current_time
        } for platform, name, count in zip(platform, dl_threat_class_list, dl_threat_class_count)]
        
        response_dict = {"ml":ml_threat_list, "dl":dl_threat_list} 
        
        return Response({"message_type": "success", "detected_threat_type":response_dict})
    else:
        return Response({"message_type": "d_not_f"})

# 24.b. ML DL Range Detected Threat Type card---Table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_ml_detected_threat_table(request):
    threat_class_type = request.GET.get('type')
    if threat_class_type is None:
        return Response({"message_type": "d_not_f", "errors": "type_not_f"})    
    
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    accuracy_val = detail_dict.get("accuracy_val")
    accuracy1, accuracy2 = getMlDlAccuracyRanges(accuracy_val)
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    threat_class_name = request.GET.get('name')
    if threat_class_name is None:
        return Response({"message_type": "d_not_f", "errors": "name_not_f"})
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    platform_name = request.GET.get('platform')

    if platform_name is None:
        return Response({"message_type": "d_not_f","errors": "platform_name_not_found"})
    
    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_f"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_f"})
    
    threat_class_type_dict = {
        "ml": "ml_threat_class",
        "dl": "dl_threat_class"
    }
    
    if threat_class_type in threat_class_type_dict:
        
        # sql query to get table data
        table_query = f"SELECT platform, type_of_threat, attacker_ip, attacker_mac, attack_timestamp, ids_threat_class, ids_threat_type, ml_threat_class, dl_threat_class, ml_accuracy, dl_accuracy, attacker_port, target_port, target_ip, geoip_city, geoip_country_name, geoip_asn_name FROM {indice_name}-* WHERE {threat_class_type_dict[threat_class_type]} = '{threat_class_name}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NULL AND platform = '{platform_name}' AND ((ml_accuracy>{accuracy1} AND ml_accuracy<={accuracy2}) OR (dl_accuracy>{accuracy1} AND dl_accuracy<={accuracy2})) "+s1+s2+f" ORDER BY attack_epoch_time DESC limit 200000;"

        run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)
    
        # formatting above query output to {column_name: column_value}
        if run_sql.get("total") not in exclude_values:
            key_names = [item['name'] for item in run_sql.get('schema')]
        
            table_query_list = []
            for i, row in enumerate(run_sql.get('datarows')):
                Dict = {}
                Dict.update(dict(zip(key_names, row)))
                table_query_list.append(Dict)
                
            return Response({"message_type":"success", "count":len(table_query_list), f"{threat_class_type_dict[threat_class_type]}":threat_class_name,"table":table_query_list})
        else:
            return Response({"message_type": "d_not_f"})
    else:
        return Response({"message_type": "d_not_f", "errors": "type_not_f"})

# 25.a. ML DL-Card Name: Attacker Geo-Locations
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_ml_map(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)
    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    platform_tuple = detail_dict.get("platform_tuple")
    platform_query = f"AND platform IN {platform_tuple} " if platform_tuple is not None else ""

    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    accuracy_val = detail_dict.get("accuracy_val")
    accuracy1, accuracy2 = getMlDlAccuracyRanges(accuracy_val)
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})

    sql = f"SELECT geoip_city, geoip_latitude,geoip_longitude, count(*) count FROM {indice_name}-* WHERE geoip_country_name IS NOT NULL AND geoip_latitude IS NOT NULL AND geoip_longitude IS NOT NULL AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NULL and ((ml_accuracy>{accuracy1} AND ml_accuracy<={accuracy2}) OR (dl_accuracy>{accuracy1} AND dl_accuracy<={accuracy2})) "+platform_query+s1+s2+f" GROUP BY geoip_city,geoip_latitude,geoip_longitude ORDER BY count desc LIMIT 20;"
    
    run_sql = opensearch_conn_using_db(sql, location_id, plan_id)
    
    map_value = []
    if run_sql.get("total") not in exclude_values:
        geoip_city, geoip_latitude, geoip_longitude, attack_count = map(list, zip(*run_sql['datarows']))
        latandlon = zip(geoip_longitude, geoip_latitude)
        for (m, n) in zip(latandlon, geoip_city):
            map_value.append({"position": m, "title": n})
        
        col_val = str(geoip_city).strip("[]")
        geoip_city_tuple = "(" + col_val + ")"
    
        # for grouping according to platform
        sql2 = f"SELECT platform, geoip_city, count(geoip_city) geoip_city_count FROM {indice_name}-* WHERE geoip_country_name IS NOT NULL AND geoip_latitude IS NOT NULL AND geoip_longitude IS NOT NULL AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) and ((ml_accuracy>{accuracy1} AND ml_accuracy<={accuracy2}) OR (dl_accuracy>{accuracy1} AND dl_accuracy<={accuracy2})) "+platform_query+s1+s2+f" AND geoip_city IN {geoip_city_tuple} AND platform IS NOT NULL AND ids_threat_class IS NULL GROUP BY platform, geoip_city ORDER BY geoip_city_count desc;"
        
        run_sql2 = opensearch_conn_using_db(sql2, location_id, plan_id)

        if run_sql2.get("total") not in [0, None]:
            # formatting sql2 query output as (key, value) pairs in dictionary

            key_names = []
            for i,n in enumerate(run_sql2.get('schema')):
                if n.get('name') == 'count(geoip_city)':
                    key_names.append(n.get('alias'))
                else:
                    key_names.append(n.get('name'))
            
            table_query_list = []
            for i, key_values in enumerate(run_sql2.get('datarows')):
                Dict = {}
                Dict.update(dict(zip(key_names, key_values)))
                Dict["past_time"] = past_time
                Dict["current_time"] = current_time

                table_query_list.append(Dict)
        else:
            return Response({"message_type":"d_not_f"})
        
        return Response({"message_type":"success", "geolocation":map_value, "filter":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})


# 25.b. ML DL-geolocation Table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_ml_map_table(request):
    city_name = request.GET.get('geoip_city')
    if city_name is None:
        return Response({"message_type": "d_not_f", "errors": "geoip_city_not_found"})
    
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    accuracy_val = detail_dict.get("accuracy_val")
    accuracy1, accuracy2 = getMlDlAccuracyRanges(accuracy_val)
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    platform_name = request.GET.get('platform')

    if platform_name is None:
        return Response({"message_type": "d_not_f","errors": "platform_name_not_found"})
    
    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f'''SELECT platform, type_of_threat, attacker_ip, attacker_mac, attack_timestamp, ids_threat_class, ids_threat_type, ml_threat_class, dl_threat_class, ml_accuracy, dl_accuracy, attacker_port, target_port, target_ip, geoip_city, geoip_country_name, geoip_asn_name FROM {indice_name}-* WHERE geoip_latitude IS NOT NULL AND geoip_longitude IS NOT NULL AND geoip_city = "{city_name}" AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform = '{platform_name}' AND ids_threat_class IS NULL and ((ml_accuracy>{accuracy1} AND ml_accuracy<={accuracy2}) OR (dl_accuracy>{accuracy1} AND dl_accuracy<={accuracy2})) '''+s1+s2+f''' ORDER BY attack_epoch_time DESC limit 200000;'''
      
    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)
    
    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [item['name'] for item in run_sql.get('schema')]
        
        table_query_list = []
        for i, row in enumerate(run_sql.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
            
        return Response({"message_type":"success", "count":len(table_query_list), "city_name":city_name,"table":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 26.a ML DL- Card Name: Top Source Attack Countries (Bar chart on geoip_country_name column)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_ml_cntry_bar(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    platform_tuple = detail_dict.get("platform_tuple")
    platform_query = f"AND platform IN {platform_tuple} " if platform_tuple is not None else ""

    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    accuracy_val = detail_dict.get("accuracy_val")
    accuracy1, accuracy2 = getMlDlAccuracyRanges(accuracy_val)
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    sql = f"SELECT geoip_country_name, COUNT(geoip_country_name) FROM {indice_name}-* WHERE geoip_country_name NOT LIKE 'NA' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NULL and ((ml_accuracy>{accuracy1} AND ml_accuracy<={accuracy2}) OR (dl_accuracy>{accuracy1} AND dl_accuracy<={accuracy2})) "+platform_query+s1+s2+f" GROUP BY geoip_country_name ORDER BY COUNT(geoip_country_name) desc LIMIT 7;"
    
    run_sql_query = opensearch_conn_using_db(sql, location_id, plan_id)
    
    if run_sql_query.get("total") not in exclude_values:
        geoip_country, country_count = map(list, zip(*run_sql_query['datarows']))
        bar_chart_dict = {"series": country_count, "labels": geoip_country}

        col_val = str(geoip_country).strip("[]")
        geoip_country_tuple = "(" + col_val + ")"
    
        # for grouping according to platform
        sql2 = f"SELECT platform, geoip_country_name, count(geoip_country_name) geoip_country_name_count FROM {indice_name}-* WHERE geoip_country_name NOT LIKE 'NA' AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} and ((ml_accuracy>{accuracy1} AND ml_accuracy<={accuracy2}) OR (dl_accuracy>{accuracy1} AND dl_accuracy<={accuracy2}))"+platform_query+s1+s2+f" AND geoip_country_name IN {geoip_country_tuple} AND platform IS NOT NULL AND ids_threat_class IS NULL GROUP BY platform, geoip_country_name ORDER BY geoip_country_name_count desc;"
        
        run_sql2 = opensearch_conn_using_db(sql2, location_id, plan_id)

        if run_sql2.get("total") not in [0, None]:
            # formatting sql2 query output as (key, value) pairs in dictionary

            key_names = []
            for i,n in enumerate(run_sql2.get('schema')):
                if n.get('name') == 'count(geoip_country_name)':
                    key_names.append(n.get('alias'))
                else:
                    key_names.append(n.get('name'))
            
            table_query_list = []
            for i, key_values in enumerate(run_sql2.get('datarows')):
                Dict = {}
                Dict.update(dict(zip(key_names, key_values)))
                Dict["past_time"] = past_time
                Dict["current_time"] = current_time

                table_query_list.append(Dict)
        else:
            return Response({"message_type":"d_not_f"})  
        
        return Response({"message_type":"success", "bar_chart":bar_chart_dict, "filter":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 26.b ML DL-Bar chart on geoip_country_name column--Table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_ml_cntry_bar_table(request):
    country_name = request.GET.get('geoip_country_name')
    if country_name is None:
        return Response({"message_type": "d_not_f", "errors": "geoip_country_name_not_found"})
    
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    accuracy_val = detail_dict.get("accuracy_val")
    accuracy1, accuracy2 = getMlDlAccuracyRanges(accuracy_val)
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    platform_name = request.GET.get('platform')

    if platform_name is None:
        return Response({"message_type": "d_not_f","errors": "platform_name_not_found"})
    
    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f'''SELECT platform, type_of_threat, attacker_ip, attacker_mac, attack_timestamp, ids_threat_class, ids_threat_type, ml_threat_class, dl_threat_class, ml_accuracy, dl_accuracy, attacker_port, target_port, target_ip, geoip_city, geoip_country_name, geoip_asn_name FROM {indice_name}-* WHERE geoip_country_name NOT LIKE 'NA' AND geoip_country_name = "{country_name}" AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform = '{platform_name}' AND ids_threat_class IS NULL and ((ml_accuracy>{accuracy1} AND ml_accuracy<={accuracy2}) OR (dl_accuracy>{accuracy1} AND dl_accuracy<={accuracy2})) '''+s1+s2+f''' ORDER BY attack_epoch_time DESC limit 200000;'''
    
    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)
    
    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [item['name'] for item in run_sql.get('schema')]
        
        table_query_list = []
        for i, row in enumerate(run_sql.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
            
        return Response({"message_type":"success", "count":len(table_query_list), "country_name":country_name,"table":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 27.a ML DL-Card Name: Attacker ASN (Bar chart on geoip_asn_name column)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_ml_asn_bar(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    platform_tuple = detail_dict.get("platform_tuple")
    platform_query = f"AND platform IN {platform_tuple} " if platform_tuple is not None else ""

    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    accuracy_val = detail_dict.get("accuracy_val")
    accuracy1, accuracy2 = getMlDlAccuracyRanges(accuracy_val)
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    sql = f"SELECT geoip_asn_name, COUNT(geoip_asn_name) FROM {indice_name}-* WHERE geoip_asn_name NOT LIKE 'NA' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NULL and ((ml_accuracy>{accuracy1} AND ml_accuracy<={accuracy2}) OR (dl_accuracy>{accuracy1} AND dl_accuracy<={accuracy2})) "+platform_query+s1+s2+f" GROUP BY geoip_asn_name ORDER BY COUNT(geoip_asn_name) desc LIMIT 7;"
    
    run_sql_query = opensearch_conn_using_db(sql, location_id, plan_id)
    
    if run_sql_query.get("total") not in exclude_values:
        geoip_asn, asn_count = map(list, zip(*run_sql_query['datarows']))
        bar_chart_dict = {"series": asn_count, "labels": geoip_asn}

        col_val = str(geoip_asn).strip("[]")
        geoip_asn_tuple = "(" + col_val + ")"
    
        # for grouping according to platform
        sql2 = f"SELECT platform, geoip_asn_name, count(geoip_asn_name) geoip_asn_name_count FROM {indice_name}-* WHERE geoip_asn_name NOT LIKE 'NA' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) and ((ml_accuracy>{accuracy1} AND ml_accuracy<={accuracy2}) OR (dl_accuracy>{accuracy1} AND dl_accuracy<={accuracy2})) "+platform_query+s1+s2+f" AND geoip_asn_name IN {geoip_asn_tuple} AND platform IS NOT NULL AND ids_threat_class IS NULL GROUP BY platform, geoip_asn_name ORDER BY geoip_asn_name_count desc;"
        
        run_sql2 = opensearch_conn_using_db(sql2, location_id, plan_id)

        if run_sql2.get("total") not in [0, None]:
            # formatting sql2 query output as (key, value) pairs in dictionary

            key_names = []
            for i,n in enumerate(run_sql2.get('schema')):
                if n.get('name') == 'count(geoip_asn_name)':
                    key_names.append(n.get('alias'))
                else:
                    key_names.append(n.get('name'))
            
            table_query_list = []
            for i, key_values in enumerate(run_sql2.get('datarows')):
                Dict = {}
                Dict.update(dict(zip(key_names, key_values)))
                Dict["past_time"] = past_time
                Dict["current_time"] = current_time

                table_query_list.append(Dict)
        else:
            return Response({"message_type":"d_not_f"})
        
        return Response({"message_type":"success", "bar_chart":bar_chart_dict, "filter":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 27.b ML DL-Bar chart on geoip_asn_name column--Table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_ml_asn_table(request):
    asn_name = request.GET.get('geoip_asn_name')
    if asn_name is None:
        return Response({"message_type": "d_not_f", "errors": "geoip_asn_name_not_found"})
    
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    accuracy_val = detail_dict.get("accuracy_val")
    accuracy1, accuracy2 = getMlDlAccuracyRanges(accuracy_val)
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    platform_name = request.GET.get('platform')

    if platform_name is None:
        return Response({"message_type": "d_not_f","errors": "platform_name_not_found"})
    
    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT platform, type_of_threat, attacker_ip, attacker_mac, attack_timestamp, ids_threat_class, ids_threat_type, ml_threat_class, dl_threat_class, ml_accuracy, dl_accuracy, attacker_port, target_port, target_ip, geoip_city, geoip_country_name, geoip_asn_name FROM {indice_name}-* WHERE geoip_asn_name = '{asn_name}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform = '{platform_name}' AND ids_threat_class IS NULL and ((ml_accuracy>{accuracy1} AND ml_accuracy<={accuracy2}) OR (dl_accuracy>{accuracy1} AND dl_accuracy<={accuracy2})) "+s1+s2+f" ORDER BY attack_epoch_time DESC limit 200000;"
    
    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)
    
    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [item['name'] for item in run_sql.get('schema')]
        
        table_query_list = []
        for i, row in enumerate(run_sql.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
            
        return Response({"message_type":"success", "count":len(table_query_list), "asn_name":asn_name,"table":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 28.a ML DL-Card Name: Top Attacker City (Pie chart on geoip_city column)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_ml_city_pie(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    platform_tuple = detail_dict.get("platform_tuple")
    platform_query = f"AND platform IN {platform_tuple} " if platform_tuple is not None else ""

    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")

    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    accuracy_val = detail_dict.get("accuracy_val")
    accuracy1, accuracy2 = getMlDlAccuracyRanges(accuracy_val)
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    sql = f"SELECT geoip_city, COUNT(geoip_city) FROM {indice_name}-* WHERE geoip_city NOT LIKE 'NA' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NULL AND geoip_city IS NOT NULL and ((ml_accuracy>{accuracy1} AND ml_accuracy<={accuracy2}) OR (dl_accuracy>{accuracy1} AND dl_accuracy<={accuracy2})) "+platform_query+s1+s2+f" GROUP BY geoip_city ORDER BY COUNT(geoip_city) desc LIMIT 7;"
    
    run_sql_query = opensearch_conn_using_db(sql, location_id, plan_id)
    
    if run_sql_query.get("total") not in exclude_values:
        geoip_city, city_count = map(list, zip(*run_sql_query['datarows']))
        pie_chart_dict = {"series": city_count, "labels": geoip_city}
        
        
        col_val = str(geoip_city).strip("[]")
        geoip_city_tuple = "(" + col_val + ")"
    
        # for grouping according to platform
        sql2 = f"SELECT platform, geoip_city, count(geoip_city) geoip_city_count FROM {indice_name}-* WHERE (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) and ((ml_accuracy>{accuracy1} AND ml_accuracy<={accuracy2}) OR (dl_accuracy>{accuracy1} AND dl_accuracy<={accuracy2})) "+platform_query+s1+s2+f" AND geoip_city IN {geoip_city_tuple} AND platform IS NOT NULL AND ids_threat_class IS NULL GROUP BY platform, geoip_city ORDER BY geoip_city_count desc;"
        
        run_sql2 = opensearch_conn_using_db(sql2, location_id, plan_id)

        if run_sql2.get("total") not in [0, None]:
            # formatting sql2 query output as (key, value) pairs in dictionary

            key_names = []
            for i,n in enumerate(run_sql2.get('schema')):
                if n.get('name') == 'count(geoip_city)':
                    key_names.append(n.get('alias'))
                else:
                    key_names.append(n.get('name'))
            
            table_query_list = []
            for i, key_values in enumerate(run_sql2.get('datarows')):
                Dict = {}
                Dict.update(dict(zip(key_names, key_values)))
                Dict["past_time"] = past_time
                Dict["current_time"] = current_time

                table_query_list.append(Dict)
        else:
            return Response({"message_type":"d_not_f"})
        
        return Response({"message_type":"success", "pie_chart":pie_chart_dict, "filter":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 28.b ML DL-Pie chart on geoip_city column--Table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_ml_city_table(request):
    city_name = request.GET.get('geoip_city')
    if city_name is None:
        return Response({"message_type": "d_not_f", "errors": "geoip_city_not_found"})
    
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    accuracy_val = detail_dict.get("accuracy_val")
    accuracy1, accuracy2 = getMlDlAccuracyRanges(accuracy_val)
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    platform_name = request.GET.get('platform')

    if platform_name is None:
        return Response({"message_type": "d_not_f","errors": "platform_name_not_found"})
    
    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f'''SELECT platform, type_of_threat, attacker_ip, attacker_mac, attack_timestamp, ids_threat_class, ids_threat_type, ml_threat_class, dl_threat_class, ml_accuracy, dl_accuracy, attacker_port, target_port, target_ip, geoip_city, geoip_country_name, geoip_asn_name FROM {indice_name}-* WHERE geoip_city = "{city_name}" AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform = '{platform_name}' AND ids_threat_class IS NULL and ((ml_accuracy>{accuracy1} AND ml_accuracy<={accuracy2}) OR (dl_accuracy>{accuracy1} AND dl_accuracy<={accuracy2})) '''+s1+s2+f''' ORDER BY attack_epoch_time DESC limit 200000;'''
    
    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)
    
    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [item['name'] for item in run_sql.get('schema')]
        
        table_query_list = []
        for i, row in enumerate(run_sql.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
            
        return Response({"message_type":"success", "count":len(table_query_list), "city_name":city_name,"table":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 29.a ML DL-Card Name: Target IP (Pie chart on target_ip column)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_ml_target_ip_pie(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    platform_tuple = detail_dict.get("platform_tuple")
    platform_query = f"AND platform IN {platform_tuple} " if platform_tuple is not None else ""

    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    accuracy_val = detail_dict.get("accuracy_val")
    accuracy1, accuracy2 = getMlDlAccuracyRanges(accuracy_val)
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    sql = f"SELECT target_ip, COUNT(target_ip) FROM {indice_name}-* WHERE (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NULL and ((ml_accuracy>{accuracy1} AND ml_accuracy<={accuracy2}) OR (dl_accuracy>{accuracy1} AND dl_accuracy<={accuracy2})) "+platform_query+s1+s2+f" GROUP BY target_ip ORDER BY COUNT(target_ip) desc LIMIT 7;"
    
    run_sql_query = opensearch_conn_using_db(sql, location_id, plan_id)
    
    if run_sql_query.get("total") not in exclude_values:
        target_ip, target_ip_count = map(list, zip(*run_sql_query['datarows']))

        bar_chart_dict = {"series": target_ip_count, "labels": target_ip}
        
        
        col_val = str(target_ip).strip("[]")
        target_ip_tuple = "(" + col_val + ")"
    
        # for grouping according to platform
        sql2 = f"SELECT platform, target_ip, count(target_ip) target_ip_count FROM {indice_name}-* WHERE (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) and ((ml_accuracy>{accuracy1} AND ml_accuracy<={accuracy2}) OR (dl_accuracy>{accuracy1} AND dl_accuracy<={accuracy2})) "+platform_query+s1+s2+f" AND target_ip IN {target_ip_tuple} AND platform IS NOT NULL AND ids_threat_class IS NULL GROUP BY platform, target_ip ORDER BY target_ip_count desc;"
        
        run_sql2 = opensearch_conn_using_db(sql2, location_id, plan_id)

        if run_sql2.get("total") not in [0, None]:
            # formatting sql2 query output as (key, value) pairs in dictionary

            key_names = []
            for i,n in enumerate(run_sql2.get('schema')):
                if n.get('name') == 'count(target_ip)':
                    key_names.append(n.get('alias'))
                else:
                    key_names.append(n.get('name'))
            
            table_query_list = []
            for i, key_values in enumerate(run_sql2.get('datarows')):
                Dict = {}
                Dict.update(dict(zip(key_names, key_values)))
                Dict["past_time"] = past_time
                Dict["current_time"] = current_time

                table_query_list.append(Dict)
        else:
            return Response({"message_type":"d_not_f"})
        
        return Response({"message_type":"success", "bar_chart":bar_chart_dict, "filter":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 29.b ML DL-Pie chart on target_ip column--Table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_ml_target_ip_table(request):
    target_ip = request.GET.get('target_ip')
    if target_ip is None:
        return Response({"message_type": "d_not_f", "errors": "target_ip_not_found"})
    
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    accuracy_val = detail_dict.get("accuracy_val")
    accuracy1, accuracy2 = getMlDlAccuracyRanges(accuracy_val)
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    platform_name = request.GET.get('platform')

    if platform_name is None:
        return Response({"message_type": "d_not_f","errors": "platform_name_not_found"})
    
    if past_time is None:
        return Response({"message_type": "d_not_f","errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f","errors": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT platform, type_of_threat, attacker_ip, attacker_mac, attack_timestamp, ids_threat_class, ids_threat_type, ml_threat_class, dl_threat_class, ml_accuracy, dl_accuracy, attacker_port, target_port, target_ip, geoip_city, geoip_country_name, geoip_asn_name FROM {indice_name}-* WHERE target_ip = '{target_ip}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform = '{platform_name}' AND ids_threat_class IS NULL and ((ml_accuracy>{accuracy1} AND ml_accuracy<={accuracy2}) OR (dl_accuracy>{accuracy1} AND dl_accuracy<={accuracy2})) "+s1+s2+f" ORDER BY attack_epoch_time DESC limit 200000;"
    
    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)
    
    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [item['name'] for item in run_sql.get('schema')]
        
        table_query_list = []
        for i, row in enumerate(run_sql.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
            
        return Response({"message_type":"success", "count":len(table_query_list), "target_ip":target_ip,"table":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 30.a ML DL- Card Name: Target MAC (Pie chart on target_mac column)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_ml_target_mac_pie_chart(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id
    
    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    platform_tuple = detail_dict.get("platform_tuple")
    platform_query = f"AND platform IN {platform_tuple} " if platform_tuple is not None else ""

    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    accuracy_val = detail_dict.get("accuracy_val")
    accuracy1, accuracy2 = getMlDlAccuracyRanges(accuracy_val)
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    sql = f"SELECT target_mac, COUNT(target_mac) FROM {indice_name}-* WHERE (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NULL AND target_mac IS NOT NULL and ((ml_accuracy>{accuracy1} AND ml_accuracy<={accuracy2}) OR (dl_accuracy>{accuracy1} AND dl_accuracy<={accuracy2})) "+platform_query+s1+s2+f" GROUP BY target_mac ORDER BY COUNT(target_mac) desc LIMIT 7;"
    
    run_sql_query = opensearch_conn_using_db(sql, location_id, plan_id)
    
    if run_sql_query.get("total") not in exclude_values:
        target_mac, target_mac_count = map(list, zip(*run_sql_query['datarows']))
        bar_chart_dict = {"series": target_mac_count, "labels": target_mac}
        
        
        col_val = str(target_mac).strip("[]")
        target_mac_tuple = "(" + col_val + ")"
    
        # for grouping according to platform
        sql2 = f"SELECT platform, target_mac, count(target_mac) target_mac_count FROM {indice_name}-* WHERE (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) and ((ml_accuracy>{accuracy1} AND ml_accuracy<={accuracy2}) OR (dl_accuracy>{accuracy1} AND dl_accuracy<={accuracy2})) "+platform_query+s1+s2+f" AND target_mac IN {target_mac_tuple} AND platform IS NOT NULL AND ids_threat_class IS NULL GROUP BY platform, target_mac ORDER BY target_mac_count desc;"
        
        run_sql2 = opensearch_conn_using_db(sql2, location_id, plan_id)

        if run_sql2.get("total") not in [0, None]:
            # formatting sql2 query output as (key, value) pairs in dictionary

            key_names = []
            for i,n in enumerate(run_sql2.get('schema')):
                if n.get('name') == 'count(target_mac)':
                    key_names.append(n.get('alias'))
                else:
                    key_names.append(n.get('name'))
            
            table_query_list = []
            for i, key_values in enumerate(run_sql2.get('datarows')):
                Dict = {}
                Dict.update(dict(zip(key_names, key_values)))
                Dict["past_time"] = past_time
                Dict["current_time"] = current_time

                table_query_list.append(Dict)
        else:
            return Response({"message_type":"d_not_f"})
        
        return Response({"message_type":"success", "bar_chart":bar_chart_dict, "filter":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 30.b ML DL-Pie chart on target_mac column--Table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_ml_target_mac_table(request):
    target_mac = request.GET.get('target_mac')
    if target_mac is None:
        return Response({"message_type": "d_not_f", "errors": "target_mac_not_found"})
    
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id
    
    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    accuracy_val = detail_dict.get("accuracy_val")
    accuracy1, accuracy2 = getMlDlAccuracyRanges(accuracy_val)
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    platform_name = request.GET.get('platform')

    if platform_name is None:
        return Response({"message_type": "d_not_f","errors": "platform_name_not_found"})
    
    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT platform, type_of_threat, attacker_ip, attacker_mac, attack_timestamp, ids_threat_class, ids_threat_type, ml_threat_class, dl_threat_class, ml_accuracy, dl_accuracy, attacker_port, target_port, target_ip, geoip_city, geoip_country_name, geoip_asn_name FROM {indice_name}-* WHERE target_mac = '{target_mac}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform = '{platform_name}' AND ids_threat_class IS NULL and ((ml_accuracy>{accuracy1} AND ml_accuracy<={accuracy2}) OR (dl_accuracy>{accuracy1} AND dl_accuracy<={accuracy2})) "+s1+s2+f" ORDER BY attack_epoch_time DESC limit 200000;"
    
    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)
    
    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [item['name'] for item in run_sql.get('schema')]
        
        table_query_list = []
        for i, row in enumerate(run_sql.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
            
        return Response({"message_type":"success", "count":len(table_query_list), "target_mac":target_mac,"table":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 31.a ML DL- Card Name: Target Port (Pie chart on target_port column)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_ml_target_port_pie(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id
    
    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    platform_tuple = detail_dict.get("platform_tuple")
    platform_query = f"AND platform IN {platform_tuple} " if platform_tuple is not None else ""

    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    accuracy_val = detail_dict.get("accuracy_val")
    accuracy1, accuracy2 = getMlDlAccuracyRanges(accuracy_val)
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    sql = f"SELECT target_port, COUNT(target_port) FROM {indice_name}-* WHERE (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NULL AND target_port IS NOT NULL and ((ml_accuracy>{accuracy1} AND ml_accuracy<={accuracy2}) OR (dl_accuracy>{accuracy1} AND dl_accuracy<={accuracy2})) "+platform_query+s1+s2+f" GROUP BY target_port ORDER BY COUNT(target_port) desc LIMIT 7;"
    
    run_sql_query = opensearch_conn_using_db(sql, location_id, plan_id)
    
    if run_sql_query.get("total") not in exclude_values:
        target_port, target_port_count = map(list, zip(*run_sql_query['datarows']))
        bar_chart_dict = {"series": target_port_count, "labels": target_port}

        col_val = str(target_port).strip("[]")
        target_port_tuple = "(" + col_val + ")"
    
        # for grouping according to platform
        sql2 = f"SELECT platform, target_port, count(target_port) target_port_count FROM {indice_name}-* WHERE (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NULL and ((ml_accuracy>{accuracy1} AND ml_accuracy<={accuracy2}) OR (dl_accuracy>{accuracy1} AND dl_accuracy<={accuracy2})) "+platform_query+s1+s2+f" AND target_port IN {target_port_tuple} AND platform IS NOT NULL GROUP BY platform, target_port ORDER BY target_port_count desc;"
        
        run_sql2 = opensearch_conn_using_db(sql2, location_id, plan_id)

        if run_sql2.get("total") not in [0, None]:
            # formatting sql2 query output as (key, value) pairs in dictionary

            key_names = []
            for i,n in enumerate(run_sql2.get('schema')):
                if n.get('name') == 'count(target_port)':
                    key_names.append(n.get('alias'))
                else:
                    key_names.append(n.get('name'))
            
            table_query_list = []
            for i, key_values in enumerate(run_sql2.get('datarows')):
                Dict = {}
                Dict.update(dict(zip(key_names, key_values)))
                Dict["past_time"] = past_time
                Dict["current_time"] = current_time

                table_query_list.append(Dict)
        else:
            return Response({"message_type":"d_not_f"})
        
        return Response({"message_type":"success", "bar_chart":bar_chart_dict, "filter":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 31.b ML DL-Pie chart on target_port column--Table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_ml_target_port_table(request):
    target_port = request.GET.get('target_port')
    if target_port is None:
        return Response({"message_type": "target_port_not_found"})
    
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id
    
    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    accuracy_val = detail_dict.get("accuracy_val")
    accuracy1, accuracy2 = getMlDlAccuracyRanges(accuracy_val)
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    platform_name = request.GET.get('platform')

    if platform_name is None:
        return Response({"message_type": "d_not_f","errors": "platform_name_not_found"})
    
    if past_time is None:
        return Response({"message_type": "d_not_f","errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f","errors": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT platform, type_of_threat, attacker_ip, attacker_mac, attack_timestamp, ids_threat_class, ids_threat_type, ml_threat_class, dl_threat_class, ml_accuracy, dl_accuracy, attacker_port, target_port, target_ip, geoip_city, geoip_country_name, geoip_asn_name FROM {indice_name}-* WHERE target_port = {target_port} AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform = '{platform_name}' AND ids_threat_class IS NULL and ((ml_accuracy>{accuracy1} AND ml_accuracy<={accuracy2}) OR (dl_accuracy>{accuracy1} AND dl_accuracy<={accuracy2})) "+s1+s2+f" ORDER BY attack_epoch_time DESC limit 200000;"
    
    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)
    
    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [item['name'] for item in run_sql.get('schema')]
        
        table_query_list = []
        for i, row in enumerate(run_sql.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
            
        return Response({"message_type":"success", "count":len(table_query_list), "target_port":target_port,"table":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 32 ML DL-Card Name: Target Frequency Host --only table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_ml_freq_trgted_host(request):
    condition = request.GET.get('condition')
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "invalid_condition"})
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id
    
    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    platform_tuple = detail_dict.get("platform_tuple")
    platform_query = f"AND platform IN {platform_tuple} " if platform_tuple is not None else ""
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    accuracy_val = detail_dict.get("accuracy_val")
    accuracy1, accuracy2 = getMlDlAccuracyRanges(accuracy_val)
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    sql_query = f"SELECT target_ip,target_mac,type_of_threat, count(target_ip) target_ip_count FROM {indice_name}-* WHERE target_ip IS NOT NULL AND type_of_threat IS NOT NULL "+platform_query+s1+s2+f" AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} AND ids_threat_class IS NULL and ((ml_accuracy>{accuracy1} AND ml_accuracy<={accuracy2}) OR (dl_accuracy>{accuracy1} AND dl_accuracy<={accuracy2})) GROUP BY target_ip,target_mac,type_of_threat ORDER BY target_ip_count DESC LIMIT 50;"
    
    api_response = opensearch_conn_using_db(sql_query, location_id, plan_id)
    
    if api_response.get("total") not in exclude_values:
        key_names = [item['alias'] if (item['name'] == "count(target_ip)") else item['name'] for item in api_response.get('schema')]
        
        final_response = []
        for i in range(len(api_response.get('datarows'))):
            row = api_response.get('datarows')[i]
            final_response.append(dict(zip(key_names, row)))
        
        return Response({"message_type":"success", "data":final_response})
    else:
        return Response({"message_type":"d_not_f"})

# 33 ML DL- Card Name: Attack Frequency --only table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_ml_freq_attacker(request):
    condition = request.GET.get('condition')
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id
    
    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    platform_tuple = detail_dict.get("platform_tuple")
    platform_query = f"AND platform IN {platform_tuple}" if platform_tuple is not None else ""
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    accuracy_val = detail_dict.get("accuracy_val")
    accuracy1, accuracy2 = getMlDlAccuracyRanges(accuracy_val)
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    sql_query = f"SELECT attacker_ip,target_mac,type_of_threat, count(attacker_ip) attacker_ip_count FROM {indice_name}-* WHERE attacker_ip IS NOT NULL AND type_of_threat IS NOT NULL "+platform_query+s1+s2+f" AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} AND ids_threat_class IS NULL and ((ml_accuracy>{accuracy1} AND ml_accuracy<={accuracy2}) OR (dl_accuracy>{accuracy1} AND dl_accuracy<={accuracy2})) GROUP BY attacker_ip,target_mac,type_of_threat ORDER BY attacker_ip_count DESC LIMIT 50;"
    
    api_response = opensearch_conn_using_db(sql_query, location_id, plan_id)
    
    if api_response.get("total") not in exclude_values:
        key_names = [item['alias'] if (item['name'] == "count(attacker_ip)") else item['name'] for item in api_response.get('schema')]
        
        final_response = []
        for i in range(len(api_response.get('datarows'))):
            row = api_response.get('datarows')[i]
            final_response.append(dict(zip(key_names, row)))
        
        return Response({"message_type":"success", "data":final_response})
    else:
        return Response({"message_type":"d_not_f"})

# 34 ML DL- Card Name: Top Attacked Services --only table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_ml_attacked_service_details(request):
    condition = request.GET.get('condition')
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id
    
    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    platform_tuple = detail_dict.get("platform_tuple")
    platform_query = f"AND platform IN {platform_tuple} " if platform_tuple is not None else ""

    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    accuracy_val = detail_dict.get("accuracy_val")
    accuracy1, accuracy2 = getMlDlAccuracyRanges(accuracy_val)
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""

    sql_query = f"SELECT attacker_ip, service_name, count(*) service_name_count FROM {indice_name}-* WHERE attacker_ip IS NOT NULL AND service_name NOT LIKE 'NA' AND type_of_threat IS NOT NULL "+platform_query+s1+s2+f" AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} AND ids_threat_class IS NULL and ((ml_accuracy>{accuracy1} AND ml_accuracy<={accuracy2}) OR (dl_accuracy>{accuracy1} AND dl_accuracy<={accuracy2})) GROUP BY attacker_ip,service_name ORDER BY service_name_count DESC LIMIT 50;"
    
    api_response = opensearch_conn_using_db(sql_query, location_id, plan_id)
    
    if api_response.get("total") not in exclude_values:
        key_names = [item['alias'] if (item['name'] == "count(*)") else item['name'] for item in api_response.get('schema')]
        
        final_response = []
        for i in range(len(api_response.get('datarows'))):
            row = api_response.get('datarows')[i]
            final_response.append(dict(zip(key_names, row)))
        
        return Response({"message_type":"success", "data":final_response})
    else:
        return Response({"message_type":"d_not_f"})

# 35 IDS----Card Name: Type of Threat (threat_type count in series, labels)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nids_alert_threat_type_ser_label(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id
    
    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    platform_tuple = detail_dict.get("platform_tuple")
    platform_query = f"AND platform IN {platform_tuple}" if platform_tuple is not None else ""

    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    threat_class_tuple = ('Lateral Movement','External Attack','Attack on External Server','Internal Compromised Machine')
    
    sql_query = f"SELECT type_of_threat, attack_epoch_time FROM {indice_name}-* WHERE type_of_threat IN {threat_class_tuple} "+platform_query+s1+s2+f" AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL ORDER BY attack_epoch_time DESC limit 200000;"
    
    search2 = opensearch_conn_using_db(sql_query, location_id, plan_id)
    
    if search2.get("total") not in exclude_values:

    # formatting sql_query query output as (key, value) pairs in dictionary
        key_names = [item['name'] for item in search2.get('schema')]
        
        table_query_list = []
        for i, row in enumerate(search2.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
        
        series_list = []
        for threat in ('Lateral Movement','Internal Compromised Machine'):
            filtered_dict = [dictionary for dictionary in table_query_list if dictionary.get('type_of_threat') == threat]
            series_list.append(len(filtered_dict))
        
        filtered_dict = [dictionary for dictionary in table_query_list if dictionary.get('type_of_threat') == 'External Attack' or dictionary.get('type_of_threat') == 'Attack on External Server']
        series_list.append(len(filtered_dict))

        response_dict = {"message_type":"success","data":{"total":sum(series_list), "series":series_list, "labels":["Lateral Movement", "Internal Compromised Machine", "External Attack"]}}
            
        return Response(response_dict)
    else:
        return Response({"message_type":"d_not_f"})

# encryption: Pie chart on attacker_port column
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def attacker_port_pie_chart_encrypt(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id
    
    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    sql = f"SELECT attacker_port, COUNT(attacker_port) FROM {indice_name}-* WHERE attacker_port IS NOT NULL AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL AND attacker_port IS NOT NULL"+s1+s2+f" GROUP BY attacker_port ORDER BY COUNT(attacker_port) desc LIMIT 7;"
    
    run_sql_query = opensearch_conn_using_db(sql, location_id, plan_id)
    
    if run_sql_query.get("total") not in exclude_values:
        type_of_threat, threat_count = map(list, zip(*run_sql_query['datarows']))
        bar_chart_dict = {"series": threat_count, "labels": type_of_threat}
        
        time_dict = {"past_time":past_time, "current_time":current_time}
        encrypted_bar_chart_dict = encrypt(json.dumps(bar_chart_dict))
        encrypted_time_dict = encrypt(json.dumps(time_dict))

        return Response({"message_type":"success", "bar_chart":encrypted_bar_chart_dict, "filter":encrypted_time_dict})
    else:
        return Response({"message_type":"d_not_f"})

# encryption: Bar chart on attacker_port column--Table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def attacker_port_pie_table_encrypt(request):
    attacker_port = request.GET.get('name')
    if attacker_port is None:
        return Response({"message_type": "d_not_f", "errors": "name_not_found"})
    
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id
    
    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('nids_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ml_threat_class NOT IN {blacklisted_class_tuple} AND dl_threat_class NOT IN {blacklisted_class_tuple} AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
    s2 = f"AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    
    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT platform, type_of_threat, attacker_ip, attacker_mac, attack_timestamp, ids_threat_class, ids_threat_type, ml_threat_class, dl_threat_class, ml_accuracy, dl_accuracy, attacker_port, target_port, target_ip, geoip_city, geoip_country_name, geoip_asn_name FROM {indice_name}-* WHERE attacker_port = {attacker_port} AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL "+s1+s2+f" ORDER BY attack_epoch_time DESC limit 200000;"
    
    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)
    
    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [item['name'] for item in run_sql.get('schema')]
        
        table_query_list = []
        for i, row in enumerate(run_sql.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
        
        encrypted_count = encrypt(json.dumps(len(table_query_list)))
        encrypted_attacker_port = encrypt(json.dumps(attacker_port))
        encrypted_table = encrypt(json.dumps(table_query_list))
            
        return Response({"message_type":"success", "count":encrypted_count, "attacker_port":encrypted_attacker_port,"table":encrypted_table})
    else:
        return Response({"message_type":"d_not_f"})