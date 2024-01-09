#  ====================================================================================================================================================================
#  File Name: nids_dashboard_page.py
#  Description: It contains all the code for each chart on NIDS Dashboard page on Client Dashboard. Currently NIDS Dashboard page is not active on Client Dashboard.

#  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  =====================================================================================================================================================================

# This file contains all queries of NIDS-Dashboard page
from ..opensearch_config import query
from ..time_filter_on_queries import calculate_start_end_time
from ..grouping_epoch_time import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from collections import defaultdict
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist

# list containing values to exclude from each query--> to avoid error on frontend page
exclude_values = [0,None]

# 1.a Internal Attacks card---counts Lateral Movement attacks
@api_view(['GET'])
def nids_dashboard_int_attack_card(request):
    condition = request.GET.get('condition')
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "invalid_condition"})
    
    lateral_attack_count = query(f"SELECT COUNT(type_of_threat) FROM xdr-logs-whizhack-* WHERE type_of_threat = 'Lateral Movement' AND platform IN ('aws') AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time});")
    # print("lateral_attack_func",lateral_attack_count)
    if lateral_attack_count.get("total") not in exclude_values:
        count_str = str(lateral_attack_count['datarows'])[2:-2]
        count_int = int(count_str)
        
        filter_list = []
        threat_dict = {
                "threat_name": "Lateral Movement",
                "threat_count": count_int,
                "past_time": past_time,
                "current_time": current_time
            }
        filter_list.append(threat_dict)
        
        return Response({"message_type":"success","attack_count":count_int, "filter":filter_list})

    else:
        return Response({"message_type":"d_not_f"})

#1.b Internal Attacks Table
@api_view(['GET'])
def nids_dashboard_int_attack_table(request):
    type_of_threat = request.GET.get('name')
    if type_of_threat is None:
        return Response({"message_type": "name_not_found"})
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    
    if past_time is None:
        return Response({"message_type": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT ids_threat_class, attack_timestamp, target_ip, target_mac_address FROM xdr-logs-whizhack-* WHERE type_of_threat = '{type_of_threat}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform IN ('aws') ORDER BY attack_epoch_time DESC limit 200000;"
    
    run_sql = query(table_query)

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

# 2.a. Outgoing Botnet Connections card--counts internal comp machine attacks
@api_view(['GET'])
def nids_dashboard_outgoing_botnet_card(request):
    condition = request.GET.get('condition')
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "invalid_condition"})
    
    internal_compr_attack_count = query(f"SELECT COUNT(type_of_threat) FROM xdr-logs-whizhack-* WHERE type_of_threat = 'Internal Compromised Machine' AND platform IN ('aws') AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time});")
    # print("internalCompromised_attack_func",internal_compr_attack_count)
    if internal_compr_attack_count.get("total") not in exclude_values:
        count_str = str(internal_compr_attack_count['datarows'])[2:-2]
        count_int = int(count_str)
        
        filter_list = []
        threat_dict = {
                "threat_name": "Internal Compromised Machine",
                "threat_count": count_int,
                "past_time": past_time,
                "current_time": current_time
            }
        filter_list.append(threat_dict)
        
        return Response({"message_type":"success","attack_count":count_int, "filter":filter_list})
    else:
        return Response({"message_type":"d_not_f"})

