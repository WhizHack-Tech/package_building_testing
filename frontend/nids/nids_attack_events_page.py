#  =============================================================================================================================================================================
#  File Name: nids_attack_events_page.py
#  Description: It contains all the code for each chart on NIDS Attack Events page on Client Dashboard. Currently NIDS Attack Events page is not active on Client Dashboard.

#  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  ==============================================================================================================================================================================

# This file contains all queries of NIDS-Dashboard page
from ..opensearch_config import query
from ..time_filter_on_queries import calculate_start_end_time
from ..grouping_epoch_time import *
from rest_framework.decorators import api_view
from rest_framework.response import Response

# list containing values to exclude from each query--> to avoid error on frontend page
exclude_values = [0,None]


#1.a Top Attacked Services
@api_view(['GET'])
def nids_attck_event_service_name(request):
    condition = request.GET.get('condition')
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "invalid_condition"})
    
    api_response = query(f"SELECT service_name, count(service_name) count FROM xdr-logs-whizhack-* WHERE service_name NOT LIKE 'NA' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) and platform IN ('aws') GROUP BY service_name ORDER BY count DESC LIMIT 6;")
    service_name_count = []
    filter_list = []
    # print("Service_name:", api_response)
    if api_response.get("total") not in exclude_values:
        service_name,service_count= map(list, zip(*api_response['datarows']))
        for (key, value) in zip(service_name,service_count):
            dict = {}
            dict.update({"name":key, "val":value})
            service_name_count.append(dict)
            
            filter_dict = {}
            filter_dict.update({"name":key, "val":value,"past_time":past_time, "current_time":current_time})
            filter_list.append(filter_dict)
            
        # time_dict = {"past_time":past_time, "current_time":current_time}
        return Response({"message_type":"success", "top_attacked_services":service_name_count, "filter":filter_list})
    else:
        return Response({"message_type":"d_not_f"})

#1.b Top Attacked Services Table
@api_view(['GET'])
def nids_attck_event_service_name_table(request):
    service_name = request.GET.get('name')
    if service_name is None:
        return Response({"message_type": "name_not_found"})
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    
    if past_time is None:
        return Response({"message_type": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT attack_timestamp, target_ip, ids_threat_class, target_mac_address FROM xdr-logs-whizhack-* WHERE service_name = '{service_name}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform IN ('aws') ORDER BY attack_epoch_time DESC limit 200000;"
    
    run_sql = query(table_query)
    
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


#2.a Top Source Attack Countries
@api_view(['GET'])
def nids_attck_event_source_country(request):
    condition = request.GET.get('condition')
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "invalid_condition"})
    
    query_output = query(f"SELECT geoip_country_name, COUNT(geoip_country_name) count FROM xdr-logs-whizhack-* WHERE geoip_country_name IS NOT NULL and (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) and platform IN ('aws') GROUP BY geoip_country_name ORDER BY count DESC LIMIT 7;")
    # print("CountryCount:", query_output)
    if query_output.get("total") not in exclude_values:
        list1, list2 = map(list, zip(*query_output['datarows']))
        required_dict = {"series": list2, "labels": list1}
        
        time_dict = {"past_time":past_time, "current_time":current_time}
        return Response({"message_type":"success", "top_countries":required_dict, "filter":time_dict})
    else:
        return Response({"message_type":"d_not_f"})

#2.b Top Source Attack Countries Table
@api_view(['GET'])
def nids_attck_event_source_country_table(request):
    country_name = request.GET.get('name')
    if country_name is None:
        return Response({"message_type": "name_not_found"})
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    
    if past_time is None:
        return Response({"message_type": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT attack_timestamp, target_ip, ids_threat_class, target_mac_address FROM xdr-logs-whizhack-* WHERE geoip_country_name IS NOT NULL AND geoip_country_name = '{country_name}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform IN ('aws') ORDER BY attack_epoch_time DESC limit 200000;"
    
    run_sql = query(table_query)
    
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

# 3.a. Attacker Geo Locations Card
@api_view(['GET'])
def nids_attck_event_geolocation(request):
    condition = request.GET.get('condition')
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "invalid_condition"})

    sql = f"SELECT geoip_city, geoip_latitude,geoip_longitude, count(*) count FROM xdr-logs-whizhack-* WHERE geoip_country_name IS NOT NULL AND geoip_latitude IS NOT NULL AND geoip_longitude IS NOT NULL AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform IN ('aws') AND ids_threat_severity IN (1,2,3) GROUP BY geoip_city,geoip_latitude,geoip_longitude ORDER BY count desc LIMIT 20;"
    
    run_sql = query(sql)
    
    map_value = []
    if run_sql.get("total") not in exclude_values:
        geoip_city, geoip_latitude, geoip_longitude, attack_count = map(list, zip(*run_sql['datarows']))
        latandlon = zip(geoip_longitude, geoip_latitude)
        for (m, n) in zip(latandlon, geoip_city):
            map_value.append({"position": m, "title": n})
        
        filter_list = []
        for i,n in enumerate(geoip_city):
            threat_dict = {
                "title": n,
                "past_time": past_time,
                "current_time": current_time
            }
            filter_list.append(threat_dict)
        
        return Response({"message_type":"success", "geolocation":map_value, "filter":filter_list})
    else:
        return Response({"message_type":"d_not_f"})


