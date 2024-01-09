#  ==============================================================================================================================
#  File Name: common_query_all_agents.py
#  Description: It contains all the code for each chart on Sensor Health page under Health Check tab on Client Dashboard.
#  Active URL: https://xdr-demo.zerohack.in/health-check/sensor-health

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

#1. Returns health_check status of all products
@never_cache
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def health_check_status_all_products(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('hc_agent')

    past_time, current_time = calculate_start_end_time(condition)
    set_response = {"message_type":"success"}

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    # sql query to get data
    sql_query = f'''SELECT sensor_id, sensor_type, sensor_name FROM {indice_name}-* WHERE sensor_id NOT IN (null, "") AND sensor_type IS NOT NULL AND sensor_name IS NOT NULL AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) GROUP BY sensor_id, sensor_type, sensor_name ORDER BY attack_epoch_time DESC;'''
    
    run_sql = opensearch_conn_using_db(sql_query, location_id, plan_id)

    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in [0,None]:
        # converting new query to table format
        key_names = [item['name'] for item in run_sql.get('schema')]

        new_query_table_data = []
        for i, row in enumerate(run_sql.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            new_query_table_data.append(Dict)

        sensor_id, sensor_type, sensor_name = map(list, zip(*run_sql['datarows']))
        unique_sensor_type = list(set(sensor_type))
        set_response["trace"] = False
        set_response["nids"] = False
        set_response["hids"] = False
        set_response["soar"] = False
        set_response["data"] = {}

        if "TRACE" in unique_sensor_type:
            set_response["trace"] = True

            # filtering trace sensor_type
            trace_filtered_dict = [dictionary for dictionary in new_query_table_data if dictionary.get('sensor_type') == 'TRACE']
            sensor_id_list = [item['sensor_id'] for item in trace_filtered_dict]
            sensor_id_tuple = str(sensor_id_list).replace("[", "(").replace("]", ")")
            trace_sensor_id_name_nested_list = [[item['sensor_id'], item['sensor_name']] for item in trace_filtered_dict]

            # sql query to get trace data
            trace_query = f"SELECT sensor_id,sensor_type,sensor_name FROM {indice_name}-* WHERE sensor_id IN {sensor_id_tuple} AND sensor_type = 'TRACE' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) GROUP BY sensor_id,sensor_type,sensor_name ORDER BY attack_epoch_time DESC;"
            
            run_sql_trace = opensearch_conn_using_db(trace_query, location_id, plan_id)
            
            # formatting above query output to {column_name: column_value}
            if run_sql_trace.get("total") not in [0,None]:
                # sensor_id, sensor_type, sensor_name  = map(list, zip(*run_sql_trace['datarows']))
                key_names = [item['name'] for item in run_sql_trace.get('schema')]

                epoch_time_list = []
                for sensor_id, sensor_name in trace_sensor_id_name_nested_list:
                    trace_latest_timestamp_query = f"SELECT attack_epoch_time FROM {indice_name}-* WHERE sensor_id = '{sensor_id}' AND sensor_type = 'TRACE' AND sensor_name = '{sensor_name}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) ORDER BY attack_epoch_time DESC limit 1;"
                    
                    run_sql_trace_latest_timestamp = opensearch_conn_using_db(trace_latest_timestamp_query, location_id, plan_id)

                    if run_sql_trace_latest_timestamp.get("total") not in [0,None]:
                        latest_attack_epoch_time = str(run_sql_trace_latest_timestamp['datarows'])[2:-2]
                        attack_epoch_time = datetime.fromtimestamp(int(latest_attack_epoch_time) / 1000).strftime('%Y-%m-%d %I:%M:%S %p')  # 12-hour format with AM/PM
                        epoch_time_list.append(attack_epoch_time)
            
                trace_data_list = []
                for row, attack_epoch_time in zip(run_sql_trace.get('datarows'), epoch_time_list):
                    Dict = {}
                    Dict.update(dict(zip(key_names, row)))
                    Dict.update({"attack_epoch_time":attack_epoch_time})
                    trace_data_list.append(Dict)

                set_response["data"].update({"trace":trace_data_list})
        else:
            set_response["data"].update({"trace":[]})

        if "NIDS" in unique_sensor_type:
            set_response["nids"] = True

            # filtering nids sensor_type
            nids_filtered_dict = [dictionary for dictionary in new_query_table_data if dictionary.get('sensor_type') == 'NIDS']
            nids_sensor_id_list = [item['sensor_id'] for item in nids_filtered_dict]
            nids_sensor_id_tuple = str(nids_sensor_id_list).replace("[", "(").replace("]", ")")
            nids_sensor_id_name_nested_list = [[item['sensor_id'], item['sensor_name']] for item in nids_filtered_dict]

            # sql query to get nids data
            nids_query = f"SELECT sensor_id,sensor_type,sensor_name FROM {indice_name}-* WHERE sensor_id IN {nids_sensor_id_tuple} AND sensor_type = 'NIDS' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) GROUP BY sensor_id,sensor_type,sensor_name ORDER BY attack_epoch_time DESC;"
            
            run_sql_nids = opensearch_conn_using_db(nids_query, location_id, plan_id)
            
            # formatting above query output to {column_name: column_value}
            if run_sql_nids.get("total") not in [0,None]:
                key_names = [item['name'] for item in run_sql_nids.get('schema')]

                nids_epoch_time_list = []
                for sensor_id, sensor_name in nids_sensor_id_name_nested_list:
                    nids_latest_timestamp_query = f"SELECT attack_epoch_time FROM {indice_name}-* WHERE sensor_id = '{sensor_id}' AND sensor_type = 'NIDS' AND sensor_name = '{sensor_name}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) ORDER BY attack_epoch_time DESC limit 1;"
                    
                    run_sql_nids_latest_timestamp = opensearch_conn_using_db(nids_latest_timestamp_query, location_id, plan_id)

                    if run_sql_nids_latest_timestamp.get("total") not in [0,None]:
                        latest_attack_epoch_time = str(run_sql_nids_latest_timestamp['datarows'])[2:-2]
                        attack_epoch_time = datetime.fromtimestamp(int(latest_attack_epoch_time) / 1000).strftime('%Y-%m-%d %I:%M:%S %p')  # 12-hour format with AM/PM
                        nids_epoch_time_list.append(attack_epoch_time)
            
                nids_data_list = []
                for row, attack_epoch_time in zip(run_sql_nids.get('datarows'), nids_epoch_time_list):
                    Dict = {}
                    Dict.update(dict(zip(key_names, row)))
                    Dict.update({"attack_epoch_time":attack_epoch_time})
                    nids_data_list.append(Dict)

                set_response["data"].update({"nids":nids_data_list})
        else:
            set_response["data"].update({"nids":[]})
        
        if "HIDS" in unique_sensor_type:
            set_response["hids"] = True

            # filtering unique sensor_type
            hids_filtered_dict = [dictionary for dictionary in new_query_table_data if dictionary.get('sensor_type') == 'HIDS']
            hids_sensor_id_list = [item['sensor_id'] for item in hids_filtered_dict]
            hids_sensor_id_tuple = str(hids_sensor_id_list).replace("[", "(").replace("]", ")")
            hids_sensor_id_name_nested_list = [[item['sensor_id'], item['sensor_name']] for item in hids_filtered_dict]

            # sql query to get hids data
            hids_query = f"SELECT sensor_id,sensor_type,sensor_name FROM {indice_name}-* WHERE sensor_id IN {hids_sensor_id_tuple} AND sensor_type = 'HIDS' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) GROUP BY sensor_id,sensor_type,sensor_name ORDER BY attack_epoch_time DESC;"
            
            run_sql_hids = opensearch_conn_using_db(hids_query, location_id, plan_id)
            
            # formatting above query output to {column_name: column_value}
            if run_sql_hids.get("total") not in [0,None]:
                key_names = [item['name'] for item in run_sql_hids.get('schema')]

                hids_epoch_time_list = []
                for sensor_id, sensor_name in hids_sensor_id_name_nested_list:
                    hids_latest_timestamp_query = f"SELECT attack_epoch_time FROM {indice_name}-* WHERE sensor_id = '{sensor_id}' AND sensor_type = 'HIDS' AND sensor_name = '{sensor_name}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) ORDER BY attack_epoch_time DESC limit 1;"
                    
                    run_sql_hids_latest_timestamp = opensearch_conn_using_db(hids_latest_timestamp_query, location_id, plan_id)

                    if run_sql_hids_latest_timestamp.get("total") not in [0,None]:
                        latest_attack_epoch_time = str(run_sql_hids_latest_timestamp['datarows'])[2:-2]
                        attack_epoch_time = datetime.fromtimestamp(int(latest_attack_epoch_time) / 1000).strftime('%Y-%m-%d %I:%M:%S %p')  # 12-hour format with AM/PM
                        hids_epoch_time_list.append(attack_epoch_time)
            
                hids_data_list = []
                for row, attack_epoch_time in zip(run_sql_hids.get('datarows'), hids_epoch_time_list):
                    Dict = {}
                    Dict.update(dict(zip(key_names, row)))
                    Dict.update({"attack_epoch_time":attack_epoch_time})
                    hids_data_list.append(Dict)
                
                set_response["data"].update({"hids":hids_data_list})

        else:
            set_response["data"].update({"hids":[]})
        
        if "SOAR" in unique_sensor_type:
            set_response["soar"] = True

            # filtering soar sensor_type
            soar_filtered_dict = [dictionary for dictionary in new_query_table_data if dictionary.get('sensor_type') == 'SOAR']
            soar_sensor_id_list = [item['sensor_id'] for item in soar_filtered_dict]
            soar_sensor_id_tuple = str(soar_sensor_id_list).replace("[", "(").replace("]", ")")
            soar_sensor_id_name_nested_list = [[item['sensor_id'], item['sensor_name']] for item in soar_filtered_dict]

            # sql query to get soar data
            soar_query = f"SELECT sensor_id,sensor_type,sensor_name FROM {indice_name}-* WHERE sensor_id IN {soar_sensor_id_tuple} AND sensor_type = 'SOAR' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) GROUP BY sensor_id,sensor_type,sensor_name ORDER BY attack_epoch_time DESC;"
            
            run_sql_soar = opensearch_conn_using_db(soar_query, location_id, plan_id)
            
            # formatting above query output to {column_name: column_value}
            if run_sql_soar.get("total") not in [0,None]:
                key_names = [item['name'] for item in run_sql_soar.get('schema')]

                soar_epoch_time_list = []
                for sensor_id, sensor_name in soar_sensor_id_name_nested_list:
                    soar_latest_timestamp_query = f"SELECT attack_epoch_time FROM {indice_name}-* WHERE sensor_id = '{sensor_id}' AND sensor_type = 'SOAR' AND sensor_name = '{sensor_name}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) ORDER BY attack_epoch_time DESC limit 1;"
                    
                    run_sql_soar_latest_timestamp = opensearch_conn_using_db(soar_latest_timestamp_query, location_id, plan_id)

                    if run_sql_soar_latest_timestamp.get("total") not in [0,None]:
                        latest_attack_epoch_time = str(run_sql_soar_latest_timestamp['datarows'])[2:-2]
                        attack_epoch_time = datetime.fromtimestamp(int(latest_attack_epoch_time) / 1000).strftime('%Y-%m-%d %I:%M:%S %p')  # 12-hour format with AM/PM
                        soar_epoch_time_list.append(attack_epoch_time)
            
                soar_data_list = []
                for row, attack_epoch_time in zip(run_sql_soar.get('datarows'), soar_epoch_time_list):
                    Dict = {}
                    Dict.update(dict(zip(key_names, row)))
                    Dict.update({"attack_epoch_time":attack_epoch_time})
                    soar_data_list.append(Dict)

                set_response["data"].update({"soar":soar_data_list})
        else:
            set_response["data"].update({"soar":[]})

        set_response["filter"] = {"past_time":past_time, "current_time":current_time, "condition": condition}
            
        return Response(set_response)
    else:
        return Response({"message_type":"d_not_f"})


#2. cpu_utilization, ram_utilization, disk_remaining of latest time acc to sent sensor_type in params
# single view for Card Names: CPU Utilization, RAM Used, Disk Remaining
@never_cache
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def health_check_dynamic_latest_cpu_ram_disk(request):
    sensor_type = request.GET.get('sensor_type')

    if sensor_type is None:
        return Response({"message_type": "d_not_f", "errors": "sensor_type_n_found"})

    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('hc_agent')
    
    set_response = {"message_type":"success", "data": {}}
    # sql query
    sql_query = f'''SELECT cpu_utilization, ram_utilization, disk_remaining FROM {indice_name}-* WHERE sensor_type = '{sensor_type}' ORDER BY attack_epoch_time DESC LIMIT 1;'''
    
    run_sql = opensearch_conn_using_db(sql_query, location_id, plan_id)

    if run_sql.get("total") not in [0,None]:
        cpu_uti, ram_uti, disk = run_sql['datarows'][0]
        set_response["data"].update({"cpu_utilization":cpu_uti, "ram_utilization": ram_uti, "disk_remaining":disk})
    else:
        set_response["data"].update({"cpu_utilization":0, "ram_utilization": 0, "disk_remaining":0})

    return Response(set_response)


# table- all excluding client_geoip_city, client_geoip_latitude, client_geoip_longitude, client_geoip_country_code, client_geoip_country_name, @timestamp (Health check Logs only Table)
#3. Card Name: Health Check Logs
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def health_check_logs_only_table(request):
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('hc_agent')
    
    sensor_id = request.GET.get('sensor_id')
    sensor_type = request.GET.get('sensor_type')
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')

    if sensor_id is None:
        return Response({"message_type": "d_not_f", "errors": "sensor_id_n_found"})

    if sensor_type is None:
        return Response({"message_type": "d_not_f", "errors": "sensor_type_n_found"})

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT level_id, level, @timestamp, ip_address, cpu_utilization, ram_utilization, disk_remaining, disk_action, license_status, xdr_trace_status, sensor_type, sensor_id, sensor_name, download_speed, upload_speed FROM {indice_name}-* WHERE (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND sensor_id = '{sensor_id}' AND sensor_type = '{sensor_type}' ORDER BY attack_epoch_time DESC;"
    
    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)

    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in [0,None]:
        key_names = ['timestamp' if (item['name'] == "@timestamp") else item['name'] for item in run_sql.get('schema')]
    
        table_query_list = []
        for i, row in enumerate(run_sql.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
        
        for item in table_query_list:
            if "timestamp" in item:
                with_fractional_part = item.get('timestamp')
                item['timestamp'] = with_fractional_part.split(".")[0]
            
        return Response({"message_type":"success", "count":len(table_query_list), "table":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})


#4.a. Card Name: Health Check Feeds (line chart on 'level' between past, current time)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def health_check_level_line_chart(request):
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('hc_agent')

    sensor_id = request.GET.get('sensor_id')
    sensor_type = request.GET.get('sensor_type')
    past_time = int(request.GET.get('past_time'))
    current_time = int(request.GET.get('current_time'))
    condition = request.GET.get('condition')

    if sensor_id is None:
        return Response({"message_type": "d_not_f", "errors": "sensor_id_n_found"})

    if sensor_type is None:
        return Response({"message_type": "d_not_f", "errors": "sensor_type_n_found"})

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_n_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_n_found"})
    
    if condition is None:
        return Response({"message_type": "d_not_f", "errors": "condition_n_found"})
    
    sql_query = f"SELECT level, attack_epoch_time FROM {indice_name}-* WHERE level IN ('running', 'stopped') AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND sensor_id = '{sensor_id}' AND sensor_type = '{sensor_type}' ORDER BY attack_epoch_time DESC limit 5000;"
    
    search2 = opensearch_conn_using_db(sql_query, location_id, plan_id)
    
    if search2.get("total") not in [0,None]:

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
        filter_list = []
        
        response_dict["message_type"] = "success"
        response_dict["total"] = len(table_query_list)
        
        for level in ('running','stopped'):
            filtered_dict = [dictionary for dictionary in table_query_list if dictionary.get('level') == level]
            level_dict = {
                "level": level,
                "sensor_id": sensor_id,
                "sensor_type": sensor_type,
                "level_count": len(filtered_dict),
                "past_time": past_time,
                "current_time": current_time
            }
            filter_list.append(level_dict)
            
            if len(filtered_dict) == 0:
                response_dict[level]
            else:
                for item in filtered_dict:
                    epoch_date = item["attack_epoch_time"]
                    for i, (start, end) in enumerate(epoch_interval_group_list):
                        if start <= epoch_date <= end:
                            response_dict[level][i] += 1
        
        response_dict["filter"]= filter_list
            
        return Response(response_dict)
    else:
        return Response({"message_type":"d_not_f"})
    
#4.b Level line chart Table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def health_check_level_line_chart_table(request):
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('hc_agent')
    
    sensor_id = request.GET.get('sensor_id')
    sensor_type = request.GET.get('sensor_type')
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    level = request.GET.get('level')
    
    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})
    
    if sensor_id is None:
        return Response({"message_type": "d_not_f", "errors": "sensor_id_n_found"})

    if sensor_type is None:
        return Response({"message_type": "d_not_f", "errors": "sensor_type_n_found"})
    
    if level is None:
        return Response({"message_type": "d_not_f", "errors": "level_n_found"})
    
    # sql query to get table data
    table_query = f"SELECT level_id, level, @timestamp, ip_address, cpu_utilization, ram_utilization, disk_remaining, disk_action, license_status, xdr_trace_status, sensor_type, sensor_id, sensor_name FROM {indice_name}-* WHERE (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND sensor_id = '{sensor_id}' AND sensor_type = '{sensor_type}' AND level = '{level}' ORDER BY attack_epoch_time DESC LIMIT 5000;"
    
    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)

    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in [0, None]:
        key_names = ['timestamp' if (item['name'] == "@timestamp") else item['name'] for item in run_sql.get('schema')]
    
        table_query_list = []
        for i, row in enumerate(run_sql.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
        
        for item in table_query_list:
            if "timestamp" in item:
                with_fractional_part = item.get('timestamp')
                item['timestamp'] = with_fractional_part.split(".")[0]
            
        return Response({"message_type":"success", "count":len(table_query_list), "level":level,"table":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})