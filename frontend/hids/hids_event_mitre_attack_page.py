#  ===============================================================================================
#  File Name: hids_event_wazuh_mitre_attack_page.py
#  Description: This file contains code for each card on HIDS Event Page.
#  Active URL: https://xdr-demo.zerohack.in/hids/events

#  ----------------------------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  ===============================================================================================

from ..helpers import (
    getIndexNameByLocationId,
    getMlDlAccuracyRanges,
    getPlatformAndBlacklistedItemsByLocationId,
    pre_check_parameters,
)
from ..time_filter_on_queries import calculate_start_end_time
from ..grouping_epoch_time import *
from ..opensearch_config import opensearch_conn_using_db
from ..time_filter_on_queries import calculate_start_end_time
from rest_framework.decorators import api_view
from rest_framework.response import Response
from collections import defaultdict
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

g = globals()
exclude_values = [0,None]

# Mitre Attack Page-pie chart(card name = Top Tactics)
def hids_event_top_tactics_func(agent_id,indice_name,current_time,past_time, location_id, plan_id):
    SQL_query = f"SELECT rule_mitre_tactic, count(rule_mitre_tactic) count from {indice_name}-* WHERE rule_mitre_tactic IS NOT NULL AND agent_id = {agent_id} AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} Group By rule_mitre_tactic ORDER BY count DESC LIMIT 5;"
    api_response = opensearch_conn_using_db(SQL_query, location_id, plan_id)
    if api_response.get("total") not in exclude_values:
        rule_mitre_tactic,count= map(list, zip(*api_response['datarows']))
        reqd_dict = {"series":count , "labels":rule_mitre_tactic}
        return {"message_type":"data_found","data":reqd_dict}
    else:
        return {"message_type":"d_not_f"}

# Mitre Attack Page-pie chart(card name = Rule Level By Attack)
def hids_event_rule_level_byattack_func(agent_id,indice_name,current_time,past_time, location_id, plan_id):

    SQL_query = f"SELECT rule_mitre_id, count(rule_mitre_id) count from {indice_name}-* WHERE rule_mitre_id IS NOT NULL AND agent_id = {agent_id} AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} Group By rule_mitre_id ORDER BY count DESC LIMIT 5;"
    api_response = opensearch_conn_using_db(SQL_query, location_id, plan_id)
    if api_response.get("total") not in exclude_values:
        rule_mitre_id,count= map(list, zip(*api_response['datarows']))
        reqd_dict = {"series":count , "labels":rule_mitre_id}
        return {"message_type":"data_found","data":reqd_dict}
    else:
        return {"message_type":"d_not_f"}

# Mitre Attack Page-pie chart(card name = Rule Level By Tactics)
def hids_event_rule_level_by_tactics_func(agent_id,indice_name,current_time,past_time, location_id, plan_id):

    SQL_query = f"SELECT rule_mitre_technique, count(rule_mitre_technique) count from {indice_name}-* WHERE rule_mitre_technique IS NOT NULL AND agent_id = {agent_id} AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} Group By rule_mitre_technique ORDER BY count DESC LIMIT 5;"
    api_response = opensearch_conn_using_db(SQL_query, location_id, plan_id)
    if api_response.get("total") not in exclude_values:
        rule_mitre_technique,count= map(list, zip(*api_response['datarows']))
        reqd_dict = {"series":count , "labels":rule_mitre_technique}
        return {"message_type":"data_found","data":reqd_dict}
    else:
        return {"message_type":"d_not_f"}

# ########################################################################
# Line chart

