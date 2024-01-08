#  ==============================================================================================================================
#  File Name: trace_alert.py
#  Description: It contains all the code for each chart on Trace Alerts page under Trace tab on Client Dashboard.
#  Active URL: https://xdr-demo.zerohack.in/trace/alerts

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
from django.views.decorators.cache import never_cache

# list containing values to exclude from each query--> to avoid error on frontend page
exclude_values = [0,None]

#1.a Card Name: Critical Threats
@never_cache
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trace_alert_critical_threats(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('trace_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type": "d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ids_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f" AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    threat_class_tuple = ('Lateral Movement','External Attack','Attack on External Server','Internal Compromised Machine')
    
    sql_query = f"SELECT type_of_threat, attack_epoch_time FROM {indice_name}-* WHERE type_of_threat IN {threat_class_tuple} "+s1+s2+f" AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL ORDER BY attack_epoch_time DESC limit 200000;"
    
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
        # filter_list = []
        
        response_dict["message_type"] = "success"
        response_dict["total"] = len(table_query_list)
        
        for threat in ('Lateral Movement','Internal Compromised Machine'):
            filtered_dict = [dictionary for dictionary in table_query_list if dictionary.get('type_of_threat') == threat]
            # threat_dict = {
            #     "threat_name": threat,
            #     "threat_count": len(filtered_dict),
            #     "past_time": past_time,
            #     "current_time": current_time
            # }
            # filter_list.append(threat_dict)
            
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
        
        # response_dict["filter"]= []
        # response_dict["filter"]= filter_list
        # ext_threat_dict ={
        #         "threat_name": 'External Attack',
        #         "threat_count": len(filtered_dict),
        #         "past_time": past_time,
        #         "current_time": current_time
        #     }
        # response_dict["filter"].append(ext_threat_dict)

        # for grouping according to sensor_name
        sql2 = f"SELECT sensor_name, type_of_threat, count(type_of_threat) threat_count FROM {indice_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} "+s1+s2+f" AND type_of_threat IN {threat_class_tuple} AND sensor_name IS NOT NULL AND ids_threat_class IS NOT NULL GROUP BY sensor_name, type_of_threat ORDER BY threat_count desc;"
    
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
@never_cache
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trace_alert_critical_threats_table(request):
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('trace_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type": "d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ids_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f" AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    type_of_threat = request.GET.get('name')
    sensor_name = request.GET.get('name1')

    if sensor_name is None:
        return Response({"message_type": "d_not_f", "errors": "sensor_name_not_found"})
    
    if type_of_threat == 'External Attack':
        threat_class_tuple = ('External Attack','Attack on External Server')
    else:
        threat_class_tuple = f"('{type_of_threat}')"
    
    if type_of_threat is None:
        return Response({"message_type": "d_not_f", "errors": "name_not_found"})
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    
    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT attack_timestamp,sensor_name,type_of_threat,ids_threat_class,ids_threat_type,tag,attacker_ip,attacker_host_type,attacker_port,ip_rep,target_ip,target_port,service_name,http_url,geoip_country_name,geoip_city,geoip_asn_name,geoip_latitude,geoip_longitude,attack_epoch_time,anomaly_event,anomaly_app_proto FROM {indice_name}-* WHERE type_of_threat IN {threat_class_tuple} AND sensor_name = '{sensor_name}' "+s1+s2+f" AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL ORDER BY attack_epoch_time DESC limit 200000;"
    
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
@never_cache
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trace_alert_lateral_mov(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('trace_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ids_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f" AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    sql_query = f"SELECT type_of_threat, attack_epoch_time FROM {indice_name}-* WHERE type_of_threat = 'Lateral Movement' "+s1+s2+f" AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL ORDER BY attack_epoch_time DESC limit 200000;"
    
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
                response_dict["lateral_movement"]
        else:
            for item in table_query_list:
                epoch_date = item["attack_epoch_time"]
                for i, (start, end) in enumerate(epoch_interval_group_list):
                    if start <= epoch_date <= end:
                        response_dict["lateral_movement"][i] += 1
    
    # for grouping according to sensor_name
    sql2 = f"SELECT sensor_name, type_of_threat, count(type_of_threat) threat_count FROM {indice_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} "+s1+s2+f" AND type_of_threat = 'Lateral Movement' AND sensor_name IS NOT NULL AND ids_threat_class IS NOT NULL GROUP BY sensor_name, type_of_threat ORDER BY threat_count desc;"
    
    run_sql2 = opensearch_conn_using_db(sql2, location_id, plan_id)

    if run_sql2.get("total") not in [0, None]:
        # formatting sql2 query output as (key, value) pairs in dictionary

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
    
        response_dict["filter"]= table_query_list
            
        return Response(response_dict)
    else:
        return Response({"message_type":"d_not_f"})

#2.b Lateral Movement table
@never_cache
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trace_alert_lateral_mov_table(request):
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('trace_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type": "d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ids_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f" AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    sensor_name = request.GET.get('name')
    
    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})
    
    if sensor_name is None:
        return Response({"message_type": "d_not_f", "errors": "sensor_name_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT attack_timestamp,sensor_name,type_of_threat,ids_threat_class,ids_threat_type,tag,attacker_ip,attacker_host_type,attacker_port,ip_rep,target_ip,target_port,service_name,http_url,geoip_country_name,geoip_city,geoip_asn_name,geoip_latitude,geoip_longitude,attack_epoch_time,anomaly_event,anomaly_app_proto FROM {indice_name}-* WHERE type_of_threat = 'Lateral Movement' AND sensor_name = '{sensor_name}' "+s1+s2+f" AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL ORDER BY attack_epoch_time DESC limit 200000;"
    
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
@never_cache
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trace_alert_int_compr(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('trace_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ids_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f" AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    sql_query = f"SELECT type_of_threat, attack_epoch_time FROM {indice_name}-* WHERE type_of_threat = 'Internal Compromised Machine' "+s1+s2+f" AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL ORDER BY attack_epoch_time DESC limit 200000;"
    
    sql_search = opensearch_conn_using_db(sql_query, location_id, plan_id)
    
    if sql_search.get("total") not in exclude_values:
    # formatting sql_query query output as (key, value) pairs in dictionary
        key_names = [item['name'] for item in sql_search.get('schema')]
        
        table_query_list = []
        for i, row in enumerate(sql_search.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
        
        # to create series
        epoch_interval_group_list = getEpochIntervalGroupList(condition, past_time, current_time)

        if epoch_interval_group_list is None:
            return Response({"message_type": "d_not_f", "errors": "condition_not_f"})
        
        # Create a dictionary with default values of 0 for time interval counts
        response_dict = defaultdict(lambda: [0] * len(epoch_interval_group_list))
        filter_list = []
        
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
        
        threat_dict = {
                "threat_name": "internal_compromised_machine",
                "threat_count": len(table_query_list),
                "past_time": past_time,
                "current_time": current_time
            }
        filter_list.append(threat_dict)
        response_dict["filter"]= filter_list

    # for grouping according to sensor_name
    sql2 = f"SELECT sensor_name, type_of_threat, count(type_of_threat) threat_count FROM {indice_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} "+s1+s2+f" AND type_of_threat = 'Internal Compromised Machine' AND sensor_name IS NOT NULL AND ids_threat_class IS NOT NULL GROUP BY sensor_name, type_of_threat ORDER BY threat_count desc;"
    
    run_sql2 = opensearch_conn_using_db(sql2, location_id, plan_id)

    if run_sql2.get("total") not in [0, None]:
        # formatting sql2 query output as (key, value) pairs in dictionary

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
    
        response_dict["filter"]= table_query_list
            
        return Response(response_dict)
    else:
        return Response({"message_type":"d_not_f"})

#3.b Internal Compromised Machine Table
@never_cache
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trace_alert_int_compr_table(request):
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('trace_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ids_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f" AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    sensor_name = request.GET.get('name')
    
    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})
    
    if sensor_name is None:
        return Response({"message_type": "d_not_f", "errors": "sensor_name_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT attack_timestamp,sensor_name,type_of_threat,ids_threat_class,ids_threat_type,tag,attacker_ip,attacker_host_type,attacker_port,ip_rep,target_ip,target_port,service_name,http_url,geoip_country_name,geoip_city,geoip_asn_name,geoip_latitude,geoip_longitude,attack_epoch_time,anomaly_event,anomaly_app_proto FROM {indice_name}-* WHERE type_of_threat = 'Internal Compromised Machine' AND sensor_name = '{sensor_name}' "+s1+s2+f" AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL ORDER BY attack_epoch_time DESC limit 200000;"
    
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
def trace_alert_ext(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('trace_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ids_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f" AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    threat_class_tuple = ('External Attack','Attack on External Server')
    
    sql_query = f"SELECT type_of_threat, attack_epoch_time FROM {indice_name}-* WHERE type_of_threat IN {threat_class_tuple} "+s1+s2+f" AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL ORDER BY attack_epoch_time DESC limit 200000;"
    
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
        
    # for grouping according to sensor_name
    sql2 = f"SELECT sensor_name, type_of_threat, count(type_of_threat) threat_count FROM {indice_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} "+s1+s2+f" AND type_of_threat IN {threat_class_tuple} AND sensor_name IS NOT NULL AND ids_threat_class IS NOT NULL GROUP BY sensor_name, type_of_threat ORDER BY threat_count desc;"
    
    run_sql2 = opensearch_conn_using_db(sql2, location_id, plan_id)

    if run_sql2.get("total") not in [0, None]:
        # formatting sql2 query output as (key, value) pairs in dictionary

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
    
        response_dict["filter"]= table_query_list
            
        return Response(response_dict)
    else:
        return Response({"message_type":"d_not_f"})

#4.b External Attack Table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trace_alert_ext_table(request):
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('trace_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ids_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f" AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    sensor_name = request.GET.get('name')

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})
    
    if sensor_name is None:
        return Response({"message_type": "d_not_f", "errors": "sensor_name_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT attack_timestamp,sensor_name,type_of_threat,ids_threat_class,ids_threat_type,tag,attacker_ip,attacker_host_type,attacker_port,ip_rep,target_ip,target_port,service_name,http_url,geoip_country_name,geoip_city,geoip_asn_name,geoip_latitude,geoip_longitude,attack_epoch_time,anomaly_event,anomaly_app_proto FROM {indice_name}-* WHERE type_of_threat IN ('External Attack','Attack on External Server') AND sensor_name = '{sensor_name}' "+s1+s2+f" AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL ORDER BY attack_epoch_time DESC limit 200000;"
    
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

# 5.a. Card Name: Attacker Geo-Locations
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trace_alert_geolocation(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('trace_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ids_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f" AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})

    sql = f"SELECT geoip_city, geoip_latitude,geoip_longitude, count(*) count FROM {indice_name}-* WHERE geoip_country_name IS NOT NULL AND geoip_latitude IS NOT NULL AND geoip_longitude IS NOT NULL AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL "+s1+s2+f" GROUP BY geoip_city,geoip_latitude,geoip_longitude ORDER BY count desc LIMIT 20;"
    
    run_sql = opensearch_conn_using_db(sql, location_id, plan_id)
    
    map_value = []
    if run_sql.get("total") not in exclude_values:
        geoip_city, geoip_latitude, geoip_longitude, attack_count = map(list, zip(*run_sql['datarows']))
        latandlon = zip(geoip_longitude, geoip_latitude)
        for (m, n) in zip(latandlon, geoip_city):
            map_value.append({"position": m, "title": n})
        
        col_val = str(geoip_city).strip("[]")
        geoip_city_tuple = "(" + col_val + ")"
    
        # for grouping according to sensor_name
        sql2 = f"SELECT sensor_name, geoip_city, count(geoip_city) geoip_city_count FROM {indice_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} "+s1+s2+f" AND geoip_city IN {geoip_city_tuple} AND sensor_name IS NOT NULL AND ids_threat_class IS NOT NULL GROUP BY sensor_name, geoip_city ORDER BY geoip_city_count desc;"
        
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
            return Response({"message_type": "d_not_f"})
        
        return Response({"message_type":"success", "geolocation":map_value, "filter":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})


# 5.b. geolocation Table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trace_alert_geolocation_table(request):
    city_name = request.GET.get('name')
    if city_name is None:
        return Response({"message_type": "d_not_f", "errors": "name_not_found"})
    
    sensor_name = request.GET.get('name1')
    if sensor_name is None:
        return Response({"message_type": "d_not_f", "errors": "sensor_name_not_found"})
    
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('trace_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ids_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f" AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    
    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT attack_timestamp,sensor_name,type_of_threat,ids_threat_class,ids_threat_type,tag,attacker_ip,attacker_host_type,attacker_port,ip_rep,target_ip,target_port,service_name,http_url,geoip_country_name,geoip_city,geoip_asn_name,geoip_latitude,geoip_longitude,attack_epoch_time,anomaly_event,anomaly_app_proto FROM {indice_name}-* WHERE geoip_city = '{city_name}' AND sensor_name = '{sensor_name}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL "+s1+s2+f" ORDER BY attack_epoch_time DESC limit 200000;"
      
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

# 6 IDS----Card Name: Type of Threat (threat_type count in series, labels)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trace_alert_threat_type_count(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('trace_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ids_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f" AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    threat_class_tuple = ('Lateral Movement','External Attack','Attack on External Server','Internal Compromised Machine')
    
    sql_query = f"SELECT type_of_threat, attack_epoch_time FROM {indice_name}-* WHERE type_of_threat IN {threat_class_tuple} "+s1+s2+f" AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL ORDER BY attack_epoch_time DESC limit 200000;"
    
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

# 7.a Card Name: Attacker Port (Pie chart on attacker_port column)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trace_alert_attacker_port_pie_chart(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('trace_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ids_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f" AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    sql = f"SELECT attacker_port, COUNT(attacker_port) FROM {indice_name}-* WHERE attacker_port IS NOT NULL AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL "+s1+s2+f" GROUP BY attacker_port ORDER BY COUNT(attacker_port) desc LIMIT 7;"
    
    run_sql_query = opensearch_conn_using_db(sql, location_id, plan_id)
    
    if run_sql_query.get("total") not in exclude_values:
        attacker_port, threat_count = map(list, zip(*run_sql_query['datarows']))
        bar_chart_dict = {"series": threat_count, "labels": attacker_port}

        col_val = str(attacker_port).strip("[]")
        attacker_port_tuple = "(" + col_val + ")"
    
        # for grouping according to sensor_name
        sql2 = f"SELECT sensor_name, attacker_port, count(attacker_port) attacker_port_count FROM {indice_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} "+s1+s2+f" AND attacker_port IN {attacker_port_tuple} AND sensor_name IS NOT NULL AND ids_threat_class IS NOT NULL GROUP BY sensor_name, attacker_port ORDER BY attacker_port_count desc;"
        
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
            return Response({"message_type": "d_not_f"})

        return Response({"message_type":"success", "bar_chart":bar_chart_dict, "filter":table_query_list})
    else:
        return Response({"message_type": "d_not_f"})

# 7.b Bar chart on attacker_port column--Table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trace_alert_attacker_port_pie_table(request):
    attacker_port = request.GET.get('name')
    sensor_name = request.GET.get('name1')

    if attacker_port is None:
        return Response({"message_type": "d_not_f", "errors": "name_not_found"})
    
    if sensor_name is None:
        return Response({"message_type": "d_not_f", "errors": "sensor_name_not_found"})
    
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('trace_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ids_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f" AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    
    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT attack_timestamp,sensor_name,type_of_threat,ids_threat_class,ids_threat_type,tag,attacker_ip,attacker_host_type,attacker_port,ip_rep,target_ip,target_port,service_name,http_url,geoip_country_name,geoip_city,geoip_asn_name,geoip_latitude,geoip_longitude,attack_epoch_time,anomaly_event,anomaly_app_proto FROM {indice_name}-* WHERE attacker_port = {attacker_port} AND sensor_name = '{sensor_name}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL "+s1+s2+f" ORDER BY attack_epoch_time DESC limit 200000;"
    
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

#8.a Card Name: Source IPs (Attacker IPs Line chart)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trace_alert_attacker_ip_line_chart(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('trace_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ids_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f" AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)
    
    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    sql1 = f"SELECT attacker_ip,count(attacker_ip) count FROM {indice_name}-* WHERE attacker_ip IS NOT NULL AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL "+s1+s2+f" GROUP BY attacker_ip ORDER BY count desc LIMIT 7;"  
    
    search1 = opensearch_conn_using_db(sql1, location_id, plan_id)
    
    if search1.get("total") not in exclude_values:
        unique_IP, unique_IP_count = map(list, zip(*search1['datarows']))
        attacker_ip_tuple = tuple(unique_IP)
        updated_tuple = attacker_ip_tuple
        if len(attacker_ip_tuple) == 1:
            updated_tuple = attacker_ip_tuple+('0',)
    else:
        return Response({"message_type": "d_not_f"})

    # date wise count of a single attacker_ip
    sql2 = f"SELECT attacker_ip, attack_epoch_time FROM {indice_name}-* WHERE attacker_ip IN {updated_tuple} AND attacker_ip IS NOT NULL AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL "+s1+s2+f" ORDER BY attack_epoch_time limit 200000;"
    
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
        return Response({"message_type": "d_not_f"})
    
    # for grouping according to sensor_name
    sql3 = f"SELECT sensor_name, attacker_ip, count(attacker_ip) attacker_ip_count FROM {indice_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} "+s1+s2+f" AND attacker_ip IN {updated_tuple} AND sensor_name IS NOT NULL AND ids_threat_class IS NOT NULL GROUP BY sensor_name, attacker_ip ORDER BY attacker_ip_count desc;"
    
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
        
        return Response({"message_type": "success","line_chart":line_chart, "filter":table_query_list})
    else:
        return Response({"message_type": "d_not_f"})


#8.b. Source IPs Table 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trace_alert_line_table(request):
    attacker_ip = request.GET.get('name')
    sensor_name = request.GET.get('name1')

    if attacker_ip is None:
        return Response({"message_type":"d_not_f", "errors": "name_not_found"})
    
    if sensor_name is None:
        return Response({"message_type": "d_not_f", "errors": "sensor_name_not_found"})
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    
    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})
    
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('trace_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ids_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f" AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""

    # sql query to get table data
    table_query = f"SELECT attack_timestamp,sensor_name,type_of_threat,ids_threat_class,ids_threat_type,tag,attacker_ip,attacker_host_type,attacker_port,ip_rep,target_ip,target_port,service_name,http_url,geoip_country_name,geoip_city,geoip_asn_name,geoip_latitude,geoip_longitude,attack_epoch_time,anomaly_event,anomaly_app_proto FROM {indice_name}-* WHERE attacker_ip = '{attacker_ip}' AND sensor_name = '{sensor_name}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL "+s1+s2+f" ORDER BY attack_epoch_time DESC limit 200000;"
        
    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)
    
    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:    
        key_names = [item['name'] for item in run_sql.get('schema')]

        table_query_list = []
        for i, row in enumerate(run_sql.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
        
        return Response({"message_type": "success", "count":len(table_query_list), "attacker_ip":attacker_ip,"table":table_query_list})
    else:
        return Response({"message_type": "d_n_found"})

# 9.a Card Name: Top Source Attack Countries (Bar chart on geoip_country_name column)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trace_alert_country_bar_chart(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('trace_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type": "d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ids_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f" AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    sql = f"SELECT geoip_country_name, COUNT(geoip_country_name) FROM {indice_name}-* WHERE geoip_country_name NOT LIKE 'NA' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL "+s1+s2+f" GROUP BY geoip_country_name ORDER BY COUNT(geoip_country_name) desc LIMIT 7;"
    
    run_sql_query = opensearch_conn_using_db(sql, location_id, plan_id)
    
    if run_sql_query.get("total") not in exclude_values:
        country_name, country_count = map(list, zip(*run_sql_query['datarows']))
        bar_chart_dict = {"series": country_count, "labels": country_name}

        col_val = str(country_name).strip("[]")
        country_tuple = "(" + col_val + ")"

        # for grouping according to sensor_name
        sql2 = f"SELECT sensor_name, geoip_country_name, count(geoip_country_name) geoip_country_name_count FROM {indice_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} "+s1+s2+f" AND geoip_country_name IN {country_tuple} AND sensor_name IS NOT NULL AND ids_threat_class IS NOT NULL GROUP BY sensor_name, geoip_country_name ORDER BY geoip_country_name_count desc;"
        
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
            return Response({"message_type": "d_not_f"})
        
        return Response({"message_type": "success", "bar_chart":bar_chart_dict, "filter":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 9.b Bar chart on geoip_country_name column--Table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trace_alert_country_bar_table(request):
    country_name = request.GET.get('name')
    sensor_name = request.GET.get('name1')

    if country_name is None:
        return Response({"message_type": "d_not_f", "errors": "name_not_found"})
    
    if sensor_name is None:
        return Response({"message_type": "d_not_f", "errors": "sensor_name_not_found"})
    
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('trace_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ids_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f" AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    
    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT attack_timestamp,sensor_name,type_of_threat,ids_threat_class,ids_threat_type,tag,attacker_ip,attacker_host_type,attacker_port,ip_rep,target_ip,target_port,service_name,http_url,geoip_country_name,geoip_city,geoip_asn_name,geoip_latitude,geoip_longitude,attack_epoch_time,anomaly_event,anomaly_app_proto FROM {indice_name}-* WHERE geoip_country_name = '{country_name}' AND sensor_name = '{sensor_name}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL "+s1+s2+f" ORDER BY attack_epoch_time DESC limit 200000;"
    
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


# 10.a Card Name: Top Attacker City (Pie chart on geoip_city column)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trace_alert_city_pie_chart(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('trace_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type": "d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ids_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f" AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    sql = f"SELECT geoip_city, COUNT(geoip_city) FROM {indice_name}-* WHERE geoip_city NOT LIKE 'NA' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL "+s1+s2+f" GROUP BY geoip_city ORDER BY COUNT(geoip_city) desc LIMIT 7;"
    
    run_sql_query = opensearch_conn_using_db(sql, location_id, plan_id)
    
    if run_sql_query.get("total") not in exclude_values:
        geoip_city, city_count = map(list, zip(*run_sql_query['datarows']))
        pie_chart_dict = {"series": city_count, "labels": geoip_city}
        
        col_val = str(geoip_city).strip("[]")
        city_tuple = "(" + col_val + ")"
    
        # for grouping according to sensor_name
        sql2 = f"SELECT sensor_name, geoip_city, count(geoip_city) geoip_city_count FROM {indice_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} "+s1+s2+f" AND geoip_city IN {city_tuple} AND sensor_name IS NOT NULL AND ids_threat_class IS NOT NULL GROUP BY sensor_name, geoip_city ORDER BY geoip_city_count desc;"
        
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
            return Response({"message_type": "d_not_f"})
        
        return Response({"message_type":"success", "pie_chart":pie_chart_dict, "filter":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 10.b Pie chart on geoip_city column--Table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trace_alert_city_pie_table(request):
    city_name = request.GET.get('name')
    sensor_name = request.GET.get('name1')

    if city_name is None:
        return Response({"message_type": "d_not_f", "errors": "name_not_found"})
    
    if sensor_name is None:
        return Response({"message_type": "d_not_f", "errors": "sensor_name_not_found"})
    
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('trace_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type": "d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ids_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f" AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    
    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f'''SELECT attack_timestamp,sensor_name,type_of_threat,ids_threat_class,ids_threat_type,tag,attacker_ip,attacker_host_type,attacker_port,ip_rep,target_ip,target_port,service_name,http_url,geoip_country_name,geoip_city,geoip_asn_name,geoip_latitude,geoip_longitude,attack_epoch_time,anomaly_event,anomaly_app_proto FROM {indice_name}-* WHERE geoip_city = "{city_name}" AND sensor_name = '{sensor_name}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL '''+s1+s2+f''' ORDER BY attack_epoch_time DESC limit 200000;'''
    
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

# 11.a Card Name: Attacker ASN (Bar chart on geoip_asn_name column)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trace_alert_asn_bar_chart(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('trace_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type": "d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ids_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f" AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    sql = f"SELECT geoip_asn_name, COUNT(geoip_asn_name) FROM {indice_name}-* WHERE geoip_asn_name NOT LIKE 'NA' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL "+s1+s2+f" GROUP BY geoip_asn_name ORDER BY COUNT(geoip_asn_name) desc LIMIT 7;"
    
    run_sql_query = opensearch_conn_using_db(sql, location_id, plan_id)
    
    if run_sql_query.get("total") not in exclude_values:
        asn_name, asn_count = map(list, zip(*run_sql_query['datarows']))
        bar_chart_dict = {"series": asn_count, "labels": asn_name}
        
        col_val = str(asn_name).strip("[]")
        asn_name_tuple = "(" + col_val + ")"
    
        # for grouping according to sensor_name
        sql2 = f"SELECT sensor_name, geoip_asn_name, count(geoip_asn_name) geoip_asn_name_count FROM {indice_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} "+s1+s2+f" AND geoip_asn_name IN {asn_name_tuple} AND sensor_name IS NOT NULL AND ids_threat_class IS NOT NULL GROUP BY sensor_name, geoip_asn_name ORDER BY geoip_asn_name_count desc;"
        
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

# 11.b Bar chart on geoip_asn_name column--Table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trace_alert_asn_bar_table(request):
    asn_name = request.GET.get('name')
    sensor_name = request.GET.get('name1')

    if asn_name is None:
        return Response({"message_type": "d_not_f", "errors": "name_not_found"})
    
    if sensor_name is None:
        return Response({"message_type": "d_not_f", "errors": "sensor_name_not_found"})   
    
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('trace_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ids_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f" AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    
    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT attack_timestamp,sensor_name,type_of_threat,ids_threat_class,ids_threat_type,tag,attacker_ip,attacker_host_type,attacker_port,ip_rep,target_ip,target_port,service_name,http_url,geoip_country_name,geoip_city,geoip_asn_name,geoip_latitude,geoip_longitude,attack_epoch_time,anomaly_event,anomaly_app_proto FROM {indice_name}-* WHERE geoip_asn_name = '{asn_name}' AND sensor_name = '{sensor_name}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL "+s1+s2+f" ORDER BY attack_epoch_time DESC limit 200000;"
    
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

# 12.a Card Name: Target IP (Pie chart on target_ip column)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trace_alert_trget_ip_pie_chart(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('trace_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type": "d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ids_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f" AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    sql = f"SELECT target_ip, COUNT(target_ip) FROM {indice_name}-* WHERE (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL "+s1+s2+f" GROUP BY target_ip ORDER BY COUNT(target_ip) desc LIMIT 7;"
    
    run_sql_query = opensearch_conn_using_db(sql, location_id, plan_id)
    
    if run_sql_query.get("total") not in exclude_values:
        target_ip, target_ip_count = map(list, zip(*run_sql_query['datarows']))
        bar_chart_dict = {"series": target_ip_count, "labels": target_ip}
        
        col_val = str(target_ip).strip("[]")
        target_ip_tuple = "(" + col_val + ")"
    
        # for grouping according to sensor_name
        sql2 = f"SELECT sensor_name, target_ip, count(target_ip) target_ip_count FROM {indice_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} "+s1+s2+f" AND target_ip IN {target_ip_tuple} AND sensor_name IS NOT NULL AND ids_threat_class IS NOT NULL GROUP BY sensor_name, target_ip ORDER BY target_ip_count desc;"
        
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
            return Response({"message_type": "d_not_f"})
        
        return Response({"message_type": "success", "bar_chart":bar_chart_dict, "filter":table_query_list})
    else:
        return Response({"message_type": "d_not_f"})

# 12.b Pie chart on target_ip column--Table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trace_alert_trget_ip_table(request):
    target_ip = request.GET.get('name')
    sensor_name = request.GET.get('name1')

    if target_ip is None:
        return Response({"message_type": "d_not_f", "errors": "name_not_found"})
    
    if sensor_name is None:
        return Response({"message_type": "d_not_f", "errors": "sensor_name_not_found"})   
    
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('trace_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ids_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f" AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    
    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT attack_timestamp,sensor_name,type_of_threat,ids_threat_class,ids_threat_type,tag,attacker_ip,attacker_host_type,attacker_port,ip_rep,target_ip,target_port,service_name,http_url,geoip_country_name,geoip_city,geoip_asn_name,geoip_latitude,geoip_longitude,attack_epoch_time,anomaly_event,anomaly_app_proto FROM {indice_name}-* WHERE target_ip = '{target_ip}' AND sensor_name = '{sensor_name}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL "+s1+s2+f" ORDER BY attack_epoch_time DESC limit 200000;"
    
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

# 13 Card Name: Top Attacked Services --only table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trace_alert_attacked_service_details(request):
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
    indice_name = index_name_dict.get('trace_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type": "d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ids_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f" AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""

    sql_query = f"SELECT attacker_ip, service_name, count(*) service_name_count FROM {indice_name}-* WHERE attacker_ip IS NOT NULL AND service_name NOT LIKE 'NA' AND type_of_threat IS NOT NULL "+s1+s2+f" AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} AND ids_threat_class IS NOT NULL GROUP BY attacker_ip,service_name ORDER BY service_name_count DESC LIMIT 50;"
    
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

# 14 Card Name: Frequent Attacker Details--only table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trace_alert_freq_attacker(request):
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
    indice_name = index_name_dict.get('trace_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ids_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f" AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    sql_query = f"SELECT attacker_ip,type_of_threat, count(attacker_ip) attacker_ip_count FROM {indice_name}-* WHERE attacker_ip IS NOT NULL AND type_of_threat IS NOT NULL "+s1+s2+f" AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} AND ids_threat_class IS NOT NULL GROUP BY attacker_ip,type_of_threat ORDER BY attacker_ip_count DESC LIMIT 50;"
    
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
    
# 15.a Card Name: Bruteforce Usernames
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trace_alert_brut_username(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('trace_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ids_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f" AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})

    sql = f"SELECT brut_username FROM {indice_name}-* WHERE brut_username IS NOT NULL AND brut_username NOT IN ('root') AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) "+s1+s2+f" LIMIT 1000;"
    
    run_sql_query = opensearch_conn_using_db(sql, location_id, plan_id)

    if run_sql_query.get("total") not in [0, None]:
    
    # converting nested list into flat list    
        table_query_list = [item for sublist in run_sql_query.get('datarows') for item in sublist]

        return Response({"message_type":"success", "data":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 16.a. Card Name: Bruteforce Passwords
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trace_alert_brut_password(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('trace_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type": "d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ids_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f" AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    sql = f"SELECT brut_password FROM {indice_name}-* WHERE brut_password IS NOT NULL AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) "+s1+s2+f" LIMIT 500;"
    
    run_sql_query = opensearch_conn_using_db(sql, location_id, plan_id)
    
    if run_sql_query.get("total") not in exclude_values:

        # converting nested list into flat list    
        table_query_list = [item for sublist in run_sql_query.get('datarows') for item in sublist]

        return Response({"message_type":"success", "data":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 17.a Card Name: Target Port (Pie chart on target_port column)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trace_alert_trget_port_pie_chart(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('trace_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ids_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f" AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    sql = f"SELECT target_port, COUNT(target_port) FROM {indice_name}-* WHERE (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL "+s1+s2+f" GROUP BY target_port ORDER BY COUNT(target_port) desc LIMIT 7;"
    
    run_sql_query = opensearch_conn_using_db(sql, location_id, plan_id)
    
    if run_sql_query.get("total") not in exclude_values:
        target_port, port_count = map(list, zip(*run_sql_query['datarows']))
        bar_chart_dict = {"series": port_count, "labels": target_port}
        
        col_val = str(target_port).strip("[]")
        target_port_tuple = "(" + col_val + ")"
    
        # for grouping according to sensor_name
        sql2 = f"SELECT sensor_name, target_port, count(target_port) target_port_count FROM {indice_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} "+s1+s2+f" AND target_port IN {target_port_tuple} AND sensor_name IS NOT NULL AND ids_threat_class IS NOT NULL GROUP BY sensor_name, target_port ORDER BY target_port_count desc;"
        
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

# 17.b Pie chart on target_port column--Table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trace_alert_trget_port_table(request):
    target_port = request.GET.get('name')
    if target_port is None:
        return Response({"message_type": "d_not_f", "errors": "name_not_found"})
    
    sensor_name = request.GET.get('name1')
    if sensor_name is None:
        return Response({"message_type": "d_not_f", "errors": "sensor_name_not_found"})
    
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('trace_alert_agent')
    
    detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

    if not detail_dict:
        # got empty dict
        return Response({"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"})
    
    blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
    
    blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
    
    s1 = f"AND ids_threat_class NOT IN {blacklisted_class_tuple}" if blacklisted_class_tuple is not None else ""
    s2 = f" AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    
    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT attack_timestamp,sensor_name,type_of_threat,ids_threat_class,ids_threat_type,tag,attacker_ip,attacker_host_type,attacker_port,ip_rep,target_ip,target_port,service_name,http_url,geoip_country_name,geoip_city,geoip_asn_name,geoip_latitude,geoip_longitude,attack_epoch_time,anomaly_event,anomaly_app_proto FROM {indice_name}-* WHERE target_port = {target_port} AND sensor_name = '{sensor_name}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND ids_threat_class IS NOT NULL "+s1+s2+f" ORDER BY attack_epoch_time DESC limit 200000;"
    
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

# 18. Card Name: Target URL's