#2.b Outgoing Botnet Connections Table
@api_view(['GET'])
def nids_dashboard_outgoing_botnet_table(request):
    type_of_threat = request.GET.get('name')
    if type_of_threat is None:
        return Response({"message_type": "name_not_found"})
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    
    if past_time is None:
        return Response({"message_type": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT ids_threat_class, attack_timestamp, target_ip, target_mac_address FROM xdr-logs-whizhack-* WHERE type_of_threat = '{type_of_threat}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform IN ('aws') ORDER BY attack_epoch_time DESC limit 200000;"
    
    run_sql = query(table_query)

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


# 3.a. External Attacks card
@api_view(['GET'])
def nids_dashboard_ext_count(request):
    condition = request.GET.get('condition')
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "invalid_condition"})
    
    external_attack_count = query(f"SELECT type_of_threat, count(type_of_threat) FROM xdr-logs-whizhack-* WHERE type_of_threat IN ('External Attack', 'Attack on External Server') AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform IN ('aws') GROUP BY type_of_threat;")
 
    # print("external_attack_count_func", external_attack_count)
    threat_count = 0
  
    if external_attack_count.get("total") not in exclude_values:
        type_of_threat, indiv_threat_count_list = map(list, zip(*external_attack_count['datarows']))  
        threat_count = sum(indiv_threat_count_list)
        
        filter_list = []
        for i,n in enumerate(type_of_threat):
            threat_dict = {
                "threat_name": n,
                "threat_count": indiv_threat_count_list[i],
                "past_time": past_time,
                "current_time": current_time
            }
        filter_list.append(threat_dict)
        
        return Response({"message_type":"success","attack_count":threat_count, "filter":filter_list})
    else:
        return Response({"message_type":"d_not_f"})

#3.b External Attacks Table
@api_view(['GET'])
def nids_dashboard_ext_count_table(request):
    type_of_threat = request.GET.get('name')
    if type_of_threat is None:
        return Response({"message_type": "name_not_found"})
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    
    if past_time is None:
        return Response({"message_type": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT ids_threat_class, attack_timestamp, target_ip, target_mac_address FROM xdr-logs-whizhack-* WHERE type_of_threat = '{type_of_threat}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform IN ('aws') ORDER BY attack_epoch_time DESC limit 200000;"
    
    run_sql = query(table_query)

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


# 4.a Overall Attack Comparison pie chart
@api_view(['GET'])
def nids_dashboard_overall_attack_pie(request):
    condition = request.GET.get('condition')
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "invalid_condition"})
    
    threat_class_tuple = ('Lateral Movement', 'Internal Compromised Machine', 'External Attack', 'Attack on External Server')
    
    sql = f"SELECT type_of_threat, COUNT(type_of_threat) FROM xdr-logs-whizhack-* WHERE type_of_threat IN {threat_class_tuple} AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform IN ('aws') GROUP BY type_of_threat;"
    
    run_sql_query = query(sql)
    
    if run_sql_query.get("total") not in exclude_values:
        type_of_threat, threat_count = map(list, zip(*run_sql_query['datarows']))
        pie_dict = {"series": threat_count, "labels": type_of_threat}
        
        time_dict = {"past_time":past_time, "current_time":current_time}
        return Response({"message_type":"success", "piechart":pie_dict, "filter":time_dict})
    else:
        return Response({"message_type":"d_not_f"})