# Mitre Attack Page-line chart(card name = Alerts evolution over time)
def hids_event_alerts_evolution_overtime_func(agent_id,indice_name,current_time,past_time, condition, location_id, plan_id):

    updated_current_time = int(current_time)
    updated_past_time = int(past_time)
    sql1 = f"SELECT rule_mitre_tactic,count(rule_mitre_tactic) count FROM {indice_name}-* WHERE rule_mitre_tactic IS NOT NULL and agent_id = {agent_id} AND attack_epoch_time >= {updated_past_time} AND attack_epoch_time <= {updated_current_time} GROUP BY rule_mitre_tactic ORDER BY count desc LIMIT 7;"  
    
    search1 = opensearch_conn_using_db(sql1, location_id, plan_id)
    
    if search1.get("total") not in exclude_values:
        unique_tactics, tactic_count = map(list, zip(*search1['datarows']))
        unique_tactics_tuple = tuple(unique_tactics)
        updated_tuple = unique_tactics_tuple
        if len(unique_tactics_tuple) == 1:
            updated_tuple = unique_tactics_tuple+('0',)
    else:
        return {"message_type":"d_not_f"}

    # date wise count of a single tactic
    sql2 = f"SELECT rule_mitre_tactic, attack_epoch_time FROM {indice_name}-* WHERE rule_mitre_tactic IN {updated_tuple} and agent_id = {agent_id} AND attack_epoch_time >= {updated_past_time} AND attack_epoch_time <= {updated_current_time} ORDER BY attack_epoch_time limit 500000;"
    
    search2 = opensearch_conn_using_db(sql2, location_id, plan_id)
    
    if search2.get("total") not in exclude_values:
        # formatting sql2 query output as (key, value) pairs in dictionary
        key_names = [item['name'] for item in search2.get('schema')]
        
        table_query_list = []
        for i, key_values in enumerate(search2.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, key_values)))
            table_query_list.append(Dict)
        
        epoch_interval_group_list = getEpochIntervalGroupList(condition, updated_past_time, updated_current_time)

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
        for tactic_value in unique_tactics:
            filtered_dict = [dictionary for dictionary in table_query_list if dictionary.get('rule_mitre_tactic') == tactic_value]
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
                "name": tactic_value,
                "data": [None if count == 0 else count for count in interval_counts]
                # "sum": sum(interval_counts)#added only for testing purpose
                
            }
            series.append(ip_dict)
        
        # creating line_chart dictionary in given format
        line_chart = {"labels":new_lables, "series":series}
        return {"message_type":"data_found","data":line_chart}
    else:
        return {"message_type":"d_not_f"}

# Mitre Attack Page-Bar chart(card name = Mitre Attacks By Tactic)
def hids_event_mitre_attackby_tactic_func(agent_id,indice_name,current_time,past_time, location_id, plan_id):
    search1 = opensearch_conn_using_db(f"SELECT rule_mitre_tactic,count(rule_mitre_tactic) count FROM {indice_name}-* WHERE rule_mitre_tactic IS NOT NULL and agent_id = {agent_id} AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY rule_mitre_tactic ORDER BY count desc LIMIT 7;", location_id, plan_id)
    # print("AttackerIPCount--finding top7 attacker ip:",search1 )
    if search1.get("total") not in exclude_values:
        unique_tactics, list2 = map(list, zip(*search1['datarows']))
        attacker_ip_tuple = tuple(unique_tactics)
        updated_tuple = attacker_ip_tuple
        if len(attacker_ip_tuple) == 1:
            updated_tuple = attacker_ip_tuple+('0',)
    else:
        return {"message_type":"d_not_f"}

    # date wise count of a single attacker_ip
    search2 = opensearch_conn_using_db(f"SELECT rule_mitre_tactic,DATE_FORMAT(@timestamp,'%Y-%m-%d %H:%i:%s'),count(rule_mitre_tactic) count FROM {indice_name}-* WHERE rule_mitre_tactic IN {updated_tuple} and agent_id = {agent_id} AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY DATE_FORMAT(@timestamp,'%Y-%m-%d %H:%i:%s'),rule_mitre_tactic ORDER BY DATE_FORMAT(@timestamp,'%Y-%m-%d %H:%i:%s');", location_id, plan_id)

    # print("AttackerIPCount--datewise count of attacker ip:", search2)
    if search2.get("total") not in exclude_values:
        tactic_list, Dates, individual_tactic_counts = map(list, zip(*search2['datarows']))
        # removing redundant elements from list with dates
        unique_dates = list(dict.fromkeys(Dates))

        #I creating nested list:each mitre tactic clubbed with multiple dates, count, name in separate list
        # print(f"unique_tactics:{unique_tactics} and updated_tuple:{updated_tuple}")
        nested_outer_list = []
        for u in range(len(unique_tactics)):
            inner_list = []
            for i in range(len(search2['datarows'])):
                if unique_tactics[u] == search2['datarows'][i][0]:
                    inner_list.append(search2['datarows'][i])
            nested_outer_list.append(inner_list)
        # print(f"nested_outer_list:{nested_outer_list}")

        #II assigning [[mitre_name, count, date1],[mitre_name, count, date1]] to a global variable
        number_of_mitre_tactic = len(nested_outer_list)
        # print(f"number_of_IPs:{number_of_mitre_tactic}")
        for i in range(number_of_mitre_tactic):
            g['mitre_tactic_{0}'.format(i)] = nested_outer_list[i]

        #III creating global variables named g['mitre_tactic_{index}_count']
        no_of_dates = len(unique_dates)
        for j in range(number_of_mitre_tactic):
            g['mitre_tactic_{0}_count'.format(j)] = ['']*no_of_dates

        # IV appending count values in global variables g['mitre_tactic_{0}_count']
        for k in range(number_of_mitre_tactic):
            for i in range(len(g['mitre_tactic_{0}'.format(k)])):
                for j in range(len(unique_dates)):
                    if unique_dates[j] == g['mitre_tactic_{0}'.format(k)][i][1]:
                        g['mitre_tactic_{0}_count'.format(k)][j] = g['mitre_tactic_{0}'.format(k)][i][2]

        # # V appending 0 on dates where count is not present
        for k in range(number_of_mitre_tactic):
            for i in range(len(g['mitre_tactic_{0}_count'.format(k)])):
                if g['mitre_tactic_{0}_count'.format(k)][i] == "":
                    g['mitre_tactic_{0}_count'.format(k)][i] = 0
        nd = {}
        series =[]
        for k in range(number_of_mitre_tactic):
            mitre_name = {}
            mitre_name.update({"name": unique_tactics[k]})
            mitre_name.update({"data": g['mitre_tactic_{0}_count'.format(k)]})
            series.append(mitre_name)

        nd.update({"labels": unique_dates})
        nd.update({"series":series})
        return {"message_type":"data_found","data":nd}
    else:
        return {"message_type":"d_not_f"}