# 3.b. geolocation Table
@api_view(['GET'])
def nids_attck_event_geolocation_table(request):
    city_name = request.GET.get('name')
    if city_name is None:
        return Response({"message_type": "name_not_found"})
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    
    if past_time is None:
        return Response({"message_type": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT geoip_country_name, geoip_region_name, attacker_ip, attacker_mac, target_mac_address, attack_timestamp FROM xdr-logs-whizhack-* WHERE geoip_city = '{city_name}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform IN ('aws') AND ids_threat_severity IN (1,2,3) ORDER BY attack_epoch_time DESC limit 200000;"
      
    run_sql = query(table_query)
    
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


# 4.a. Top Attacker Cities Card
@api_view(['GET'])
def nids_attck_event_top_city(request):
    condition = request.GET.get('condition')
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "invalid_condition"})
    
    formed_sql = f"SELECT geoip_city, COUNT(geoip_city) count FROM xdr-logs-whizhack-* WHERE geoip_city IS NOT NULL AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) and platform IN ('aws') GROUP BY geoip_city ORDER BY count DESC LIMIT 7;"
    query_output = query(formed_sql)
    # print("Attack events page--> Geoipcityname", formed_sql)
    if query_output.get("total") not in exclude_values:
        list1, list2 = map(list, zip(*query_output['datarows']))
        required_dict = {"series": list2, "labels": list1}
        
        time_dict = {"past_time":past_time, "current_time":current_time}
        return Response({"message_type":"success", "attacker_city":required_dict, "filter":time_dict})
    else:
        return Response({"message_type":"d_not_f"})

# 4.a. Top Attacker Cities Table
@api_view(['GET'])
def nids_attck_event_city_table(request):
    city_name = request.GET.get('name')
    if city_name is None:
        return Response({"message_type": "name_not_found"})
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    
    if past_time is None:
        return Response({"message_type": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT attack_timestamp, target_ip, ids_threat_class, target_mac_address FROM xdr-logs-whizhack-* WHERE geoip_city IS NOT NULL AND geoip_city = '{city_name}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform IN ('aws') ORDER BY attack_epoch_time DESC limit 200000;"
    
    run_sql = query(table_query)
    
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

# 5.a. Top Attacker ASNs
@api_view(['GET'])
def nids_attck_event_top_asn(request):
    condition = request.GET.get('condition')
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "invalid_condition"})
    
    SQL_query = f"SELECT geoip_asn_name, COUNT(geoip_asn_name) as count FROM xdr-logs-whizhack-* WHERE geoip_asn_name IS NOT NULL and (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) and platform IN ('aws') GROUP BY geoip_asn_name ORDER BY count DESC LIMIT 7;"
    # print(f"query:{SQL_query}")
    query_output = query(SQL_query)
    if query_output.get("total") not in exclude_values:
        list1, list2 = map(list, zip(*query_output['datarows']))
        required_dict = {"series": list2, "labels": list1}
        
        time_dict = {"past_time":past_time, "current_time":current_time}
        return Response({"message_type":"success", "attacker_city":required_dict, "filter":time_dict})
    else:
        return Response({"message_type":"d_not_f"})