# 4.b Overall Attack Comparison--Table
@api_view(['GET'])
def nids_dashboard_overall_attack_table(request):
    threat_type = request.GET.get('name')
    if threat_type is None:
        return Response({"message_type": "name_not_found"})
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    
    if past_time is None:
        return Response({"message_type": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT attack_timestamp, target_ip, ids_threat_class, target_mac_address FROM xdr-logs-whizhack-* WHERE type_of_threat = '{threat_type}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform IN ('aws') ORDER BY attack_epoch_time DESC limit 200000;"
    
    run_sql = query(table_query)
    
    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [item['name'] for item in run_sql.get('schema')]
        
        table_query_list = []
        for i, row in enumerate(run_sql.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
            
        return Response({"message_type":"success", "count":len(table_query_list), "threat_type":threat_type,"table":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 5. Threat Logs card
@api_view(['GET'])
def nids_dashboard_threat_logs(request):
    condition = request.GET.get('condition')
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "invalid_condition"})
    
    formed_sql = f"SELECT t.platform, DATE_FORMAT(attack_timestamp, '%Y-%m-%d %h:%m:%s') attack_timestamp, t.attacker_ip, t.type_of_threat, t.attacker_mac, t.attack_os, t.target_ip, t.target_mac_address, t.target_os, t.ids_threat_class, t.ml_accuracy, t.ml_threat_class, t.dl_accuracy, t.dl_threat_class, t.ids_threat_severity FROM xdr-logs-whizhack-* as t WHERE (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) and t.platform IN ('aws') ORDER BY attack_timestamp DESC;"
    api_response = query(formed_sql)
    # print("dashboard query-->attacker table:", formed_sql)
    # print("o/p of Attacker_Table_func", api_response)
    if api_response.get("total") not in exclude_values:
        key_names = []
        for i in range(len(api_response.get('schema'))):
            if i==1:
                key_names.append(api_response.get('schema')[i].get('alias'))
            else:
                key_names.append(api_response.get('schema')[i].get('name'))
        final_response = []
        for i in range(len(api_response.get('datarows'))):
            row = api_response.get('datarows')[i]
            final_response.append(dict(zip(key_names, row)))
        for i in range(len(final_response)):
            if final_response[i]['dl_threat_class'] == "1.0000000000000001e-103":
                final_response[i]['dl_threat_class'] = "none"
            if final_response[i]['dl_threat_class'] == None:
                final_response[i]['dl_threat_class'] = "not alert"
    else:
        final_response = 0
    return Response({"message_type":"success", "threat_logs": final_response})

# 6.a. Detected Threat Type card  -----(i).ML (ii).DL (iii). IDS
@api_view(['GET'])
def nids_dashboard_detected_threat_type(request):
    condition = request.GET.get('condition')
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "invalid_condition"})
     
    ml_sql_query = f"SELECT ml_threat_class, count(ml_threat_class) count FROM xdr-logs-whizhack-* WHERE ml_threat_class IS NOT NULL and ml_threat_class !='undefined class' and platform IN ('aws') and (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) GROUP BY ml_threat_class ORDER BY count desc LIMIT 7;"
    
    dl_sql_query = f"SELECT dl_threat_class, count(dl_threat_class) count FROM xdr-logs-whizhack-* WHERE dl_threat_class IS NOT NULL AND dl_threat_class !='undefined class' AND platform IN ('aws') and (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) GROUP BY dl_threat_class ORDER BY count desc LIMIT 7;"
    
    ids_sql_query = f"SELECT ids_threat_class, count(ids_threat_class) count FROM xdr-logs-whizhack-* WHERE ids_threat_class IS NOT NULL AND ids_threat_class !='undefined class' AND platform IN ('aws') and (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) GROUP BY ids_threat_class ORDER BY count desc LIMIT 7;"
    
    ml_query_output = query(ml_sql_query)
    dl_query_output = query(dl_sql_query)
    ids_query_output = query(ids_sql_query)
    
    # Check if all "total" values are in the exclude_values set
    if all(value.get("total") not in exclude_values for value in [ml_query_output, dl_query_output, ids_query_output]):
        
        ml_threat_list = []
        ml_threat_class_list,ml_threat_class_count= map(list, zip(*ml_query_output['datarows']))
        
        ml_threat_list = [{
            "name": name,
            "value": count,
            "past_time": past_time,
            "current_time": current_time
        } for name, count in zip(ml_threat_class_list, ml_threat_class_count)]
        
        
        dl_threat_list = []
        dl_threat_class_list,dl_threat_class_count= map(list, zip(*dl_query_output['datarows']))
        
        dl_threat_list = [{
            "name": name,
            "value": count,
            "past_time": past_time,
            "current_time": current_time
        } for name, count in zip(dl_threat_class_list, dl_threat_class_count)]

    
        ids_threat_list = []
        ids_threat_class_list,ids_threat_class_count= map(list, zip(*ids_query_output['datarows']))
        
        ids_threat_list = [{
            "name": name,
            "value": count,
            "past_time": past_time,
            "current_time": current_time
        } for name, count in zip(ids_threat_class_list, ids_threat_class_count)]
        
    
    # response dictionary
        response_dict = {"ml":ml_threat_list, "dl":dl_threat_list, "ids":ids_threat_list} 
        
        return Response({"message_type":"success", "detected_threat_type":response_dict})
    else:
        return Response({"message_type":"d_not_f"})


# 6.b. Detected Threat Type card---Table
@api_view(['GET'])
def nids_dashboard_detected_threat_type_table(request):
    threat_class_type = request.GET.get('type')
    if threat_class_type is None:
        return Response({"message_type": "type_not_f"})    
    
    ids_threat_class = request.GET.get('name')
    if ids_threat_class is None:
        return Response({"message_type": "name_not_f"})
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    
    if past_time is None:
        return Response({"message_type": "past_time_not_f"})

    if current_time is None:
        return Response({"message_type": "current_time_not_f"})
    
    threat_class_type_dict = {
        "ml": "ml_threat_class",
        "dl": "dl_threat_class",
        "ids": "ids_threat_class"
    }
    
    if threat_class_type in threat_class_type_dict:
        
        # sql query to get table data
        table_query = f"SELECT ids_threat_class, attack_timestamp, target_ip, type_of_threat, target_mac_address FROM xdr-logs-whizhack-* WHERE {threat_class_type_dict[threat_class_type]} = '{ids_threat_class}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform IN ('aws') ORDER BY attack_epoch_time DESC limit 200000;"
    
        run_sql = query(table_query)
    
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
        return Response({"message_type":"type_not_f"})

# 7.a. Internal and external attack comparison card--gives datewise count of internal attack, external attack
def query_having_total_zero(query1, query2, query3):
    queries = [query1.get("total"),query2.get("total"),query3.get("total")]
    flag = 0
    query_n=[]
    total_val = {}
    for i,n in enumerate(queries):
        # print("before checking if block")
        if n == 0 or n == None:
            # print("entered if")
            flag = flag+1
            query_n.append(i+1)
            # print("item", i)
            # print("flag val",flag)
        total_val.update({'queries with zero_None as total':flag})
    return total_val,query_n

@api_view(['GET'])
def nids_dashboard_int_ext_attack_count(request):
    condition = request.GET.get('condition')
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "invalid_condition"})
   
    lateral_movement_query=query(f"SELECT DATE_FORMAT(attack_timestamp, '%Y-%m-%d'),COUNT(type_of_threat) FROM xdr-logs-whizhack-* WHERE type_of_threat = 'Lateral Movement' AND platform IN ('aws') AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) GROUP BY DATE_FORMAT(attack_timestamp, '%Y-%m-%d');")
     
    internal_compromised_machine_query=query(f"SELECT DATE_FORMAT(attack_timestamp, '%Y-%m-%d'),COUNT(type_of_threat) FROM xdr-logs-whizhack-* WHERE type_of_threat = 'Internal Compromised Machine' AND platform IN ('aws') AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) GROUP BY DATE_FORMAT(attack_timestamp, '%Y-%m-%d');")
   
    external_attack_query=query(f"SELECT DATE_FORMAT(attack_timestamp, '%Y-%m-%d'),COUNT(type_of_threat) FROM xdr-logs-whizhack-* WHERE type_of_threat IN ('External Attack', 'Attack on External Server') AND platform IN ('aws') AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) GROUP BY DATE_FORMAT(attack_timestamp, '%Y-%m-%d');")
   
    # print("Internal_External_Attack_Count------lateral_movement_query", lateral_movement_query)
    # print("Internal_External_Attack_Count------internal_compromised_machine_query", internal_compromised_machine_query)
    # print("Internal_External_Attack_Count------external_attack_query", external_attack_query)
    # print("lat mov total:", lateral_movement_query.get("total"))
    # print("int comp total:", internal_compromised_machine_query.get("total"))
    # print("ext attack total:", external_attack_query.get("total"))
    catch,n = query_having_total_zero(lateral_movement_query,internal_compromised_machine_query,external_attack_query)
    # print("total values of each query", catch)
    # print("query which has 0 val is:",n)
    if catch["queries with zero_None as total"] == 1:
        for element in n:
            if element==1:
                query1_name=internal_compromised_machine_query
                query2_name=external_attack_query
                key_1="lateral_movement"
                key_2="internal_compromised_machine"
                key_3="external"
            if element==2:
                query1_name=lateral_movement_query
                query2_name=external_attack_query
                key_1="internal_compromised_machine"
                key_2="lateral_movement"
                key_3="external"
            if element==3:
                query1_name=lateral_movement_query
                query2_name=internal_compromised_machine_query
                key_1 = "external"
                key_2 = "lateral_movement"
                key_3 = "internal_compromised_machine"
        date_1,count_1= map(list, zip(*query1_name['datarows']))
        date_2,count_2= map(list, zip(*query2_name['datarows']))
        lat_mov_count_with_Null = []
        query1_count_with_Null = []
        dict_int_compr_machine = dict(zip(date_1,count_1))
        for item in date_2:
            lat_mov_count_with_Null.append(None)
        for item in date_2:
            if item in dict_int_compr_machine:
                query1_count_with_Null.append(dict_int_compr_machine[item])
            else:
                query1_count_with_Null.append(None)
        required_dict = {key_1:lat_mov_count_with_Null, key_2:query1_count_with_Null, key_3:count_2, "labels":date_2}
        return Response({"message_type":"success", "int_ext_dict":required_dict})
    if catch["queries with zero_None as total"] == 2:
        if 1 not in n:
            query_name = lateral_movement_query
            key_1 = "external"
            key_2 = "internal_compromised_machine"
            key_3 = "lateral_movement"
        if 2 not in n:
            query_name = internal_compromised_machine_query
            key_1 = "external"
            key_2 = "lateral_movement"
            key_3 = "internal_compromised_machine"
        if 3 not in n:
            query_name = external_attack_query
            key_1 = "internal_compromised_machine"
            key_2 = "lateral_movement"
            key_3 = "external"
        query_date,query_count= map(list, zip(*query_name['datarows']))
        lat_mov_count_with_Null = []
        int_compr_with_Null = []
        for item in query_date:
            lat_mov_count_with_Null.append(None)
            int_compr_with_Null.append(None)
        required_dict = {key_1:lat_mov_count_with_Null, key_2:int_compr_with_Null, key_3:query_count, "labels":query_date}
        return Response({"message_type":"success", "int_ext_dict":required_dict})
    elif catch["queries with zero_None as total"] == 3:
        required_dict = {"lateral_movement": ["null"], "internal_compromised_machine": ["null"], "external": [0], "labels": ["null"]}
        return Response({"message_type":"success", "int_ext_dict":required_dict})
    elif catch["queries with zero_None as total"] == 0:
        lat_mov_date,lat_mov_count= map(list, zip(*lateral_movement_query['datarows']))
        int_compr_date,int_compr_count= map(list, zip(*internal_compromised_machine_query['datarows']))
        ext_date,ext_count= map(list, zip(*external_attack_query['datarows']))
        lat_mov_count_with_Null = []
        int_compr_with_Null = []
        dict_lat_mov = dict(zip(lat_mov_date,lat_mov_count))
        dict_int_compr_machine = dict(zip(int_compr_date,int_compr_count))
        for item in ext_date:
            if item in dict_lat_mov:
                lat_mov_count_with_Null.append(dict_lat_mov[item])
            else:
                lat_mov_count_with_Null.append(None)
        for item in ext_date:
            if item in dict_int_compr_machine:
                int_compr_with_Null.append(dict_int_compr_machine[item])
            else:
                int_compr_with_Null.append(None)
        
        filter_list = [
            {
                "name": "Lateral Movement",
                "count": sum(lat_mov_count_with_Null),
                "past_time": past_time,
                "current_time": current_time
            },
            {
                "name": "Internal Compromised Machine",
                "count": sum(int_compr_with_Null),
                "past_time": past_time,
                "current_time": current_time
            },
            {
                "name": "External Attack",
                "count": sum(ext_count),
                "past_time": past_time,
                "current_time": current_time
            },
            
            ]
        
        
        required_dict = {"lateral_movement":lat_mov_count_with_Null, "internal_compromised_machine":int_compr_with_Null, "external":ext_count, "labels":ext_date}
        return Response({"message_type":"success", "int_ext_dict":required_dict, "filter":filter_list})

