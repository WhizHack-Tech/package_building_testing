#  ====================================================================================================================================================================
#  File Name: dashboard_queries.py
#  Description: It contains all the code for each chart on NIDS Dashboard page on Client Dashboard. Currently NIDS Dashboard page is not active on Client Dashboard.

#  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  =====================================================================================================================================================================

import json
from urllib import response
import requests
from django.db import connection
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .opensearch_config import query

# list containing values to exclude from each query--> to avoid error on frontend page
exclude_values = [0,None]

# Lateral Movement count #2
# Internal Attacks card (Dashboard Page)
def lateral_attack_func(agent_name,start_date,end_date,platform,severity):    
    lateral_attack_count = query(f"SELECT COUNT(type_of_threat) FROM {agent_name}-* WHERE type_of_threat = 'Lateral Movement' AND platform IN ({platform}) AND ids_threat_severity IN ({severity}) AND DATE_FORMAT(@timestamp, '%Y-%m-%d') >= '{start_date}' AND DATE_FORMAT(@timestamp, '%Y-%m-%d') <= '{end_date}';")
    # print("lateral_attack_func",lateral_attack_count)
    if lateral_attack_count.get("total") not in exclude_values:
        count_str = str(lateral_attack_count['datarows'])[2:-2]
        mov_count_filter = int(count_str)
    else:
        mov_count_filter = 0
    return mov_count_filter

# Outgoing Botnet Connections card (Dashboard Page) #3
def internalCompromised_attack_func(agent_name,start_date,end_date,platform,severity):    
    internalCompromised_attack_count = query(f"SELECT COUNT(type_of_threat) FROM {agent_name}-* WHERE type_of_threat = 'Internal Compromised Machine' AND platform IN ({platform}) AND ids_threat_severity IN ({severity}) AND DATE_FORMAT(@timestamp, '%Y-%m-%d') >= '{start_date}' AND DATE_FORMAT(@timestamp, '%Y-%m-%d') <= '{end_date}';")
    # print("internalCompromised_attack_func",internalCompromised_attack_count)
    if internalCompromised_attack_count.get("total") not in exclude_values:
        count_str = str(internalCompromised_attack_count['datarows'])[2:-2]
        com_count_filter = int(count_str)
    else:
        com_count_filter = 0
    return com_count_filter

# Severity Label Count#4
# Critical Threats (Dashboard page)
def severity1_attack_count_func(agent_name,start_date,end_date,platform,severity):    
    # severity1_attack_count = query(f"SELECT COUNT(type_of_threat) FROM {agent_name}-* WHERE type_of_threat IS NOT NULL AND ids_threat_severity IN ({severity}) AND DATE_FORMAT(@timestamp, '%Y-%m-%d') >= '{start_date}' AND DATE_FORMAT(@timestamp, '%Y-%m-%d') <= '{end_date}' AND platform IN ({platform});")
    severity1_attack_count = query(f"SELECT COUNT(type_of_threat) FROM {agent_name}-* WHERE type_of_threat IN ('Lateral Movement','External Attack','Attack on External Server')  AND ids_threat_severity IN ({severity}) AND DATE_FORMAT(@timestamp, '%Y-%m-%d') >= '{start_date}' AND DATE_FORMAT(@timestamp, '%Y-%m-%d') <= '{end_date}' AND platform IN ({platform});")
    # print("severity1_attack_count_func",severity1_attack_count)
    severity_count_filter = 0
  
    if severity1_attack_count.get("total") not in exclude_values:
        count_str = str(severity1_attack_count['datarows'])[2:-2]
        severity_count_filter = int(count_str)
    return severity_count_filter

#External #5
# External Attacks card (Dashboard Page)
def external_attack_count_func(agent_name,start_date,end_date,platform,severity):
    external_attack_count = query(f"SELECT count(type_of_threat) FROM {agent_name}-* WHERE type_of_threat IN ('External Attack', 'Attack on External Server') AND ids_threat_severity IN ({severity}) AND DATE_FORMAT(@timestamp, '%Y-%m-%d') >= '{start_date}' AND DATE_FORMAT(@timestamp, '%Y-%m-%d') <= '{end_date}' AND platform IN ({platform});")
 
    # print("external_attack_count_func", external_attack_count)
    eat_count_filter = 0
  
    if external_attack_count.get("total") not in exclude_values:
        count_str = str(external_attack_count['datarows'])[2:-2]
        eat_count_filter = int(count_str)
    # else:
    #     eat_count_filter = 0
    return eat_count_filter

#7
#Dashboard Page: Threat Logs card
def Attacker_Table_func(agent_name,start_date,end_date,platform,severity):
    formed_sql = f"SELECT t.platform, DATE_FORMAT(@timestamp, '%Y-%m-%d %h:%m:%s') target_timestamp, t.attacker_ip, t.type_of_threat, t.attacker_mac, t.attack_os, t.target_ip, t.target_mac_address, t.target_os, t.ids_threat_class, t.ml_accuracy, t.ml_threat_class, t.dl_accuracy, t.dl_threat_class, t.ids_threat_severity FROM {agent_name}-* as t WHERE DATE_FORMAT(@timestamp, '%Y-%m-%d') >= '{start_date}' and DATE_FORMAT(@timestamp, '%Y-%m-%d') <= '{end_date}' and t.ids_threat_severity IN ({severity}) and t.platform IN ({platform}) ORDER BY DATE_FORMAT(@timestamp, '%Y-%m-%d %h:%m:%s') DESC;"
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
    return final_response