# 5.b. Top Attacker ASNs Table
@api_view(['GET'])
def nids_attck_event_asn_table(request):
    asn_name = request.GET.get('name')
    if asn_name is None:
        return Response({"message_type": "name_not_found"})
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    
    if past_time is None:
        return Response({"message_type": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT attack_timestamp, target_ip, ids_threat_class, target_mac_address FROM xdr-logs-whizhack-* WHERE geoip_asn_name IS NOT NULL AND geoip_asn_name = '{asn_name}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform IN ('aws') ORDER BY attack_epoch_time DESC limit 200000;"
    
    run_sql = query(table_query)
    
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


# 6.a. Attacker IPs (Line Chart)
@api_view(['GET'])
def nids_attck_event_ip_line_chart(request):
    condition = request.GET.get('condition')
    past_time, current_time = calculate_start_end_time(condition)
    
    if past_time is None:
        return Response({"message_type": "invalid_condition"})
    
    sql1 = f"SELECT attacker_ip,count(attacker_ip) count FROM xdr-logs-whizhack-* WHERE attacker_ip IS NOT NULL AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform IN ('aws') AND ids_threat_severity IN (1,2,3) GROUP BY attacker_ip ORDER BY count desc LIMIT 7;"  
    
    # print(f"sql1:{sql1}")
    search1 = query(sql1)
    
    if search1.get("total") not in exclude_values:
        unique_IP, unique_IP_count = map(list, zip(*search1['datarows']))
        attacker_ip_tuple = tuple(unique_IP)
        updated_tuple = attacker_ip_tuple
        if len(attacker_ip_tuple) == 1:
            updated_tuple = attacker_ip_tuple+('0',)
    else:
        return Response({"message_type":"d_not_f"})
    
    filter_list = []
    # creating filter values to be returned in response---contains total count of attacker_ip on all given dates
    for i,n in enumerate(unique_IP):
        # dictionary for each attacker_ip
        ip_dict = {
            "name": n,
            "count": unique_IP_count[i],
            "past_time": past_time,
            "current_time": current_time
            }
        filter_list.append(ip_dict)

    # date wise count of a single attacker_ip
    sql2 = f"SELECT attacker_ip, DATE_FORMAT(attack_timestamp,'%Y-%m-%d') as attack_date,count(attacker_ip) count FROM xdr-logs-whizhack-* WHERE attacker_ip IN {updated_tuple} AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform IN ('aws') AND ids_threat_severity IN (1,2,3) GROUP BY DATE_FORMAT(attack_timestamp,'%Y-%m-%d'),attacker_ip ORDER BY attack_date limit 500000;"
    search2 = query(sql2)
    # print(f"sql_two:{sql2}")
    
    if search2.get("total") not in exclude_values:
        Attacker_IP, Dates, individual_ip_counts = map(list, zip(*search2['datarows']))
        # removing redundant elements from list with dates
        unique_dates = list(dict.fromkeys(Dates))
        
        key_names = [item['alias'] if (item['name'] == "count(attacker_ip)") or (item['name'] == "DATE_FORMAT(attack_timestamp,'%Y-%m-%d')")  else item['name'] for item in search2.get('schema')]

        
        table_query_list = []
        for i, key_values in enumerate(search2.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, key_values)))
            table_query_list.append(Dict)
        
        
        series = [] 
        for item in unique_IP:
            filtered_dict = [dictionary for dictionary in table_query_list if dictionary.get('attacker_ip') == item]
            # creating a temporary dictionary with date and count of the filtered attacker ip-----eg. count_dict:{'2023-06-01': 21, '2023-06-02': 61, '2023-06-03': 7}
            count_dict = {entry["attack_date"]: entry["count"] for entry in filtered_dict}
            series_data = [count_dict.get(attack_date) for attack_date in unique_dates]
            ip_dict = {
                "name": item,
                "data": [None if count is None else count for count in series_data]
            }
            series.append(ip_dict)
        
        # creating line_chart dictionary in given format
        line_chart = {"labels":unique_dates, "series":series}
        
        return Response({"message_type":"success", "line_chart":line_chart, "filter":filter_list})
    else:
        return Response({"message_type":"d_not_f"})

