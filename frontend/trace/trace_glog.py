#  ==============================================================================================================================
#  File Name: trace_glog.py
#  Description: It contains all the code for each chart on Trace Global Threat Feed page under Trace tab on Client Dashboard.
#  Active URL: https://xdr-demo.zerohack.in/trace/globalthreatfeed

#  ------------------------------------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  =============================================================================================================================

# This file contains all the charts of "Global Threat Feed" page of Trace
from rest_framework.response import Response
from ..helpers import getIndexNameByLocationId, getPlatformAndBlacklistedItemsByLocationId, getMlDlAccuracyRanges
from ..time_filter_on_queries import calculate_start_end_time
from ..grouping_epoch_time import *
from ..opensearch_config import opensearch_conn_using_db
from rest_framework.decorators import api_view
from rest_framework.response import Response
from collections import defaultdict
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

# 1.a Card Name: Malware Details (Pie chart on malware_details column)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trace_glog_malware_details_pie_chart(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('trace_global_agent')
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    sql = f"SELECT malware_detail, COUNT(malware_detail) FROM {indice_name}-* WHERE malware_detail IS NOT NULL AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) GROUP BY malware_detail ORDER BY COUNT(malware_detail) desc LIMIT 7;"
    
    run_sql_query = opensearch_conn_using_db(sql, location_id, plan_id)
    
    if run_sql_query.get("total") not in [0, None]:
        attacker_port, threat_count = map(list, zip(*run_sql_query['datarows']))
        bar_chart_dict = {"series": threat_count, "labels": attacker_port}

        time_dict = {"past_time":past_time, "current_time":current_time}

        return Response({"message_type":"success", "bar_chart":bar_chart_dict, "filter":time_dict})
    else:
        return Response({"message_type":"d_not_f"})

# 1.b Pie chart on malware_details column--Table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trace_glog_malware_details_pie_table(request):
    malware_name = request.GET.get('name')
    if malware_name is None:
        return Response({"message_type": "d_not_f", "errors": "name_not_found"})
    
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('trace_global_agent')
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    
    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT * FROM {indice_name}-* WHERE malware_detail = '{malware_name}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) ORDER BY attack_epoch_time DESC limit 200000;"
    
    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)
    
    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in [0, None]:
        key_names = [item['name'] for item in run_sql.get('schema')]
        
        table_query_list = []
        for i, row in enumerate(run_sql.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
            
        return Response({"message_type":"success", "count":len(table_query_list), "malware_detail":malware_name,"table":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 2.a Card Name: Intel Source (Pie chart on intel_source column)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trace_glog_intel_source_pie_chart(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('trace_global_agent')
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    sql = f"SELECT intel_source, COUNT(intel_source) FROM {indice_name}-* WHERE intel_source IS NOT NULL AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) GROUP BY intel_source ORDER BY COUNT(intel_source) desc LIMIT 7;"
    
    run_sql_query = opensearch_conn_using_db(sql, location_id, plan_id)
    
    if run_sql_query.get("total") not in [0, None]:
        attacker_port, threat_count = map(list, zip(*run_sql_query['datarows']))
        bar_chart_dict = {"series": threat_count, "labels": attacker_port}

        time_dict = {"past_time":past_time, "current_time":current_time}

        return Response({"message_type":"success", "bar_chart":bar_chart_dict, "filter":time_dict})
    else:
        return Response({"message_type":"d_not_f"})

# 2.b Pie chart on intel_source column--Table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trace_glog_intel_source_pie_table(request):
    intel_source_name = request.GET.get('name')
    if intel_source_name is None:
        return Response({"message_type": "d_not_f", "errors": "name_not_found"})
    
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('trace_global_agent')
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    
    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT * FROM {indice_name}-* WHERE intel_source = '{intel_source_name}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) ORDER BY attack_epoch_time DESC limit 200000;"
    
    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)
    
    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in [0, None]:
        key_names = [item['name'] for item in run_sql.get('schema')]
        
        table_query_list = []
        for i, row in enumerate(run_sql.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
            
        return Response({"message_type":"success", "count":len(table_query_list), "intel_source":intel_source_name,"table":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 3.a Card Name: Threat Type (Pie chart on threat_type column)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trace_glog_threat_type_pie_chart(request):
    condition = request.GET.get('condition')
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('trace_global_agent')
    
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})
    
    sql = f"SELECT threat_type, COUNT(threat_type) FROM {indice_name}-* WHERE threat_type IS NOT NULL AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) GROUP BY threat_type ORDER BY COUNT(threat_type) desc LIMIT 7;"
    
    run_sql_query = opensearch_conn_using_db(sql, location_id, plan_id)
    
    if run_sql_query.get("total") not in [0, None]:
        threat_type, threat_count = map(list, zip(*run_sql_query['datarows']))
        bar_chart_dict = {"series": threat_count, "labels": threat_type}

        time_dict = {"past_time":past_time, "current_time":current_time}

        return Response({"message_type":"success", "bar_chart":bar_chart_dict, "filter":time_dict})
    else:
        return Response({"message_type":"d_not_f"})

# 3.b Pie chart on threat_type column--Table
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trace_glog_threat_type_pie_table(request):
    threat_type = request.GET.get('name')
    if threat_type is None:
        return Response({"message_type": "name_not_found"})
    
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})
    
    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get('trace_global_agent')
    
    past_time = request.GET.get('past_time')
    current_time = request.GET.get('current_time')
    
    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})
    
    # sql query to get table data
    table_query = f"SELECT * FROM {indice_name}-* WHERE threat_type = '{threat_type}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) ORDER BY attack_epoch_time DESC limit 200000;"
    
    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)
    
    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in [0, None]:
        key_names = [item['name'] for item in run_sql.get('schema')]
        
        table_query_list = []
        for i, row in enumerate(run_sql.get('datarows')):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)
            
        return Response({"message_type":"success", "count":len(table_query_list), "malware_detail":threat_type,"table":table_query_list})
    else:
        return Response({"message_type":"d_not_f"})

# 4 Card Name: Global Threat Feed Logs (only Table)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trace_glog_logs_table(request):
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
    indice_name = index_name_dict.get('trace_global_agent')

    sql_query = f"SELECT * FROM {indice_name}-* WHERE attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} ORDER BY attack_epoch_time DESC limit 2000;"
    
    api_response = opensearch_conn_using_db(sql_query, location_id, plan_id)
    
    if api_response.get("total") not in [0,None]:
        key_names = [item['name'] for item in api_response.get('schema')]
        
        final_response = []
        for i in range(len(api_response.get('datarows'))):
            row = api_response.get('datarows')[i]
            final_response.append(dict(zip(key_names, row)))
        
        return Response({"message_type":"success", "data":final_response})
    else:
        return Response({"message_type":"d_not_f"})
    