#Dashboard Page: Internal and External Attack Comparison Card
# gives datewise count of internal attack, external attack #8
 
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

def Internal_External_Attack_Count(agent_name, start_date, end_date,platform,severity):
   
    lateral_movement_query=query(f"SELECT DATE_FORMAT(@timestamp, '%Y-%m-%d'),COUNT(type_of_threat) FROM {agent_name}-* WHERE type_of_threat = 'Lateral Movement' AND ids_threat_severity IN ({severity}) AND platform IN ({platform}) AND DATE_FORMAT(@timestamp, '%Y-%m-%d') >= '{start_date}' AND DATE_FORMAT(@timestamp, '%Y-%m-%d') <= '{end_date}' GROUP BY DATE_FORMAT(@timestamp, '%Y-%m-%d');")
     
    internal_compromised_machine_query=query(f"SELECT DATE_FORMAT(@timestamp, '%Y-%m-%d'),COUNT(type_of_threat) FROM {agent_name}-* WHERE type_of_threat = 'Internal Compromised Machine' AND ids_threat_severity IN ({severity}) AND platform IN ({platform}) AND DATE_FORMAT(@timestamp, '%Y-%m-%d') >= '{start_date}' AND DATE_FORMAT(@timestamp, '%Y-%m-%d') <= '{end_date}' GROUP BY DATE_FORMAT(@timestamp, '%Y-%m-%d');")
   
    external_attack_query=query(f"SELECT DATE_FORMAT(@timestamp, '%Y-%m-%d'),COUNT(type_of_threat) FROM {agent_name}-* WHERE type_of_threat IN ('External Attack', 'Attack on External Server') AND ids_threat_severity IN ({severity}) AND platform IN ({platform}) AND DATE_FORMAT(@timestamp, '%Y-%m-%d') >= '{start_date}' AND DATE_FORMAT(@timestamp, '%Y-%m-%d') <= '{end_date}' GROUP BY DATE_FORMAT(@timestamp, '%Y-%m-%d');")
   
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
        return required_dict
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
        return required_dict
    elif catch["queries with zero_None as total"] == 3:
        required_dict = {"lateral_movement": ["null"], "internal_compromised_machine": ["null"], "external": [0], "labels": ["null"]}
        return required_dict
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
        required_dict = {"lateral_movement":lat_mov_count_with_Null, "internal_compromised_machine":int_compr_with_Null, "external":ext_count, "labels":ext_date}
        return required_dict

# Detected Threat Type card---Ml
#To count all ml threat class of values and keys #9
def Ml_Threat_Count_Func(agent_name,start_date,end_date,platform,severity):    
    api_response=query(f"SELECT ml_threat_class, count(ml_threat_class) count FROM {agent_name}-* WHERE ml_threat_class IS NOT NULL and ml_threat_class !='undefined class' and ids_threat_severity IN ({severity}) and platform IN ({platform}) and DATE_FORMAT(@timestamp, '%Y-%m-%d') >= '{start_date}' and DATE_FORMAT(@timestamp, '%Y-%m-%d') <= '{end_date}' GROUP BY ml_threat_class ORDER BY count desc LIMIT 7")
   
    ml_threat_list = []
    if api_response.get("total") not in exclude_values:
        ml_threat_class_name,ml_threat_class_count= map(list, zip(*api_response['datarows']))        
        for (key, value) in zip(ml_threat_class_name,ml_threat_class_count):
            dict = {}
            dict.update({"name":key,"val":value})
            ml_threat_list.append(dict)
    return ml_threat_list
   
# Detected Threat Type card---Dl
#To count all dl threat class of values and keys #10
def Dl_Threat_Count_Func(agent_name,start_date,end_date,platform,severity):
    api_response=query(f"SELECT dl_threat_class, count(dl_threat_class) count FROM {agent_name}-* WHERE dl_threat_class IS NOT NULL and dl_threat_class !='undefined class' and ids_threat_severity IN ({severity}) and platform IN ({platform}) and DATE_FORMAT(@timestamp, '%Y-%m-%d') >= '{start_date}' and DATE_FORMAT(@timestamp, '%Y-%m-%d') <= '{end_date}' GROUP BY dl_threat_class ORDER BY count desc LIMIT 7")
    dl_threat_list = []
    if api_response.get("total") not in exclude_values:
        dl_threat_class_name,dl_threat_class_count= map(list, zip(*api_response['datarows']))        
        for (key, value) in zip(dl_threat_class_name,dl_threat_class_count):
            dict = {}
            dict.update({"name":key,"val":value})
            dl_threat_list.append(dict)
    return dl_threat_list