# -- 1.a. Mitre Alerts Evolution Over Time(line chart)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def hids_event_mitre_alert_evolution_over_time(request):

    parameters = pre_check_parameters(
        request, indice="hids_event_agent", type="line_chart"
    )
    if parameters.pop("error"):
        return Response(parameters)
    else:
        indice_name = parameters.get("indice_name")
        current_time = parameters.get("current_time")
        past_time = parameters.get("past_time")
        location_id = parameters.get("location_id")
        plan_id = parameters.get("plan_id")
        agent_id = parameters.get("agent_id")
        condition = parameters.get("condition")

    sql1 = f"SELECT rule_mitre_tactic,count(rule_mitre_tactic) count FROM {indice_name}-* WHERE rule_mitre_tactic IS NOT NULL and agent_id = {agent_id} AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY rule_mitre_tactic ORDER BY count desc LIMIT 7;"  
    
    search1 = opensearch_conn_using_db(sql1, location_id, plan_id)
    
    if search1.get("total") not in exclude_values:
        unique_tactics, tactic_count = map(list, zip(*search1['datarows']))
        unique_tactics_tuple = tuple(unique_tactics)
        updated_tuple = unique_tactics_tuple
        if len(unique_tactics_tuple) == 1:
            updated_tuple = unique_tactics_tuple+('0',)
    else:
        return Response({"message_type":"d_not_f"})

    # date wise count of a single tactic
    sql2 = f"SELECT rule_mitre_tactic, attack_epoch_time FROM {indice_name}-* WHERE rule_mitre_tactic IN {updated_tuple} and agent_id = {agent_id} AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} ORDER BY attack_epoch_time limit 500000;"
    
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
        for tactic_value in unique_tactics:
            filtered_dict = [dictionary for dictionary in table_query_list if dictionary.get('rule_mitre_tactic') == tactic_value]
            
            interval_counts = [0] * len(epoch_interval_group_list)  # Initialize count for each interval to 0

            for item in filtered_dict:
                epoch_date = item["attack_epoch_time"]
                for i,interval in enumerate(epoch_interval_group_list):
                    start, end = interval
                    if start <= epoch_date <= end:
                        interval_counts[i] += 1
                        # break  # No need to check further intervals
            ip_dict = {
                "name": tactic_value,
                "data": [None if count == 0 else count for count in interval_counts]
                
            }
            series.append(ip_dict)
        
    # unique agent_id, agent_ip, rule_mitre_tactic wise count
    SQL_query2 = f"SELECT agent_id, agent_ip, rule_mitre_tactic, count(agent_id) as rule_mitre_tactic_count from {indice_name}-* WHERE rule_mitre_tactic IN {updated_tuple} AND rule_mitre_tactic IS NOT NULL AND agent_id IS NOT NULL AND agent_ip IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY agent_id, agent_ip, rule_mitre_tactic;"

    search2 = opensearch_conn_using_db(SQL_query2, location_id, plan_id)

    if search2.get("total") not in exclude_values:
        # formatting sql2 query output as (key, value) pairs in dictionary
        key_names = [
            item["alias"] if (item["name"] == "count(agent_id)") else item["name"]
            for item in search2.get("schema")
        ]

        table_query_list = []
        for i, key_values in enumerate(search2.get("datarows")):
            Dict = {}
            Dict.update(dict(zip(key_names, key_values)))
            Dict["past_time"] = past_time
            Dict["current_time"] = current_time

            table_query_list.append(Dict)
        return Response(
            {
                "message_type": "data_found",
                "data": {"labels":new_lables, "series":series},
                "filter": table_query_list,
            }
        )
    else:
        return Response({"message_type":"d_not_f"})