# only for testing
# testing to split data according to condition
@api_view(['GET'])
def modified_line_chart(request):
    condition = request.GET.get('condition')
    past_time, current_time = calculate_start_end_time(condition)
    
    # print(f"epoch: between past_time:{past_time}, current_time:{current_time}")
    if past_time is None:
        return Response({"message_type": "invalid_condition"})
    
    sql1 = f"SELECT attacker_ip,count(attacker_ip) count FROM xdr-logs-whizhack-* WHERE attacker_ip IS NOT NULL AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) GROUP BY attacker_ip ORDER BY count desc LIMIT 7;"  
    
    # print(f"sql1:{sql1}")
    search1 = query(sql1)
    
    if search1.get("total") not in exclude_values:
        unique_IP, unique_IP_count = map(list, zip(*search1['datarows']))
        attacker_ip_tuple = tuple(unique_IP)
        updated_tuple = attacker_ip_tuple
        if len(attacker_ip_tuple) == 1:
            updated_tuple = attacker_ip_tuple+('0',)
    else:
        return Response({"message_type":"d_not_f"})
    
    filter_list = []
    # creating filter values to be returned in response---contains total count of attacker_ip on all given dates
    for i,n in enumerate(unique_IP):
        # dictionary for each attacker_ip
        ip_dict = {
            "name": n,
            "count": unique_IP_count[i],
            "past_time": past_time,
            "current_time": current_time
            }
        filter_list.append(ip_dict)

    # date wise count of a single attacker_ip
    sql2 = f"SELECT attacker_ip, attack_epoch_time FROM xdr-logs-whizhack-* WHERE attacker_ip IN {updated_tuple} AND attacker_ip IS NOT NULL AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) ORDER BY attack_epoch_time limit 500000;"
    
    search2 = query(sql2)
    
    if search2.get("total") not in exclude_values:
        
        # formatting sql2 query output as (key, value) pairs in dictionary
        key_names = [item['name'] for item in search2.get('schema')]
        
        table_query_list = []
        for i, key_values in enumerate(search2.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, key_values)))
            table_query_list.append(Dict)
        
        # print(f"length of table_query_list:{len(table_query_list)}")
        
        if condition == "last_5_minutes":
            epoch_interval_group_list = group_time_by_minute(past_time, current_time)
        elif condition == "last_15_minutes":
            epoch_interval_group_list = group_time_by_minute(past_time, current_time)
        elif condition == "last_30_minutes":
            epoch_interval_group_list = group_time_by_5_minutes(past_time, current_time)
        elif condition == "last_1_hour":
            epoch_interval_group_list = group_time_by_5_minutes(past_time, current_time)
        elif condition == "last_24_hours":
            epoch_interval_group_list = group_time_by_3_hours(past_time, current_time)
        elif condition == "last_7_days":
            epoch_interval_group_list = group_time_by_12_hours(past_time, current_time)
        elif condition == "last_30_days":
            epoch_interval_group_list = group_time_by_3_day(past_time, current_time)
        elif condition == "last_90_days":
            epoch_interval_group_list = group_time_by_7_days(past_time, current_time)
        elif condition == "last_1_year":
            epoch_interval_group_list = group_time_by_month(past_time, current_time)
        else:
            return Response({"message_type":"d_not_f", "errors": "condition_not_f"})
        # print(f"epoch_interval_group_list:{epoch_interval_group_list}")
        
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
            # print(f"ip:{ip_value}, len:{len(filtered_dict)}")
            
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
        
        return Response({"message_type":"success","line_chart":line_chart, "filter":filter_list})
    else:
        return Response({"message_type":"d_not_f"})


#6.b. Attacker IPs Table
@api_view(['GET'])
def nids_attck_event_ip_line_table(request):
    attacker_ip = request.GET.get('name')
    if attacker_ip is None:
        return Response({"message_type": "name_not_found"})
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    
    if past_time is None:
        return Response({"message_type": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "current_time_not_found"})

    # sql query to get table data
    table_query = f"SELECT attack_timestamp, target_ip, ids_threat_class, target_mac_address FROM xdr-logs-whizhack-* WHERE attacker_ip = '{attacker_ip}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform IN ('aws') AND ids_threat_severity IN (1,2,3) ORDER BY attack_epoch_time DESC limit 200000;"
        
    run_sql = query(table_query)
    
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
        # print("run_sql.get('total'):",run_sql.get("total") )
        return Response({"message_type":"d_n_found"})

# 7.a. Most Attacked Ports
@api_view(['GET'])
def nids_attck_event_port(request):
    condition = request.GET.get('condition')
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "invalid_condition"})
    
    query_output = query(f"SELECT tcp_port, count(tcp_port) count FROM xdr-logs-whizhack-* WHERE tcp_port IS NOT NULL and (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) and platform IN ('aws') GROUP BY tcp_port ORDER BY count desc LIMIT 7;")
    # print("TcpCount", query_output)
    if query_output.get("total") not in exclude_values:
        list1, list2 = map(list, zip(*query_output['datarows']))
        required_dict = {"series": list2, "labels": list1}
        
        time_dict = {"past_time":past_time, "current_time":current_time}
        return Response({"message_type":"success", "ports":required_dict, "filter":time_dict})
    else:
        return Response({"message_type":"d_not_f"})