# 7.b. Internal and external attack comparison --Table
@api_view(['GET'])
def nids_dashboard_int_ext_attack_table(request):
    threat_type = request.GET.get('name')
    if threat_type is None:
        return Response({"message_type": "name_not_found"})
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    
    if past_time is None:
        return Response({"message_type": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT attack_timestamp, target_ip, ids_threat_class, target_mac_address FROM xdr-logs-whizhack-* WHERE type_of_threat = '{threat_type}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform IN ('aws') ORDER BY attack_epoch_time DESC limit 200000;"
    
    run_sql = query(table_query)
    
    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [item['name'] for item in run_sql.get('schema')]
        
        table_query_list = []
        for i, row in enumerate(run_sql.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
            
        return Response({"message_type":"success", "count":len(table_query_list), "threat_type":threat_type,"table":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})


# only for testing---new format---modified External Attacks Table
@api_view(['GET'])
def modified_ext_count_card(request):
    condition = request.GET.get('condition')
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "invalid_condition"})
    
    external_attack_count = query(f"SELECT type_of_threat, count(type_of_threat) FROM xdr-logs-whizhack-* WHERE type_of_threat IN ('External Attack', 'Attack on External Server') AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform IN ('aws') GROUP BY type_of_threat;")
 
    # print("external_attack_count_func", external_attack_count)
    threat_count = 0
  
    if external_attack_count.get("total") not in exclude_values:
        type_of_threat, indiv_threat_count_list = map(list, zip(*external_attack_count['datarows']))  
        threat_count = sum(indiv_threat_count_list)
        
        filter_list = []
        for i,n in enumerate(type_of_threat):
            threat_dict = {
                "threat_name": n,
                "threat_count": indiv_threat_count_list[i],
                "past_time": past_time,
                "current_time": current_time
            }
        filter_list.append(threat_dict)
    
    else:
        return Response({"message_type":"d_not_f"})
    
    sql2 = f"SELECT attack_epoch_time FROM xdr-logs-whizhack-* WHERE type_of_threat IN ('External Attack', 'Attack on External Server') AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) AND platform IN ('aws') ORDER BY attack_epoch_time limit 200000;"
    
    search2 = query(sql2)
    
    if search2.get("total") not in exclude_values:
        
        # formatting sql2 query output as (key, value) pairs in dictionary
        table_query_list = []
        for i, key_values in enumerate(search2.get('datarows')):
            Dict = {
                "epoch_time": key_values[0]
            }
            table_query_list.append(Dict)
        
        # # to create series
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
        
        
        
        interval_counts = [0] * len(epoch_interval_group_list)  # Initialize count for each interval to 0
        
        # # print(f"epoch_list:{epoch_interval_group_list}")
        for item in table_query_list:
                epoch_time = item["epoch_time"]
                # print(f"date:{date}")
                for i,interval in enumerate(epoch_interval_group_list):
                    start, end = interval
                    if start <= epoch_time <= end:
                        interval_counts[i] += 1

        return Response({"message_type":"success","series":interval_counts, "total":sum(interval_counts), "filter":filter_list})
    else:
        return Response({"message_type":"d_not_f"})