# 1.b. Alert Groups Evolution(line chart) # view more
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def hids_event_mitre_alert_evolution_over_time_table(request):

    parameters = pre_check_parameters(
        request, indice="hids_event_agent", type="table", rule="rule_mitre_tactic"
    )
    if parameters.pop("error"):
        return Response(parameters)
    else:
        indice_name = parameters.get("indice_name")
        location_id = parameters.get("location_id")
        plan_id = parameters.get("plan_id")
        agent_id = parameters.get("agent_id")
        rule_mitre_tactic = parameters.get("rule_mitre_tactic")
        agent_ip = parameters.get("agent_ip")
        past_time = parameters.get("past_time")
        current_time = parameters.get("current_time")
    
    # sql query to get table data
    table_query = f"SELECT @timestamp, agent_name, agent_ip, agent_id, id, rule_level, rule_description, rule_id, rule_groups, rule_pci_dss, rule_gpg13, rule_gdpr, rule_hipaa, rule_mitre_id, rule_mitre_tactic, rule_mitre_technique FROM {indice_name}-* WHERE agent_id = {agent_id} AND agent_ip = '{agent_ip}' AND rule_mitre_tactic = '{rule_mitre_tactic}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) ORDER BY attack_epoch_time DESC limit 200000;"
    
    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)

    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
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

        return Response({"message_type":"success", "count":len(table_query_list), "rule_mitre_tactic":rule_mitre_tactic,"table":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})
    