# 7.b. Most Attacked Ports Table
@api_view(['GET'])
def nids_attck_event_port_table(request):
    tcp_port = request.GET.get('name')
    if tcp_port is None:
        return Response({"message_type": "name_not_found"})
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    
    if past_time is None:
        return Response({"message_type": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT attack_timestamp, target_ip, ids_threat_class, target_mac_address FROM xdr-logs-whizhack-* WHERE tcp_port IS NOT NULL AND tcp_port = '{tcp_port}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform IN ('aws') ORDER BY attack_epoch_time DESC limit 200000;"
    
    run_sql = query(table_query)
    
    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [item['name'] for item in run_sql.get('schema')]
        
        table_query_list = []
        for i, row in enumerate(run_sql.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
            
        return Response({"message_type":"success", "count":len(table_query_list), "tcp_port":tcp_port,"table":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})



# 8.a. Attacker Mac Addresses
@api_view(['GET'])
def nids_attck_event_mac_addr(request):
    condition = request.GET.get('condition')
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "invalid_condition"})
    
    query_output = query(f"SELECT attacker_mac, COUNT(attacker_mac) count FROM xdr-logs-whizhack-* WHERE attacker_mac IS NOT NULL and  (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) and platform IN ('aws') GROUP BY attacker_mac ORDER BY count DESC LIMIT 7;")
    # print("FrequentAttackerMackAddresses:",query_output)
    if query_output.get("total") not in exclude_values:
        list1, list2 = map(list, zip(*query_output['datarows']))
        required_dict = {"series": list2, "labels": list1}
        
        time_dict = {"past_time":past_time, "current_time":current_time}
        return Response({"message_type":"success", "ports":required_dict, "filter":time_dict})
    else:
        return Response({"message_type":"d_not_f"})

@api_view(['GET'])
def nids_attck_event_mac_table(request):
    attacker_mac = request.GET.get('name')
    if attacker_mac is None:
        return Response({"message_type": "name_not_found"})
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    
    if past_time is None:
        return Response({"message_type": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT attack_timestamp, target_ip, ids_threat_class, target_mac_address FROM xdr-logs-whizhack-* WHERE attacker_mac IS NOT NULL AND attacker_mac = '{attacker_mac}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform IN ('aws') ORDER BY attack_epoch_time DESC limit 200000;"
    
    run_sql = query(table_query)
    
    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [item['name'] for item in run_sql.get('schema')]
        
        table_query_list = []
        for i, row in enumerate(run_sql.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
            
        return Response({"message_type":"success", "count":len(table_query_list), "attacker_mac_address":attacker_mac,"table":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 9.a. Attack Frequency 
@api_view(['GET'])
def nids_attck_event_frequency(request):
    condition = request.GET.get('condition')
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "invalid_condition"})
    
    SQL_query = query(f"SELECT DATE_FORMAT(attack_timestamp, '%Y-%m-%d') Date, count(*) FROM xdr-logs-whizhack-* WHERE (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) and platform IN ('aws') GROUP BY DATE_FORMAT(attack_timestamp,'%Y-%m-%d') ORDER BY DATE_FORMAT(attack_timestamp, '%Y-%m-%d');")
    # print("FrequencyOfAttacks:", SQL_query)
    
    filter_list = []
    if SQL_query.get("total") not in exclude_values:
        Dates, count_of_attacks = map(list, zip(*SQL_query['datarows']))
        required_dict = {"categories": Dates, "series": count_of_attacks}
        
        for (key, value) in zip(Dates,count_of_attacks):
            filter_dict = {}
            filter_dict.update({"name":key, "val":value,"past_time":past_time, "current_time":current_time})
            filter_list.append(filter_dict)
        
        return Response({"message_type":"success", "ports":required_dict, "filter":filter_list})
    else:
        return Response({"message_type":"d_not_f"})

# 9.b. Attack Frequency Table
@api_view(['GET'])
def nids_attck_event_freq_table(request):
    attack_date = request.GET.get('name')
    if attack_date is None:
        return Response({"message_type": "name_not_found"})
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    
    if past_time is None:
        return Response({"message_type": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT attack_timestamp, target_ip, ids_threat_class, target_mac_address FROM xdr-logs-whizhack-* WHERE DATE_FORMAT(attack_timestamp, '%Y-%m-%d') = '{attack_date}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform IN ('aws') ORDER BY attack_epoch_time DESC limit 200000;"
    
    run_sql = query(table_query)
    
    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [item['name'] for item in run_sql.get('schema')]
        
        table_query_list = []
        
        for i, row in enumerate(run_sql.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
            
        return Response({"message_type":"success", "count":len(table_query_list), "attack_date":attack_date, "table":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})
    