# Detected Threat Type card---IDS
#To count all ids threat class of values and keys #11
def Ids_Threat_Count_Func(agent_name,start_date,end_date,platform,severity):    
    api_response=query(f"SELECT ids_threat_class, count(ids_threat_class) count FROM {agent_name}-* WHERE ids_threat_class IS NOT NULL and ids_threat_class !='undefined class' and ids_threat_severity IN ({severity}) and platform IN ({platform}) and DATE_FORMAT(@timestamp, '%Y-%m-%d') >= '{start_date}' and DATE_FORMAT(@timestamp, '%Y-%m-%d') <= '{end_date}' GROUP BY ids_threat_class ORDER BY count desc LIMIT 7")

    ids_threat_list = []
    if api_response.get("total") not in exclude_values:
        ids_threat_class_name,ids_threat_class_count= map(list, zip(*api_response['datarows']))        
        for (key, value) in zip(ids_threat_class_name,ids_threat_class_count):
            dict = {}
            dict.update({"name":key,"val":value})
            ids_threat_list.append(dict)
    return ids_threat_list

# Overall Attack Comparison pie chart
def internal_external_pie(agent_name,start_date,end_date,platform,severity):
    lateral_mov_count = query(f"SELECT COUNT(type_of_threat) FROM {agent_name}-* WHERE type_of_threat = 'Lateral Movement' AND ids_threat_severity IN ({severity}) AND platform IN ({platform}) AND DATE_FORMAT(@timestamp, '%Y-%m-%d') >= '{start_date}' AND DATE_FORMAT(@timestamp, '%Y-%m-%d') <= '{end_date}';")
    internal_compromised_machine_count = query(f"SELECT COUNT(type_of_threat) internal_count FROM {agent_name}-* WHERE type_of_threat = 'Internal Compromised Machine' AND ids_threat_severity IN ({severity}) AND platform IN ({platform}) AND DATE_FORMAT(@timestamp, '%Y-%m-%d') >= '{start_date}' AND DATE_FORMAT(@timestamp, '%Y-%m-%d') <= '{end_date}';")
    external_attack_count=query(f"SELECT COUNT(type_of_threat) external_count FROM {agent_name}-* WHERE type_of_threat IN ('External Attack', 'Attack on External Server') AND ids_threat_severity IN ({severity}) AND platform IN ({platform}) AND DATE_FORMAT(@timestamp, '%Y-%m-%d') >= '{start_date}' AND DATE_FORMAT(@timestamp, '%Y-%m-%d') <= '{end_date}';")
   
    # print("internal_external_pie----lateral_mov_count:",lateral_mov_count)
    # print("internal_external_pie----internal_compromised_machine_count:",internal_compromised_machine_count)
    # print("internal_external_pie----external_attack_count:",external_attack_count)
   
 
    if lateral_mov_count.get("total") not in exclude_values:
        dict_val1 = str(lateral_mov_count['datarows'])[2:-2]
        lateral_mov_count_integer = int(dict_val1)    
    else:
        dict_val1 = "0"
        lateral_mov_count_integer = 0
    if internal_compromised_machine_count.get("total") not in exclude_values:
        dict_val2 = str(internal_compromised_machine_count['datarows'])[2:-2]
        internal_compromised_machine_count_integer = int(dict_val2)
    else:
        dict_val2 = "0"
        internal_compromised_machine_count_integer = 0
    if external_attack_count.get("total") not in exclude_values:
        dict_val3 = str(external_attack_count['datarows'])[2:-2]
        external_count_integer = int(dict_val3)
    else:
        dict_val3 = "0"
        external_count_integer = 0
    series_list = []
    series_list.extend((lateral_mov_count_integer,internal_compromised_machine_count_integer,external_count_integer))
    required_dict = {"series":series_list, "lateral_mov_count":dict_val1, "internal_compromised_machine_count":dict_val2, "external_count":dict_val3}
    return required_dict


# zero day attack card
def zero_day_attack_card(agent_name,start_date,end_date,platform,severity):
    ml_threat_class = ('A Network Trojan was detected', 'Attempted Administrator Privilege Gain', 'Successful Administrator Privilege Gain', 'Attempted Denial of Service', 'Attempted Information Leak', 'Detection of a Denial of Service Attack', 'Detection of a Network Scan', 'Exploit Kit Activity Detected')
    if severity.__contains__('1'):
        qu = f"SELECT COUNT(type_of_threat) FROM {agent_name}-* WHERE type_of_threat IS NOT NULL AND ids_threat_severity = 1 AND ml_threat_class IN {ml_threat_class} AND (ml_accuracy>=80) AND (ml_accuracy<=100) AND DATE_FORMAT(@timestamp, '%Y-%m-%d') >= '{start_date}' AND DATE_FORMAT(@timestamp, '%Y-%m-%d') <= '{end_date}' AND platform IN ({platform});"
        lateral_attack_count = query(qu)
        if lateral_attack_count.get("total") not in exclude_values:
            count_str = str(lateral_attack_count['datarows'])[2:-2]
            mov_count_filter = int(count_str)
        else:
            mov_count_filter = 0
    else:
        mov_count_filter = 0
    return mov_count_filter