# -- 4.a. Mitre Att&ck Tactics (bar chart)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def hids_event_mitre_attack_by_tactic(request):

    parameters = pre_check_parameters(
        request, indice="hids_event_agent", type="bar_chart"
    )
    if parameters.pop("error"):
        return Response(parameters)
    else:
        indice_name = parameters.get("indice_name")
        current_time = parameters.get("current_time")
        past_time = parameters.get("past_time")
        location_id = parameters.get("location_id")
        plan_id = parameters.get("plan_id")
        agent_id = parameters.get("agent_id")

    search1 = opensearch_conn_using_db(f"SELECT rule_mitre_tactic,count(rule_mitre_tactic) count FROM {indice_name}-* WHERE rule_mitre_tactic IS NOT NULL and agent_id = {agent_id} AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY rule_mitre_tactic ORDER BY count desc LIMIT 7;", location_id, plan_id)
    
    if search1.get("total") not in exclude_values:
            unique_tactics, list2 = map(list, zip(*search1['datarows']))
            attacker_ip_tuple = tuple(unique_tactics)
            updated_tuple = attacker_ip_tuple
            if len(attacker_ip_tuple) == 1:
                updated_tuple = attacker_ip_tuple+('0',)
    else:
            return Response({"message_type":"d_not_f"})

    # date wise count of a single attacker_ip
    search2 = opensearch_conn_using_db(f"SELECT rule_mitre_tactic,DATE_FORMAT(@timestamp,'%Y-%m-%d %H:%i:%s'),count(rule_mitre_tactic) count FROM {indice_name}-* WHERE rule_mitre_tactic IN {updated_tuple} and agent_id = {agent_id} AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY DATE_FORMAT(@timestamp,'%Y-%m-%d %H:%i:%s'),rule_mitre_tactic ORDER BY DATE_FORMAT(@timestamp,'%Y-%m-%d %H:%i:%s');", location_id, plan_id)

    # print("AttackerIPCount--datewise count of attacker ip:", search2)
    if search2.get("total") not in exclude_values:
        tactic_list, Dates, individual_tactic_counts = map(list, zip(*search2['datarows']))
        # removing redundant elements from list with dates
        unique_dates = list(dict.fromkeys(Dates))

        #I creating nested list:each mitre tactic clubbed with multiple dates, count, name in separate list
        
        nested_outer_list = []
        for u in range(len(unique_tactics)):
            inner_list = []
            for i in range(len(search2['datarows'])):
                if unique_tactics[u] == search2['datarows'][i][0]:
                    inner_list.append(search2['datarows'][i])
            nested_outer_list.append(inner_list)
        
        #II assigning [[mitre_name, count, date1],[mitre_name, count, date1]] to a global variable
        number_of_mitre_tactic = len(nested_outer_list)
        
        for i in range(number_of_mitre_tactic):
            g['mitre_tactic_{0}'.format(i)] = nested_outer_list[i]

        #III creating global variables named g['mitre_tactic_{index}_count']
        no_of_dates = len(unique_dates)
        for j in range(number_of_mitre_tactic):
            g['mitre_tactic_{0}_count'.format(j)] = ['']*no_of_dates

        # IV appending count values in global variables g['mitre_tactic_{0}_count']
        for k in range(number_of_mitre_tactic):
            for i in range(len(g['mitre_tactic_{0}'.format(k)])):
                for j in range(len(unique_dates)):
                    if unique_dates[j] == g['mitre_tactic_{0}'.format(k)][i][1]:
                        g['mitre_tactic_{0}_count'.format(k)][j] = g['mitre_tactic_{0}'.format(k)][i][2]

        # # V appending 0 on dates where count is not present
        for k in range(number_of_mitre_tactic):
            for i in range(len(g['mitre_tactic_{0}_count'.format(k)])):
                if g['mitre_tactic_{0}_count'.format(k)][i] == "":
                    g['mitre_tactic_{0}_count'.format(k)][i] = 0
        nd = {}
        series =[]
        for k in range(number_of_mitre_tactic):
            mitre_name = {}
            mitre_name.update({"name": unique_tactics[k]})
            mitre_name.update({"data": g['mitre_tactic_{0}_count'.format(k)]})
            series.append(mitre_name)

        nd.update({"labels": unique_dates})
        nd.update({"series":series})

    # unique agent_id, agent_ip, rule_mitre_tactic wise count
    SQL_query2 = f"SELECT agent_id, agent_ip, rule_mitre_tactic, count(agent_id) as rule_mitre_tactic_count from {indice_name}-* WHERE rule_mitre_tactic IN {updated_tuple} AND rule_mitre_tactic IS NOT NULL AND agent_id IS NOT NULL AND agent_ip IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY agent_id, agent_ip, rule_mitre_tactic;"

    search2 = opensearch_conn_using_db(SQL_query2, location_id, plan_id)

    if search2.get("total") not in exclude_values:
        # formatting sql2 query output as (key, value) pairs in dictionary
        key_names = [
            item["alias"] if (item["name"] == "count(agent_id)") else item["name"]
            for item in search2.get("schema")
        ]

        table_query_list = []
        for i, key_values in enumerate(search2.get("datarows")):
            Dict = {}
            Dict.update(dict(zip(key_names, key_values)))
            Dict["past_time"] = past_time
            Dict["current_time"] = current_time

            table_query_list.append(Dict)
        return Response(
            {
                "message_type": "data_found",
                "data": nd,
                "filter": table_query_list,
            })
        # return Response({"message_type":"data_found","data":nd})
    else:
        return Response({"message_type":"d_not_f"})
    

# 4.b. Mitre Att&ck Tactics (line chart) # view more
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def hids_event_mitre_attack_by_tactic_table(request):
    
    parameters = pre_check_parameters(
        request, indice="hids_event_agent", type="table", rule="rule_mitre_tactic"
    )
    if parameters.pop("error"):
        return Response(parameters)
    else:
        indice_name = parameters.get("indice_name")
        location_id = parameters.get("location_id")
        plan_id = parameters.get("plan_id")
        agent_id = parameters.get("agent_id")
        rule_mitre_tactic = parameters.get("rule_mitre_tactic")
        agent_ip = parameters.get("agent_ip")
        past_time = parameters.get("past_time")
        current_time = parameters.get("current_time")

    # sql query to get table data
    table_query = f"SELECT @timestamp, agent_name, agent_ip, agent_id, id, rule_level, rule_description, rule_id, rule_groups, rule_pci_dss, rule_gpg13, rule_gdpr, rule_hipaa, rule_mitre_id, rule_mitre_tactic, rule_mitre_technique FROM {indice_name}-* WHERE agent_id = {agent_id} AND agent_ip = '{agent_ip}' AND rule_mitre_tactic = '{rule_mitre_tactic}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) ORDER BY attack_epoch_time DESC limit 200000;"
    
    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)

    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
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

        return Response({"message_type":"success", "count":len(table_query_list), "rule_mitre_tactic":rule_mitre_tactic,"table":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})