#  ================================================================================================================================================================================
#  File Name: wo_agent_id_wazuh_queries.py
#  Description: This file contains HIDS query cards which doesnt require a specific agent_id to be passed explicitly. Below mentioned cards find out column count for each agent_id

#  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  ================================================================================================================================================================================

from collections import defaultdict

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .grouping_epoch_time import *
from .helpers import getIndexNameByLocationId
from .opensearch_config import opensearch_conn_using_db
from .time_filter_on_queries import calculate_start_end_time

# list containing values to exclude from each query--> to avoid error on frontend page
exclude_values = [0, None]

# ################################ hids_alert_agent #start ####################################################################


# 1.a rule_mitre_tactic pie chart with table data (rule_mitre_tactic count in each agent_id) in filter # Card Name: Mitre Att&ck Tactics
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_alert_rule_mitre_pie_chart(request):
    condition = request.GET.get("condition")
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get("hids_alert_agent")
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})

    # unique rule_mitre_tactic count
    SQL_query1 = f"SELECT rule_mitre_tactic, count(rule_mitre_tactic) rule_mitre_tactic_count from {indice_name}-* WHERE rule_mitre_tactic IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} Group By rule_mitre_tactic ORDER BY rule_mitre_tactic_count DESC LIMIT 5;"

    search1 = opensearch_conn_using_db(SQL_query1, location_id, plan_id)

    if search1.get("total") not in exclude_values:
        unique_tactic, unique_tactic_count = map(list, zip(*search1["datarows"]))

        pie_chart_dict = {"series": unique_tactic_count, "labels": unique_tactic}

        str_unique_tactic = str(unique_tactic).strip("[]")
        unique_tactic_tuple = "({})".format(str_unique_tactic)
    else:
        return Response({"message_type": "d_not_f"})

    # in the total count of single agent_id calculating 'rule_mitre_tactic' wise count
    SQL_query2 = f"SELECT agent_id, agent_ip, rule_mitre_tactic, count(rule_mitre_tactic) rule_mitre_tactic_count from {indice_name}-* WHERE rule_mitre_tactic IN {unique_tactic_tuple} AND rule_mitre_tactic IS NOT NULL AND agent_id IS NOT NULL AND agent_ip IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY agent_id, agent_ip, rule_mitre_tactic LIMIT 200000;"

    search2 = opensearch_conn_using_db(SQL_query2, location_id, plan_id)

    if search2.get("total") not in exclude_values:
        # formatting sql2 query output as (key, value) pairs in dictionary
        key_names = [
            item["alias"]
            if (item["name"] == "count(rule_mitre_tactic)")
            else item["name"]
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
                "message_type": "success",
                "pie_chart": pie_chart_dict,
                "filter": table_query_list,
            }
        )
    else:
        return Response({"message_type": "d_not_f"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_alert_rule_mitre_pie_chart_testing(request):
    condition = request.GET.get("condition")
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get("hids_alert_agent")
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})

    # unique rule_mitre_tactic count
    SQL_query1 = f"SELECT rule_mitre_tactic, count(agent_id) rule_mitre_tactic_count from {indice_name}-* WHERE rule_mitre_tactic IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} Group By rule_mitre_tactic ORDER BY rule_mitre_tactic_count DESC LIMIT 5;"

    search1 = opensearch_conn_using_db(SQL_query1, location_id, plan_id)

    if search1.get("total") not in exclude_values:
        unique_tactic, unique_tactic_count = map(list, zip(*search1["datarows"]))

        pie_chart_dict = {"series": unique_tactic_count, "labels": unique_tactic}

        str_unique_tactic = str(unique_tactic).strip("[]")
        unique_tactic_tuple = "({})".format(str_unique_tactic)
    else:
        return Response({"message_type": "d_not_f"})

    # in the total count of single agent_id calculating 'rule_mitre_tactic' wise count
    SQL_query2 = f"SELECT agent_id, agent_ip, rule_mitre_tactic, count(agent_id) as rule_mitre_tactic_count from {indice_name}-* WHERE rule_mitre_tactic IN {unique_tactic_tuple} AND rule_mitre_tactic IS NOT NULL AND agent_id IS NOT NULL AND agent_ip IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY agent_id, agent_ip, rule_mitre_tactic;"

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
                "message_type": "success",
                "pie_chart": pie_chart_dict,
                "filter": table_query_list,
            }
        )
    else:
        return Response({"message_type": "d_not_f"})


# 1.b rule_mitre_tactic count table # Card Name: Mitre Att&ck Tactics (view more)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_alert_mitre_tactic_card_table(request):
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get("hids_alert_agent")
    agent_id = request.GET.get("name")

    if agent_id is None:
        return Response({"message_type": "d_not_f", "errors": "name_not_found"})

    rule_mitre_tactic = request.GET.get("name1")

    if rule_mitre_tactic is None:
        return Response({"message_type": "d_not_f", "errors": "name1_not_found"})

    agent_ip = request.GET.get("name2")

    if agent_ip is None:
        return Response({"message_type": "d_not_f", "errors": "name2_not_found"})

    past_time = request.GET.get("past_time")
    current_time = request.GET.get("current_time")

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})

    # sql query to get table data
    table_query = f"SELECT @timestamp, agent_name, agent_ip, agent_id, id, rule_level, rule_description, rule_id, rule_groups, rule_pci_dss, rule_gpg13, rule_gdpr, rule_hipaa, rule_mitre_id, rule_mitre_tactic, rule_mitre_technique FROM {indice_name}-* WHERE agent_id = {agent_id} AND agent_ip = '{agent_ip}' AND rule_mitre_tactic = '{rule_mitre_tactic}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) ORDER BY attack_epoch_time DESC limit 200000;"

    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)

    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [
            "timestamp" if (item["name"] == "@timestamp") else item["name"]
            for item in run_sql.get("schema")
        ]

        table_query_list = []
        for i, row in enumerate(run_sql.get("datarows")):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)

        for item in table_query_list:
            if "timestamp" in item:
                with_fractional_part = item.get("timestamp")
                item["timestamp"] = with_fractional_part.split(".")[0]

        return Response(
            {
                "message_type": "success",
                "agent_id": agent_id,
                "count": len(table_query_list),
                "table": table_query_list,
            }
        )
    else:
        return Response({"message_type": "d_not_f"})


# 2.a rule_mitre_technique pie chart with table data (rule_mitre_technique count in each agent_id) in filter # Card Name: Mitre Att&ck Techniques
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_alert_mitre_techniq_pie_chart(request):
    condition = request.GET.get("condition")
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get("hids_alert_agent")
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})

    # groupby query to get total unique count of 'rule_mitre_technique'
    SQL_query1 = f"SELECT rule_mitre_technique, count(rule_mitre_technique) rule_mitre_technique_count from {indice_name}-* WHERE rule_mitre_technique IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} Group By rule_mitre_technique ORDER BY rule_mitre_technique_count DESC LIMIT 5;"

    search1 = opensearch_conn_using_db(SQL_query1, location_id, plan_id)

    if search1.get("total") not in exclude_values:
        unique_technique, technique_count = map(list, zip(*search1["datarows"]))

        pie_chart_dict = {"series": technique_count, "labels": unique_technique}

        str_unique_technique = str(unique_technique).strip("[]")
        unique_technique_tuple = "({})".format(str_unique_technique)
    else:
        return Response({"message_type": "d_not_f"})

    # in the total count of single agent_id calculating 'rule_mitre_technique' wise count
    SQL_query2 = f"SELECT agent_id, agent_ip, rule_mitre_technique, count(rule_mitre_technique) rule_mitre_technique_count from {indice_name}-* WHERE rule_mitre_technique IN {unique_technique_tuple} AND rule_mitre_technique IS NOT NULL AND agent_id IS NOT NULL AND agent_ip IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY agent_id, agent_ip, rule_mitre_technique LIMIT 200000;"

    search2 = opensearch_conn_using_db(SQL_query2, location_id, plan_id)

    if search2.get("total") not in exclude_values:
        # formatting sql2 query output as (key, value) pairs in dictionary
        key_names = [
            item["alias"]
            if (item["name"] == "count(rule_mitre_technique)")
            else item["name"]
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
                "message_type": "success",
                "pie_chart": pie_chart_dict,
                "filter": table_query_list,
            }
        )
    else:
        return Response({"message_type": "d_not_f"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_alert_mitre_techniq_pie_chart_testing(request):
    condition = request.GET.get("condition")
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get("hids_alert_agent")
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})

    # groupby query to get total unique count of 'rule_mitre_technique'
    SQL_query1 = f"SELECT rule_mitre_technique, count(agent_id) rule_mitre_technique_count from {indice_name}-* WHERE rule_mitre_technique IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} Group By rule_mitre_technique ORDER BY rule_mitre_technique_count DESC LIMIT 5;"

    search1 = opensearch_conn_using_db(SQL_query1, location_id, plan_id)

    if search1.get("total") not in exclude_values:
        unique_technique, technique_count = map(list, zip(*search1["datarows"]))

        pie_chart_dict = {"series": technique_count, "labels": unique_technique}

        str_unique_technique = str(unique_technique).strip("[]")
        unique_technique_tuple = "({})".format(str_unique_technique)
    else:
        return Response({"message_type": "d_not_f"})

    # in the total count of single agent_id calculating 'rule_mitre_technique' wise count
    SQL_query2 = f"SELECT agent_id, agent_ip, rule_mitre_technique, count(agent_id) as rule_mitre_technique_count from {indice_name}-* WHERE rule_mitre_technique IN {unique_technique_tuple} AND rule_mitre_technique IS NOT NULL AND agent_id IS NOT NULL AND agent_ip IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY agent_id, agent_ip, rule_mitre_technique;"

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
                "message_type": "success",
                "pie_chart": pie_chart_dict,
                "filter": table_query_list,
            }
        )
    else:
        return Response({"message_type": "d_not_f"})


# 2.b rule_mitre_technique count table # Card Name: Mitre Att&ck Techniques (view more)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_alert_mitre_techniq_table(request):
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get("hids_alert_agent")
    agent_id = request.GET.get("name")

    if agent_id is None:
        return Response({"message_type": "d_not_f", "errors": "name_not_found"})

    rule_mitre_technique = request.GET.get("name1")

    if rule_mitre_technique is None:
        return Response({"message_type": "d_not_f", "errors": "name1_not_found"})

    agent_ip = request.GET.get("name2")

    if agent_ip is None:
        return Response({"message_type": "d_not_f", "errors": "name2_not_found"})

    past_time = request.GET.get("past_time")
    current_time = request.GET.get("current_time")

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})

    # sql query to get table data
    table_query = f"SELECT @timestamp, agent_name, agent_ip, agent_id, id, rule_level, rule_description, rule_id, rule_groups, rule_pci_dss, rule_gpg13, rule_gdpr, rule_hipaa, rule_mitre_id, rule_mitre_tactic, rule_mitre_technique FROM {indice_name}-* WHERE agent_id = {agent_id} AND agent_ip = '{agent_ip}' AND rule_mitre_technique = '{rule_mitre_technique}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) ORDER BY attack_epoch_time DESC limit 200000;"

    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)

    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [
            "timestamp" if (item["name"] == "@timestamp") else item["name"]
            for item in run_sql.get("schema")
        ]

        table_query_list = []
        for i, row in enumerate(run_sql.get("datarows")):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)

        for item in table_query_list:
            if "timestamp" in item:
                with_fractional_part = item.get("timestamp")
                item["timestamp"] = with_fractional_part.split(".")[0]

        return Response(
            {
                "message_type": "success",
                "count": len(table_query_list),
                "agent_id": agent_id,
                "table": table_query_list,
            }
        )
    else:
        return Response({"message_type": "d_not_f"})


# 3.a rule_pci_dss pie chart with table data (rule_pci_dss count in each agent_id) in filter # Card Name: PCI DSS
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_alert_rule_pci_dss_pie_chart(request):
    condition = request.GET.get("condition")
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get("hids_alert_agent")
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})

    # groupby query to get total unique count of 'rule_pci_dss'
    SQL_query1 = f"SELECT rule_pci_dss, count(rule_pci_dss) rule_pci_dss_count from {indice_name}-* WHERE rule_pci_dss IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} Group By rule_pci_dss ORDER BY rule_pci_dss_count DESC LIMIT 5;"

    search1 = opensearch_conn_using_db(SQL_query1, location_id, plan_id)

    if search1.get("total") not in exclude_values:
        unique_rule_pci_dss, rule_pci_dss_count = map(list, zip(*search1["datarows"]))

        pie_chart_dict = {"series": rule_pci_dss_count, "labels": unique_rule_pci_dss}

        str_unique_technique = str(unique_rule_pci_dss).strip("[]")
        unique_rule_pci_dss_tuple = "({})".format(str_unique_technique)

    else:
        return Response({"message_type": "d_not_f"})

    # in the total count of single agent_id calculating 'rule_pci_dss' wise count
    SQL_query2 = f"SELECT agent_id, agent_ip, rule_pci_dss, count(rule_pci_dss) rule_pci_dss_count from {indice_name}-* WHERE rule_pci_dss IN {unique_rule_pci_dss_tuple} AND rule_pci_dss IS NOT NULL AND agent_id IS NOT NULL AND agent_ip IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY agent_id, agent_ip, rule_pci_dss LIMIT 200000;"

    search2 = opensearch_conn_using_db(SQL_query2, location_id, plan_id)

    if search2.get("total") not in exclude_values:
        # formatting sql2 query output as (key, value) pairs in dictionary
        key_names = [
            item["alias"] if (item["name"] == "count(rule_pci_dss)") else item["name"]
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
                "message_type": "success",
                "pie_chart": pie_chart_dict,
                "filter_len": len(table_query_list),
                "filter": table_query_list,
            }
        )
    else:
        return Response({"message_type": "d_not_f"})


# 3.a rule_pci_dss pie chart with table data (rule_pci_dss count in each agent_id) in filter # Card Name: PCI DSS
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_alert_rule_pci_dss_pie_chart_testing(request):
    condition = request.GET.get("condition")
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get("hids_alert_agent")
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})

    # groupby query to get total unique count of 'rule_pci_dss'
    SQL_query1 = f"SELECT rule_pci_dss, count(agent_id) rule_pci_dss_count from {indice_name}-* WHERE rule_pci_dss IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} Group By rule_pci_dss ORDER BY rule_pci_dss_count DESC LIMIT 5;"
    search1 = opensearch_conn_using_db(SQL_query1, location_id, plan_id)

    if search1.get("total") not in exclude_values:
        unique_rule_pci_dss, rule_pci_dss_count = map(list, zip(*search1["datarows"]))

        pie_chart_dict = {"series": rule_pci_dss_count, "labels": unique_rule_pci_dss}

        str_unique_technique = str(unique_rule_pci_dss).strip("[]")
        unique_rule_pci_dss_tuple = "({})".format(str_unique_technique)

    else:
        return Response({"message_type": "d_not_f"})

    # in the total count of single agent_id calculating 'rule_pci_dss' wise count
    SQL_query2 = f"SELECT agent_id, agent_ip, rule_pci_dss, count(agent_id) as rule_pci_dss_count from {indice_name}-* WHERE rule_pci_dss IN {unique_rule_pci_dss_tuple} AND rule_pci_dss IS NOT NULL AND agent_id IS NOT NULL AND agent_ip IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY agent_id, agent_ip, rule_pci_dss;"

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
                "message_type": "success",
                "pie_chart": pie_chart_dict,
                "filter_len": len(table_query_list),
                "filter": table_query_list,
            }
        )
    else:
        return Response({"message_type": "d_not_f"})


# 3.b rule_pci_dss count table # Card Name: PCI DSS (view more)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_alert_rule_pci_dss_table(request):
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get("hids_alert_agent")
    agent_id = request.GET.get("name")

    if agent_id is None:
        return Response({"message_type": "d_not_f", "errors": "name_not_found"})

    rule_pci_dss = request.GET.get("name1")

    if rule_pci_dss is None:
        return Response({"message_type": "d_not_f", "errors": "name1_not_found"})

    agent_ip = request.GET.get("name2")

    if agent_ip is None:
        return Response({"message_type": "d_not_f", "errors": "name2_not_found"})

    past_time = request.GET.get("past_time")
    current_time = request.GET.get("current_time")

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})

    # sql query to get table data
    table_query = f"SELECT @timestamp, agent_name, agent_ip, agent_id, id, rule_level, rule_description, rule_id, rule_groups, rule_pci_dss, rule_gpg13, rule_gdpr, rule_hipaa, rule_mitre_id, rule_mitre_tactic, rule_mitre_technique FROM {indice_name}-* WHERE agent_id = {agent_id} AND agent_ip = '{agent_ip}' AND rule_pci_dss = '{rule_pci_dss}' AND agent_id IS NOT NULL AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) ORDER BY attack_epoch_time DESC limit 200000;"

    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)

    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [
            "timestamp" if (item["name"] == "@timestamp") else item["name"]
            for item in run_sql.get("schema")
        ]

        table_query_list = []
        for i, row in enumerate(run_sql.get("datarows")):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)

        for item in table_query_list:
            if "timestamp" in item:
                with_fractional_part = item.get("timestamp")
                item["timestamp"] = with_fractional_part.split(".")[0]

        return Response(
            {
                "message_type": "success",
                "count": len(table_query_list),
                "agent_id": agent_id,
                "table": table_query_list,
            }
        )
    else:
        return Response({"message_type": "d_not_f"})


# 4.a potential_ransomware_event count # Card Name: potential_ransomware_event
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_alert_potential_ransomware(request):
    condition = request.GET.get("condition")
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get("hids_alert_agent")

    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})

    sql_query = f"SELECT agent_id, agent_ip, count(potential_ransomware_event) FROM {indice_name}-* WHERE potential_ransomware_event = 'true' AND agent_id IS NOT NULL AND agent_ip IS NOT NULL AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) GROUP BY agent_id, agent_ip, potential_ransomware_event;"

    search1 = opensearch_conn_using_db(sql_query, location_id, plan_id)

    if search1.get("total") not in exclude_values:
        agent_id, agent_id, ransomeware_count = map(list, zip(*search1["datarows"]))
        total_ransomeware_count = sum(ransomeware_count)
        key_names = [
            "ransomware_count"
            if (item["name"] == "count(potential_ransomware_event)")
            else item["name"]
            for item in search1.get("schema")
        ]

        table_query_list = []
        for i, key_values in enumerate(search1.get("datarows")):
            Dict = {}
            Dict.update(dict(zip(key_names, key_values)))
            Dict["ransomware_value"] = "true"
            Dict["past_time"] = past_time
            Dict["current_time"] = current_time

            table_query_list.append(Dict)

        return Response(
            {
                "message_type": "success",
                "count": total_ransomeware_count,
                "filter": table_query_list,
            }
        )
    else:
        filter_list = [
            {
                "agent_id": 0,
                "agent_ip": 0,
                "ransomware_count": 0,
                "ransomware_value": "true",
                "past_time": past_time,
                "current_time": current_time,
            }
        ]
        return Response({"message_type": "success", "count": 0, "filter": filter_list})


# 4.b potential_ransomware_event table # Card Name: potential_ransomware_event (view more)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_alert_potential_ransomware_table(request):
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get("hids_alert_agent")
    ransomeware_count = request.GET.get("ransomware_count")

    if ransomeware_count is None:
        return Response(
            {"message_type": "d_not_f", "errors": "ransomeware_count_n_found"}
        )

    past_time = request.GET.get("past_time")
    current_time = request.GET.get("current_time")

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})

    agent_ip = request.GET.get("agent_ip")

    if agent_ip is None:
        return Response({"message_type": "d_not_f", "errors": "agent_ip_n_found"})

    agent_id = request.GET.get("agent_id")

    if agent_id is None:
        return Response({"message_type": "d_not_f", "errors": "agent_id_n_found"})

    # sql query to get table data
    table_query = f"SELECT @timestamp, agent_name, agent_ip, agent_id, id, rule_level, rule_description, rule_id, rule_groups, rule_pci_dss, rule_gpg13, rule_gdpr, rule_hipaa, rule_mitre_id, rule_mitre_tactic, rule_mitre_technique, syscheck_path FROM {indice_name}-* WHERE agent_id = {agent_id} AND agent_ip = '{agent_ip}' AND potential_ransomware_event = 'true' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) ORDER BY attack_epoch_time DESC limit {ransomeware_count};"

    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)

    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [
            "timestamp" if (item["name"] == "@timestamp") else item["name"]
            for item in run_sql.get("schema")
        ]

        table_query_list = []
        for i, row in enumerate(run_sql.get("datarows")):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)

        for item in table_query_list:
            if "timestamp" in item:
                with_fractional_part = item.get("timestamp")
                item["timestamp"] = with_fractional_part.split(".")[0]

        return Response(
            {
                "message_type": "success",
                "count": len(table_query_list),
                "table": table_query_list,
            }
        )
    else:
        return Response({"message_type": "d_not_f"})


# 5.a anomaly_label count # Card Name: anomaly_label
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_alert_anomaly_label(request):
    condition = request.GET.get("condition")
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get("hids_alert_agent")

    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})

    sql_query = f"SELECT agent_id, agent_ip, count(anomaly_label) FROM {indice_name}-* WHERE anomaly_label = 0 AND agent_id IS NOT NULL AND agent_ip IS NOT NULL AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) GROUP BY agent_id, agent_ip, anomaly_label;"

    search1 = opensearch_conn_using_db(sql_query, location_id, plan_id)

    if search1.get("total") not in exclude_values:
        agent_id, agent_id, anomaly_count = map(list, zip(*search1["datarows"]))
        total_anomaly_count = sum(anomaly_count)
        key_names = [
            "anomaly_label_count"
            if (item["name"] == "count(anomaly_label)")
            else item["name"]
            for item in search1.get("schema")
        ]

        table_query_list = []
        for i, key_values in enumerate(search1.get("datarows")):
            Dict = {}
            Dict.update(dict(zip(key_names, key_values)))
            Dict["anomaly_label_value"] = 0
            Dict["past_time"] = past_time
            Dict["current_time"] = current_time

            table_query_list.append(Dict)

        return Response(
            {
                "message_type": "success",
                "count": total_anomaly_count,
                "filter": table_query_list,
            }
        )
    else:
        filter_list = [
            {
                "agent_id": 0,
                "agent_ip": 0,
                "anomaly_label_count": 0,
                "anomaly_label_value": 0,
                "past_time": past_time,
                "current_time": current_time,
            }
        ]
        return Response({"message_type": "success", "count": 0, "filter": filter_list})


# 5.b anomaly_label table # Card Name: anomaly_label (view more)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_alert_anomaly_table(request):
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get("hids_alert_agent")
    ransomeware_count = request.GET.get("anomaly_label_count")

    if ransomeware_count is None:
        return Response(
            {"message_type": "d_not_f", "errors": "ransomeware_count_n_found"}
        )

    past_time = request.GET.get("past_time")
    current_time = request.GET.get("current_time")

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})

    agent_ip = request.GET.get("agent_ip")

    if agent_ip is None:
        return Response({"message_type": "d_not_f", "errors": "agent_ip_n_found"})

    agent_id = request.GET.get("agent_id")

    if agent_id is None:
        return Response({"message_type": "d_not_f", "errors": "agent_id_n_found"})

    # sql query to get table data
    table_query = f"SELECT @timestamp, agent_name, agent_ip, agent_id, id, rule_level, rule_description, rule_id, rule_groups, rule_pci_dss, rule_gpg13, rule_gdpr, rule_hipaa, rule_mitre_id, rule_mitre_tactic, rule_mitre_technique FROM {indice_name}-* WHERE agent_id = {agent_id} AND agent_ip = '{agent_ip}' AND anomaly_label = 0 AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) ORDER BY attack_epoch_time DESC limit {ransomeware_count};"

    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)

    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [
            "timestamp" if (item["name"] == "@timestamp") else item["name"]
            for item in run_sql.get("schema")
        ]

        table_query_list = []
        for i, row in enumerate(run_sql.get("datarows")):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)

        for item in table_query_list:
            if "timestamp" in item:
                with_fractional_part = item.get("timestamp")
                item["timestamp"] = with_fractional_part.split(".")[0]

        return Response(
            {
                "message_type": "success",
                "count": len(table_query_list),
                "table": table_query_list,
            }
        )
    else:
        return Response({"message_type": "d_not_f"})


# ################################ hids_alert_agent #end ####################################################################

# ################################ hids_event_agent #start ####################################################################


# 1.a rule_mitre_tactic pie chart with table data (rule_mitre_tactic count in each agent_id) in filter # Card Name: Mitre Att&ck Tactics
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_event_tactic_pie_chart(request):
    condition = request.GET.get("condition")
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get("hids_event_agent")
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})

    # unique rule_mitre_tactic count
    SQL_query1 = f"SELECT rule_mitre_tactic, count(rule_mitre_tactic) rule_mitre_tactic_count from {indice_name}-* WHERE rule_mitre_tactic IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} Group By rule_mitre_tactic ORDER BY rule_mitre_tactic_count DESC LIMIT 5;"

    search1 = opensearch_conn_using_db(SQL_query1, location_id, plan_id)

    if search1.get("total") not in exclude_values:
        unique_tactic, unique_tactic_count = map(list, zip(*search1["datarows"]))

        pie_chart_dict = {"series": unique_tactic_count, "labels": unique_tactic}

        str_unique_tactic = str(unique_tactic).strip("[]")
        unique_tactic_tuple = "({})".format(str_unique_tactic)
    else:
        return Response({"message_type": "d_not_f"})

    # in the total count of single agent_id calculating 'rule_mitre_tactic' wise count
    SQL_query2 = f"SELECT agent_id, agent_ip, rule_mitre_tactic, count(rule_mitre_tactic) rule_mitre_tactic_count from {indice_name}-* WHERE rule_mitre_tactic IN {unique_tactic_tuple} AND rule_mitre_tactic IS NOT NULL AND agent_id IS NOT NULL AND agent_ip IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY agent_id, agent_ip, rule_mitre_tactic LIMIT 200000;"

    search2 = opensearch_conn_using_db(SQL_query2, location_id, plan_id)

    if search2.get("total") not in exclude_values:
        # formatting sql2 query output as (key, value) pairs in dictionary
        key_names = [
            item["alias"]
            if (item["name"] == "count(rule_mitre_tactic)")
            else item["name"]
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
                "message_type": "success",
                "pie_chart": pie_chart_dict,
                "filter": table_query_list,
            }
        )
    else:
        return Response({"message_type": "d_not_f"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_event_tactic_pie_chart_testing(request):
    condition = request.GET.get("condition")
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get("hids_event_agent")
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})

    # unique rule_mitre_tactic count
    SQL_query1 = f"SELECT rule_mitre_tactic, count(agent_id) rule_mitre_tactic_count from {indice_name}-* WHERE rule_mitre_tactic IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} Group By rule_mitre_tactic ORDER BY rule_mitre_tactic_count DESC LIMIT 5;"

    search1 = opensearch_conn_using_db(SQL_query1, location_id, plan_id)

    if search1.get("total") not in exclude_values:
        unique_tactic, unique_tactic_count = map(list, zip(*search1["datarows"]))

        pie_chart_dict = {"series": unique_tactic_count, "labels": unique_tactic}

        str_unique_tactic = str(unique_tactic).strip("[]")
        unique_tactic_tuple = "({})".format(str_unique_tactic)
    else:
        return Response({"message_type": "d_not_f"})

    # in the total count of single agent_id calculating 'rule_mitre_tactic' wise count
    SQL_query2 = f"SELECT agent_id, agent_ip, rule_mitre_tactic, count(agent_id) as rule_mitre_tactic_count from {indice_name}-* WHERE rule_mitre_tactic IN {unique_tactic_tuple} AND rule_mitre_tactic IS NOT NULL AND agent_id IS NOT NULL AND agent_ip IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY agent_id, agent_ip, rule_mitre_tactic;"

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
                "message_type": "success",
                "pie_chart": pie_chart_dict,
                "filter": table_query_list,
            }
        )
    else:
        return Response({"message_type": "d_not_f"})


# 1.b rule_mitre_tactic count table # Card Name: Mitre Att&ck Tactics (view more)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_event_tactic_table(request):
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get("hids_event_agent")
    agent_id = request.GET.get("name")

    if agent_id is None:
        return Response({"message_type": "d_not_f", "errors": "name_not_found"})

    rule_mitre_tactic = request.GET.get("name1")

    if rule_mitre_tactic is None:
        return Response({"message_type": "d_not_f", "errors": "name1_not_found"})

    agent_ip = request.GET.get("name2")

    if agent_ip is None:
        return Response({"message_type": "d_not_f", "errors": "name2_not_found"})

    past_time = request.GET.get("past_time")
    current_time = request.GET.get("current_time")

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})

    # sql query to get table data
    table_query = f"SELECT @timestamp, agent_name, agent_ip, agent_id, id, rule_level, rule_description, rule_id, rule_groups, rule_pci_dss, rule_gpg13, rule_gdpr, rule_hipaa, rule_mitre_id, rule_mitre_tactic, rule_mitre_technique FROM {indice_name}-* WHERE agent_id = {agent_id} AND agent_ip = '{agent_ip}' AND rule_mitre_tactic = '{rule_mitre_tactic}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) ORDER BY attack_epoch_time DESC limit 200000;"

    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)

    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [
            "timestamp" if (item["name"] == "@timestamp") else item["name"]
            for item in run_sql.get("schema")
        ]

        table_query_list = []
        for i, row in enumerate(run_sql.get("datarows")):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)

        for item in table_query_list:
            if "timestamp" in item:
                with_fractional_part = item.get("timestamp")
                item["timestamp"] = with_fractional_part.split(".")[0]

        return Response(
            {
                "message_type": "success",
                "count": len(table_query_list),
                "agent_id": agent_id,
                "table": table_query_list,
            }
        )
    else:
        return Response({"message_type": "d_not_f"})


# 2.a rule_mitre_technique pie chart with table data (rule_mitre_technique count in each agent_id) in filter # Card Name: Mitre Att&ck Techniques (view more)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_event_techniq_pie_chart(request):
    condition = request.GET.get("condition")
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get("hids_event_agent")
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})

    # groupby query to get total unique count of 'rule_mitre_technique'
    SQL_query1 = f"SELECT rule_mitre_technique, count(rule_mitre_technique) rule_mitre_technique_count from {indice_name}-* WHERE rule_mitre_technique IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} Group By rule_mitre_technique ORDER BY rule_mitre_technique_count DESC LIMIT 5;"

    search1 = opensearch_conn_using_db(SQL_query1, location_id, plan_id)

    if search1.get("total") not in exclude_values:
        unique_technique, technique_count = map(list, zip(*search1["datarows"]))

        pie_chart_dict = {"series": technique_count, "labels": unique_technique}

        str_unique_technique = str(unique_technique).strip("[]")
        unique_technique_tuple = "({})".format(str_unique_technique)
    else:
        return Response({"message_type": "d_not_f"})

    # in the total count of single agent_id calculating 'rule_mitre_technique' wise count
    SQL_query2 = f"SELECT agent_id, agent_ip, rule_mitre_technique, count(rule_mitre_technique) rule_mitre_technique_count from {indice_name}-* WHERE rule_mitre_technique IN {unique_technique_tuple} AND rule_mitre_technique IS NOT NULL AND agent_id IS NOT NULL AND agent_ip IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY agent_id, agent_ip, rule_mitre_technique LIMIT 200000;"

    search2 = opensearch_conn_using_db(SQL_query2, location_id, plan_id)

    if search2.get("total") not in exclude_values:
        # formatting sql2 query output as (key, value) pairs in dictionary
        key_names = [
            item["alias"]
            if (item["name"] == "count(rule_mitre_technique)")
            else item["name"]
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
                "message_type": "success",
                "pie_chart": pie_chart_dict,
                "filter": table_query_list,
            }
        )
    else:
        return Response({"message_type": "d_not_f"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_event_techniq_pie_chart_testing(request):
    condition = request.GET.get("condition")
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get("hids_event_agent")
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})

    # groupby query to get total unique count of 'rule_mitre_technique'
    SQL_query1 = f"SELECT rule_mitre_technique, count(agent_id) rule_mitre_technique_count from {indice_name}-* WHERE rule_mitre_technique IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} Group By rule_mitre_technique ORDER BY rule_mitre_technique_count DESC LIMIT 5;"

    search1 = opensearch_conn_using_db(SQL_query1, location_id, plan_id)

    if search1.get("total") not in exclude_values:
        unique_technique, technique_count = map(list, zip(*search1["datarows"]))

        pie_chart_dict = {"series": technique_count, "labels": unique_technique}

        str_unique_technique = str(unique_technique).strip("[]")
        unique_technique_tuple = "({})".format(str_unique_technique)
    else:
        return Response({"message_type": "d_not_f"})

    # in the total count of single agent_id calculating 'rule_mitre_technique' wise count
    SQL_query2 = f"SELECT agent_id, agent_ip, rule_mitre_technique, count(agent_id) rule_mitre_technique_count from {indice_name}-* WHERE rule_mitre_technique IN {unique_technique_tuple} AND rule_mitre_technique IS NOT NULL AND agent_id IS NOT NULL AND agent_ip IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY agent_id, agent_ip, rule_mitre_technique;"

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
                "message_type": "success",
                "pie_chart": pie_chart_dict,
                "filter": table_query_list,
            }
        )
    else:
        return Response({"message_type": "d_not_f"})


# 2.b rule_mitre_technique count table # Card Name: Mitre Att&ck Techniques (view more)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_event_techniq_table(request):
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get("hids_event_agent")
    agent_id = request.GET.get("name")

    if agent_id is None:
        return Response({"message_type": "d_not_f", "errors": "name_not_found"})

    rule_mitre_technique = request.GET.get("name1")

    if rule_mitre_technique is None:
        return Response({"message_type": "d_not_f", "errors": "name1_not_found"})

    agent_ip = request.GET.get("name2")

    if agent_ip is None:
        return Response({"message_type": "d_not_f", "errors": "name2_not_found"})

    past_time = request.GET.get("past_time")
    current_time = request.GET.get("current_time")

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})

    # sql query to get table data
    table_query = f"SELECT @timestamp, agent_name, agent_ip, agent_id, id, rule_level, rule_description, rule_id, rule_groups, rule_pci_dss, rule_gpg13, rule_gdpr, rule_hipaa, rule_mitre_id, rule_mitre_tactic, rule_mitre_technique FROM {indice_name}-* WHERE agent_id = {agent_id} AND agent_ip = '{agent_ip}' AND rule_mitre_technique = '{rule_mitre_technique}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) ORDER BY attack_epoch_time DESC limit 200000;"

    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)

    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [
            "timestamp" if (item["name"] == "@timestamp") else item["name"]
            for item in run_sql.get("schema")
        ]

        table_query_list = []
        for i, row in enumerate(run_sql.get("datarows")):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)

        for item in table_query_list:
            if "timestamp" in item:
                with_fractional_part = item.get("timestamp")
                item["timestamp"] = with_fractional_part.split(".")[0]

        return Response(
            {
                "message_type": "success",
                "count": len(table_query_list),
                "agent_id": agent_id,
                "table": table_query_list,
            }
        )
    else:
        return Response({"message_type": "d_not_f"})


# 3.a rule_pci_dss pie chart with table data (rule_pci_dss count in each agent_id) in filter # Card Name: PCI DSS
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_event_pci_dss_pie_chart(request):
    condition = request.GET.get("condition")
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get("hids_event_agent")
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})

    # groupby query to get total unique count of 'rule_pci_dss'
    SQL_query1 = f"SELECT rule_pci_dss, count(rule_pci_dss) rule_pci_dss_count from {indice_name}-* WHERE rule_pci_dss IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} Group By rule_pci_dss ORDER BY rule_pci_dss_count DESC LIMIT 5;"

    search1 = opensearch_conn_using_db(SQL_query1, location_id, plan_id)

    if search1.get("total") not in exclude_values:
        unique_rule_pci_dss, rule_pci_dss_count = map(list, zip(*search1["datarows"]))

        pie_chart_dict = {"series": rule_pci_dss_count, "labels": unique_rule_pci_dss}

        str_unique_technique = str(unique_rule_pci_dss).strip("[]")
        unique_rule_pci_dss_tuple = "({})".format(str_unique_technique)

    else:
        return Response({"message_type": "d_not_f"})

    # in the total count of single agent_id calculating 'rule_pci_dss' wise count
    SQL_query2 = f"SELECT agent_id, agent_ip, rule_pci_dss, count(rule_pci_dss) rule_pci_dss_count from {indice_name}-* WHERE rule_pci_dss IN {unique_rule_pci_dss_tuple} AND rule_pci_dss IS NOT NULL AND agent_id IS NOT NULL AND agent_ip IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY agent_id, agent_ip, rule_pci_dss LIMIT 200000;"

    search2 = opensearch_conn_using_db(SQL_query2, location_id, plan_id)

    if search2.get("total") not in exclude_values:
        # formatting sql2 query output as (key, value) pairs in dictionary
        key_names = [
            item["alias"] if (item["name"] == "count(rule_pci_dss)") else item["name"]
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
                "message_type": "success",
                "pie_chart": pie_chart_dict,
                "filter": table_query_list,
            }
        )
    else:
        return Response({"message_type": "d_not_f"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_event_pci_dss_pie_chart_testing(request):
    condition = request.GET.get("condition")
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get("hids_event_agent")
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})

    # groupby query to get total unique count of 'rule_pci_dss'
    SQL_query1 = f"SELECT rule_pci_dss, count(agent_id) rule_pci_dss_count from {indice_name}-* WHERE rule_pci_dss IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} Group By rule_pci_dss ORDER BY rule_pci_dss_count DESC LIMIT 5;"

    search1 = opensearch_conn_using_db(SQL_query1, location_id, plan_id)

    if search1.get("total") not in exclude_values:
        unique_rule_pci_dss, rule_pci_dss_count = map(list, zip(*search1["datarows"]))

        pie_chart_dict = {"series": rule_pci_dss_count, "labels": unique_rule_pci_dss}

        str_unique_technique = str(unique_rule_pci_dss).strip("[]")
        unique_rule_pci_dss_tuple = "({})".format(str_unique_technique)

    else:
        return Response({"message_type": "d_not_f"})

    # in the total count of single agent_id calculating 'rule_pci_dss' wise count
    SQL_query2 = f"SELECT agent_id, agent_ip, rule_pci_dss, count(agent_id) as rule_pci_dss_count from {indice_name}-* WHERE rule_pci_dss IN {unique_rule_pci_dss_tuple} AND rule_pci_dss IS NOT NULL AND agent_id IS NOT NULL AND agent_ip IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY agent_id, agent_ip, rule_pci_dss;"

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
                "message_type": "success",
                "pie_chart": pie_chart_dict,
                "filter": table_query_list,
            }
        )
    else:
        return Response({"message_type": "d_not_f"})


# 3.b rule_pci_dss count table # Card Name: PCI DSS (view more)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_event_pci_dss_table(request):
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get("hids_event_agent")
    agent_id = request.GET.get("name")

    if agent_id is None:
        return Response({"message_type": "d_not_f", "errors": "name_not_found"})

    rule_pci_dss = request.GET.get("name1")

    if rule_pci_dss is None:
        return Response({"message_type": "d_not_f", "errors": "name1_not_found"})

    agent_ip = request.GET.get("name2")

    if agent_ip is None:
        return Response({"message_type": "d_not_f", "errors": "name2_not_found"})

    past_time = request.GET.get("past_time")
    current_time = request.GET.get("current_time")

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})

    # sql query to get table data
    table_query = f"SELECT @timestamp, agent_name, agent_ip, agent_id, id, rule_level, rule_description, rule_id, rule_groups, rule_pci_dss, rule_gpg13, rule_gdpr, rule_hipaa, rule_mitre_id, rule_mitre_tactic, rule_mitre_technique FROM {indice_name}-* WHERE agent_id = {agent_id} AND agent_ip = '{agent_ip}' AND rule_pci_dss = '{rule_pci_dss}' AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} ORDER BY attack_epoch_time DESC limit 200000;"

    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)

    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [
            "timestamp" if (item["name"] == "@timestamp") else item["name"]
            for item in run_sql.get("schema")
        ]

        table_query_list = []
        for i, row in enumerate(run_sql.get("datarows")):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)

        for item in table_query_list:
            if "timestamp" in item:
                with_fractional_part = item.get("timestamp")
                item["timestamp"] = with_fractional_part.split(".")[0]

        return Response(
            {
                "message_type": "success",
                "count": len(table_query_list),
                "agent_id": agent_id,
                "table": table_query_list,
            }
        )
    else:
        return Response({"message_type": "d_not_f"})


# 4.a potential_ransomware_event count # Card Name: potential_ransomware_event
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_event_potential_ransomware(request):
    condition = request.GET.get("condition")
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get("hids_event_agent")

    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})

    sql_query = f"SELECT agent_id, agent_ip, count(potential_ransomware_event) FROM {indice_name}-* WHERE potential_ransomware_event = 'true' AND agent_id IS NOT NULL AND agent_ip IS NOT NULL AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) GROUP BY agent_id, agent_ip, potential_ransomware_event;"

    search1 = opensearch_conn_using_db(sql_query, location_id, plan_id)

    if search1.get("total") not in exclude_values:
        agent_id, agent_id, ransomeware_count = map(list, zip(*search1["datarows"]))
        total_ransomeware_count = sum(ransomeware_count)
        key_names = [
            "ransomware_count"
            if (item["name"] == "count(potential_ransomware_event)")
            else item["name"]
            for item in search1.get("schema")
        ]

        table_query_list = []
        for i, key_values in enumerate(search1.get("datarows")):
            Dict = {}
            Dict.update(dict(zip(key_names, key_values)))
            Dict["ransomware_value"] = "true"
            Dict["past_time"] = past_time
            Dict["current_time"] = current_time

            table_query_list.append(Dict)

        return Response(
            {
                "message_type": "success",
                "count": total_ransomeware_count,
                "filter": table_query_list,
            }
        )
    else:
        filter_list = [
            {
                "agent_id": 0,
                "agent_ip": 0,
                "ransomware_count": 0,
                "ransomware_value": "true",
                "past_time": past_time,
                "current_time": current_time,
            }
        ]
        return Response({"message_type": "success", "count": 0, "filter": filter_list})


# 4.b potential_ransomware_event table # Card Name: potential_ransomware_event (view more)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_event_potential_ransomware_table(request):
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get("hids_event_agent")
    ransomeware_count = request.GET.get("ransomware_count")

    if ransomeware_count is None:
        return Response(
            {"message_type": "d_not_f", "errors": "ransomeware_count_n_found"}
        )

    past_time = request.GET.get("past_time")
    current_time = request.GET.get("current_time")

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})

    agent_ip = request.GET.get("agent_ip")

    if agent_ip is None:
        return Response({"message_type": "d_not_f", "errors": "agent_ip_n_found"})

    agent_id = request.GET.get("agent_id")

    if agent_id is None:
        return Response({"message_type": "d_not_f", "errors": "agent_id_n_found"})

    # sql query to get table data
    table_query = f"SELECT @timestamp, agent_name, agent_ip, agent_id, id, rule_level, rule_description, rule_id, rule_groups, rule_pci_dss, rule_gpg13, rule_gdpr, rule_hipaa, rule_mitre_id, rule_mitre_tactic, rule_mitre_technique, syscheck_path FROM {indice_name}-* WHERE agent_id = {agent_id} AND agent_ip = '{agent_ip}' AND potential_ransomware_event = 'true' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) ORDER BY attack_epoch_time DESC limit {ransomeware_count};"

    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)

    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [
            "timestamp" if (item["name"] == "@timestamp") else item["name"]
            for item in run_sql.get("schema")
        ]

        table_query_list = []
        for i, row in enumerate(run_sql.get("datarows")):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)

        for item in table_query_list:
            if "timestamp" in item:
                with_fractional_part = item.get("timestamp")
                item["timestamp"] = with_fractional_part.split(".")[0]

        return Response(
            {
                "message_type": "success",
                "count": len(table_query_list),
                "table": table_query_list,
            }
        )
    else:
        return Response({"message_type": "d_not_f"})


# 5.a anomaly_label count # Card Name: anomaly_label
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_event_anomaly_label(request):
    condition = request.GET.get("condition")
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get("hids_event_agent")

    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})

    sql_query = f"SELECT agent_id, agent_ip, count(anomaly_label) FROM {indice_name}-* WHERE anomaly_label = 0 AND agent_id IS NOT NULL AND agent_ip IS NOT NULL AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) GROUP BY agent_id, agent_ip, anomaly_label;"

    search1 = opensearch_conn_using_db(sql_query, location_id, plan_id)

    if search1.get("total") not in exclude_values:
        agent_id, agent_id, anomaly_count = map(list, zip(*search1["datarows"]))
        total_anomaly_count = sum(anomaly_count)
        key_names = [
            "anomaly_label_count"
            if (item["name"] == "count(anomaly_label)")
            else item["name"]
            for item in search1.get("schema")
        ]

        table_query_list = []
        for i, key_values in enumerate(search1.get("datarows")):
            Dict = {}
            Dict.update(dict(zip(key_names, key_values)))
            Dict["anomaly_label_value"] = 0
            Dict["past_time"] = past_time
            Dict["current_time"] = current_time

            table_query_list.append(Dict)

        return Response(
            {
                "message_type": "success",
                "count": total_anomaly_count,
                "filter": table_query_list,
            }
        )
    else:
        filter_list = [
            {
                "agent_id": 0,
                "agent_ip": 0,
                "anomaly_label_count": 0,
                "anomaly_label_value": 0,
                "past_time": past_time,
                "current_time": current_time,
            }
        ]

        return Response({"message_type": "success", "count": 0, "filter": filter_list})


# 5.b anomaly_label table # Card Name: anomaly_label (view more)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_event_anomaly_table(request):
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get("hids_event_agent")
    ransomeware_count = request.GET.get("anomaly_label_count")

    if ransomeware_count is None:
        return Response(
            {"message_type": "d_not_f", "errors": "ransomeware_count_n_found"}
        )

    past_time = request.GET.get("past_time")
    current_time = request.GET.get("current_time")

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})

    agent_ip = request.GET.get("agent_ip")

    if agent_ip is None:
        return Response({"message_type": "d_not_f", "errors": "agent_ip_n_found"})

    agent_id = request.GET.get("agent_id")

    if agent_id is None:
        return Response({"message_type": "d_not_f", "errors": "agent_id_n_found"})

    # sql query to get table data
    table_query = f"SELECT @timestamp, agent_name, agent_ip, agent_id, id, rule_level, rule_description, rule_id, rule_groups, rule_pci_dss, rule_gpg13, rule_gdpr, rule_hipaa, rule_mitre_id, rule_mitre_tactic, rule_mitre_technique FROM {indice_name}-* WHERE agent_id = {agent_id} AND agent_ip = '{agent_ip}' AND anomaly_label = 0 AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) ORDER BY attack_epoch_time DESC limit {ransomeware_count};"

    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)

    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [
            "timestamp" if (item["name"] == "@timestamp") else item["name"]
            for item in run_sql.get("schema")
        ]

        table_query_list = []
        for i, row in enumerate(run_sql.get("datarows")):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)

        for item in table_query_list:
            if "timestamp" in item:
                with_fractional_part = item.get("timestamp")
                item["timestamp"] = with_fractional_part.split(".")[0]

        return Response(
            {
                "message_type": "success",
                "count": len(table_query_list),
                "table": table_query_list,
            }
        )
    else:
        return Response({"message_type": "d_not_f"})


# ################################ hids_event_agent #end ####################################################################


# ################################ hids_incident_agent #start ####################################################################


# 1.a rule_mitre_tactic pie chart with table data (rule_mitre_tactic count in each agent_id) in filter # Card Name: Mitre Att&ck Tactics
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_incident_tactic_pie_chart(request):
    condition = request.GET.get("condition")
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get("hids_incident_agent")
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})

    # unique rule_mitre_tactic count
    SQL_query1 = f"SELECT rule_mitre_tactic, count(rule_mitre_tactic) rule_mitre_tactic_count from {indice_name}-* WHERE rule_mitre_tactic IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} Group By rule_mitre_tactic ORDER BY rule_mitre_tactic_count DESC LIMIT 5;"

    search1 = opensearch_conn_using_db(SQL_query1, location_id, plan_id)

    if search1.get("total") not in exclude_values:
        unique_tactic, unique_tactic_count = map(list, zip(*search1["datarows"]))

        pie_chart_dict = {"series": unique_tactic_count, "labels": unique_tactic}

        str_unique_tactic = str(unique_tactic).strip("[]")
        unique_tactic_tuple = "({})".format(str_unique_tactic)
    else:
        return Response({"message_type": "d_not_f"})

    # in the total count of single agent_id calculating 'rule_mitre_tactic' wise count
    SQL_query2 = f"SELECT agent_id, agent_ip, rule_mitre_tactic, count(rule_mitre_tactic) rule_mitre_tactic_count from {indice_name}-* WHERE rule_mitre_tactic IN {unique_tactic_tuple} AND rule_mitre_tactic IS NOT NULL AND agent_id IS NOT NULL AND agent_ip IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY agent_id, agent_ip, rule_mitre_tactic LIMIT 200000;"

    search2 = opensearch_conn_using_db(SQL_query2, location_id, plan_id)

    if search2.get("total") not in exclude_values:
        # formatting sql2 query output as (key, value) pairs in dictionary
        key_names = [
            item["alias"]
            if (item["name"] == "count(rule_mitre_tactic)")
            else item["name"]
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
                "message_type": "success",
                "pie_chart": pie_chart_dict,
                "filter": table_query_list,
            }
        )
    else:
        return Response({"message_type": "d_not_f"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_incident_tactic_pie_chart_testing(request):
    condition = request.GET.get("condition")
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get("hids_incident_agent")
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})

    # unique rule_mitre_tactic count
    SQL_query1 = f"SELECT rule_mitre_tactic, count(agent_id) rule_mitre_tactic_count from {indice_name}-* WHERE rule_mitre_tactic IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} Group By rule_mitre_tactic ORDER BY rule_mitre_tactic_count DESC LIMIT 5;"

    search1 = opensearch_conn_using_db(SQL_query1, location_id, plan_id)

    if search1.get("total") not in exclude_values:
        unique_tactic, unique_tactic_count = map(list, zip(*search1["datarows"]))

        pie_chart_dict = {"series": unique_tactic_count, "labels": unique_tactic}

        str_unique_tactic = str(unique_tactic).strip("[]")
        unique_tactic_tuple = "({})".format(str_unique_tactic)
    else:
        return Response({"message_type": "d_not_f"})

    # in the total count of single agent_id calculating 'rule_mitre_tactic' wise count
    SQL_query2 = f"SELECT agent_id, agent_ip, rule_mitre_tactic, count(agent_id) as rule_mitre_tactic_count from {indice_name}-* WHERE rule_mitre_tactic IN {unique_tactic_tuple} AND rule_mitre_tactic IS NOT NULL AND agent_id IS NOT NULL AND agent_ip IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY agent_id, agent_ip, rule_mitre_tactic;"

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
                "message_type": "success",
                "pie_chart": pie_chart_dict,
                "filter": table_query_list,
            }
        )
    else:
        return Response({"message_type": "d_not_f"})


# 1.b rule_mitre_tactic count table # Card Name: Mitre Att&ck Tactics (view more)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_incident_tactic_table(request):
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get("hids_incident_agent")
    agent_id = request.GET.get("name")

    if agent_id is None:
        return Response({"message_type": "d_not_f", "errors": "name_not_found"})

    rule_mitre_tactic = request.GET.get("name1")

    if rule_mitre_tactic is None:
        return Response({"message_type": "d_not_f", "errors": "name1_not_found"})

    agent_ip = request.GET.get("name2")

    if agent_ip is None:
        return Response({"message_type": "d_not_f", "errors": "name2_not_found"})

    past_time = request.GET.get("past_time")
    current_time = request.GET.get("current_time")

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})

    # sql query to get table data
    table_query = f"SELECT @timestamp, agent_name, agent_ip, agent_id, id, rule_level, rule_description, rule_id, rule_groups, rule_pci_dss, rule_gpg13, rule_gdpr, rule_mitre_id, rule_mitre_tactic, rule_mitre_technique FROM {indice_name}-* WHERE agent_id = {agent_id} AND agent_ip = '{agent_ip}' AND rule_mitre_tactic = '{rule_mitre_tactic}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) ORDER BY attack_epoch_time DESC limit 200000;"

    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)

    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [
            "timestamp" if (item["name"] == "@timestamp") else item["name"]
            for item in run_sql.get("schema")
        ]

        table_query_list = []
        for i, row in enumerate(run_sql.get("datarows")):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)

        for item in table_query_list:
            if "timestamp" in item:
                with_fractional_part = item.get("timestamp")
                item["timestamp"] = with_fractional_part.split(".")[0]

        return Response(
            {
                "message_type": "success",
                "count": len(table_query_list),
                "agent_id": agent_id,
                "table": table_query_list,
            }
        )
    else:
        return Response({"message_type": "d_not_f"})


# 2.a rule_mitre_technique pie chart with table data (rule_mitre_technique count in each agent_id) in filter # Card Name: Mitre Att&ck Techniques
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_incident_techniq_pie_chart(request):
    condition = request.GET.get("condition")
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get("hids_incident_agent")
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})

    # groupby query to get total unique count of 'rule_mitre_technique'
    SQL_query1 = f"SELECT rule_mitre_technique, count(rule_mitre_technique) rule_mitre_technique_count from {indice_name}-* WHERE rule_mitre_technique IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} Group By rule_mitre_technique ORDER BY rule_mitre_technique_count DESC LIMIT 5;"

    search1 = opensearch_conn_using_db(SQL_query1, location_id, plan_id)

    if search1.get("total") not in exclude_values:
        unique_technique, technique_count = map(list, zip(*search1["datarows"]))

        pie_chart_dict = {"series": technique_count, "labels": unique_technique}

        str_unique_technique = str(unique_technique).strip("[]")
        unique_technique_tuple = "({})".format(str_unique_technique)
    else:
        return Response({"message_type": "d_not_f"})

    # in the total count of single agent_id calculating 'rule_mitre_technique' wise count
    SQL_query2 = f"SELECT agent_id, agent_ip, rule_mitre_technique, count(rule_mitre_technique) rule_mitre_technique_count from {indice_name}-* WHERE rule_mitre_technique IN {unique_technique_tuple} AND rule_mitre_technique IS NOT NULL AND agent_id IS NOT NULL AND agent_ip IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY agent_id, agent_ip, rule_mitre_technique LIMIT 200000;"

    search2 = opensearch_conn_using_db(SQL_query2, location_id, plan_id)

    if search2.get("total") not in exclude_values:
        # formatting sql2 query output as (key, value) pairs in dictionary
        key_names = [
            item["alias"]
            if (item["name"] == "count(rule_mitre_technique)")
            else item["name"]
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
                "message_type": "success",
                "pie_chart": pie_chart_dict,
                "filter": table_query_list,
            }
        )
    else:
        return Response({"message_type": "d_not_f"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_incident_techniq_pie_chart_testing(request):
    condition = request.GET.get("condition")
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get("hids_incident_agent")
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})

    # groupby query to get total unique count of 'rule_mitre_technique'
    SQL_query1 = f"SELECT rule_mitre_technique, count(agent_id) rule_mitre_technique_count from {indice_name}-* WHERE rule_mitre_technique IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} Group By rule_mitre_technique ORDER BY rule_mitre_technique_count DESC LIMIT 5;"

    search1 = opensearch_conn_using_db(SQL_query1, location_id, plan_id)

    if search1.get("total") not in exclude_values:
        unique_technique, technique_count = map(list, zip(*search1["datarows"]))

        pie_chart_dict = {"series": technique_count, "labels": unique_technique}

        str_unique_technique = str(unique_technique).strip("[]")
        unique_technique_tuple = "({})".format(str_unique_technique)
    else:
        return Response({"message_type": "d_not_f"})

    # in the total count of single agent_id calculating 'rule_mitre_technique' wise count
    SQL_query2 = f"SELECT agent_id, agent_ip, rule_mitre_technique, count(agent_id) as rule_mitre_technique_count from {indice_name}-* WHERE rule_mitre_technique IN {unique_technique_tuple} AND rule_mitre_technique IS NOT NULL AND agent_id IS NOT NULL AND agent_ip IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY agent_id, agent_ip, rule_mitre_technique;"

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
                "message_type": "success",
                "pie_chart": pie_chart_dict,
                "filter": table_query_list,
            }
        )
    else:
        return Response({"message_type": "d_not_f"})


# 2.b rule_mitre_technique count table # Card Name: Mitre Att&ck Techniques (view more)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_incident_techniq_table(request):
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get("hids_incident_agent")
    agent_id = request.GET.get("name")

    if agent_id is None:
        return Response({"message_type": "d_not_f", "errors": "name_not_found"})

    rule_mitre_technique = request.GET.get("name1")

    if rule_mitre_technique is None:
        return Response({"message_type": "d_not_f", "errors": "name1_not_found"})

    agent_ip = request.GET.get("name2")

    if agent_ip is None:
        return Response({"message_type": "d_not_f", "errors": "name2_not_found"})

    past_time = request.GET.get("past_time")
    current_time = request.GET.get("current_time")

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})

    # sql query to get table data
    table_query = f"SELECT @timestamp, agent_name, agent_ip, agent_id, id, rule_level, rule_description, rule_id, rule_groups, rule_pci_dss, rule_gpg13, rule_gdpr, rule_mitre_id, rule_mitre_tactic, rule_mitre_technique FROM {indice_name}-* WHERE agent_id = {agent_id} AND agent_ip = '{agent_ip}' AND rule_mitre_technique = '{rule_mitre_technique}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) ORDER BY attack_epoch_time DESC limit 200000;"

    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)

    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [
            "timestamp" if (item["name"] == "@timestamp") else item["name"]
            for item in run_sql.get("schema")
        ]

        table_query_list = []
        for i, row in enumerate(run_sql.get("datarows")):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)

        for item in table_query_list:
            if "timestamp" in item:
                with_fractional_part = item.get("timestamp")
                item["timestamp"] = with_fractional_part.split(".")[0]

        return Response(
            {
                "message_type": "success",
                "count": len(table_query_list),
                "agent_id": agent_id,
                "table": table_query_list,
            }
        )
    else:
        return Response({"message_type": "d_not_f"})


# 3.a rule_pci_dss pie chart with table data (rule_pci_dss count in each agent_id) in filter # Card Name: PCI DSS
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_incident_pci_dss_pie_chart(request):
    condition = request.GET.get("condition")
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get("hids_incident_agent")
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})

    # groupby query to get total unique count of 'rule_pci_dss'
    SQL_query1 = f"SELECT rule_pci_dss, count(rule_pci_dss) rule_pci_dss_count from {indice_name}-* WHERE rule_pci_dss IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} Group By rule_pci_dss ORDER BY rule_pci_dss_count DESC LIMIT 5;"

    search1 = opensearch_conn_using_db(SQL_query1, location_id, plan_id)

    if search1.get("total") not in exclude_values:
        unique_rule_pci_dss, rule_pci_dss_count = map(list, zip(*search1["datarows"]))

        pie_chart_dict = {"series": rule_pci_dss_count, "labels": unique_rule_pci_dss}

        str_unique_technique = str(unique_rule_pci_dss).strip("[]")
        unique_rule_pci_dss_tuple = "({})".format(str_unique_technique)

    else:
        return Response({"message_type": "d_not_f"})

    # in the total count of single agent_id calculating 'rule_pci_dss' wise count
    SQL_query2 = f"SELECT agent_id, agent_ip, rule_pci_dss, count(rule_pci_dss) rule_pci_dss_count from {indice_name}-* WHERE rule_pci_dss IN {unique_rule_pci_dss_tuple} AND rule_pci_dss IS NOT NULL AND agent_id IS NOT NULL AND agent_ip IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY agent_id, agent_ip, rule_pci_dss LIMIT 200000;"

    search2 = opensearch_conn_using_db(SQL_query2, location_id, plan_id)

    if search2.get("total") not in exclude_values:
        # formatting sql2 query output as (key, value) pairs in dictionary
        key_names = [
            item["alias"] if (item["name"] == "count(rule_pci_dss)") else item["name"]
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
                "message_type": "success",
                "pie_chart": pie_chart_dict,
                "filter": table_query_list,
            }
        )
    else:
        return Response({"message_type": "d_not_f"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_incident_pci_dss_pie_chart_testing(request):
    condition = request.GET.get("condition")
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get("hids_incident_agent")
    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})

    # groupby query to get total unique count of 'rule_pci_dss'
    SQL_query1 = f"SELECT rule_pci_dss, count(agent_id) rule_pci_dss_count from {indice_name}-* WHERE rule_pci_dss IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} Group By rule_pci_dss ORDER BY rule_pci_dss_count DESC LIMIT 5;"

    search1 = opensearch_conn_using_db(SQL_query1, location_id, plan_id)

    if search1.get("total") not in exclude_values:
        unique_rule_pci_dss, rule_pci_dss_count = map(list, zip(*search1["datarows"]))

        pie_chart_dict = {"series": rule_pci_dss_count, "labels": unique_rule_pci_dss}

        str_unique_technique = str(unique_rule_pci_dss).strip("[]")
        unique_rule_pci_dss_tuple = "({})".format(str_unique_technique)

    else:
        return Response({"message_type": "d_not_f"})

    # in the total count of single agent_id calculating 'rule_pci_dss' wise count
    SQL_query2 = f"SELECT agent_id, agent_ip, rule_pci_dss, count(agent_id) as rule_pci_dss_count from {indice_name}-* WHERE rule_pci_dss IN {unique_rule_pci_dss_tuple} AND rule_pci_dss IS NOT NULL AND agent_id IS NOT NULL AND agent_ip IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY agent_id, agent_ip, rule_pci_dss;"

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
                "message_type": "success",
                "pie_chart": pie_chart_dict,
                "filter": table_query_list,
            }
        )
    else:
        return Response({"message_type": "d_not_f"})


# 3.b rule_pci_dss count table # Card Name: PCI DSS (view more)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_incident_pci_dss_table(request):
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get("hids_incident_agent")
    agent_id = request.GET.get("name")

    if agent_id is None:
        return Response({"message_type": "d_not_f", "errors": "name_not_found"})

    rule_pci_dss = request.GET.get("name1")

    if rule_pci_dss is None:
        return Response({"message_type": "d_not_f", "errors": "name1_not_found"})

    agent_ip = request.GET.get("name2")

    if agent_ip is None:
        return Response({"message_type": "d_not_f", "errors": "name2_not_found"})

    past_time = request.GET.get("past_time")
    current_time = request.GET.get("current_time")

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})

    # sql query to get table data
    table_query = f"SELECT @timestamp, agent_name, agent_ip, agent_id, id, rule_level, rule_description, rule_id, rule_groups, rule_pci_dss, rule_gpg13, rule_gdpr, rule_mitre_id, rule_mitre_tactic, rule_mitre_technique FROM {indice_name}-* WHERE agent_id = {agent_id} AND agent_ip = '{agent_ip}' AND rule_pci_dss = '{rule_pci_dss}' AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} ORDER BY attack_epoch_time DESC limit 200000;"

    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)

    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [
            "timestamp" if (item["name"] == "@timestamp") else item["name"]
            for item in run_sql.get("schema")
        ]

        table_query_list = []
        for i, row in enumerate(run_sql.get("datarows")):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)

        for item in table_query_list:
            if "timestamp" in item:
                with_fractional_part = item.get("timestamp")
                item["timestamp"] = with_fractional_part.split(".")[0]

        return Response(
            {
                "message_type": "success",
                "count": len(table_query_list),
                "agent_id": agent_id,
                "table": table_query_list,
            }
        )
    else:
        return Response({"message_type": "d_not_f"})


# 4.a potential_ransomware_event count # Card Name: potential_ransomware_event
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_incident_potential_ransomware(request):
    condition = request.GET.get("condition")
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get("hids_incident_agent")

    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})

    sql_query = f"SELECT agent_id, agent_ip, count(potential_ransomware_event) FROM {indice_name}-* WHERE potential_ransomware_event = 'true' AND agent_id IS NOT NULL AND agent_ip IS NOT NULL AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) GROUP BY agent_id, agent_ip, potential_ransomware_event;"

    search1 = opensearch_conn_using_db(sql_query, location_id, plan_id)

    if search1.get("total") not in exclude_values:
        agent_id, agent_id, ransomeware_count = map(list, zip(*search1["datarows"]))
        total_ransomeware_count = sum(ransomeware_count)
        key_names = [
            "ransomware_count"
            if (item["name"] == "count(potential_ransomware_event)")
            else item["name"]
            for item in search1.get("schema")
        ]

        table_query_list = []
        for i, key_values in enumerate(search1.get("datarows")):
            Dict = {}
            Dict.update(dict(zip(key_names, key_values)))
            Dict["ransomware_value"] = "true"
            Dict["past_time"] = past_time
            Dict["current_time"] = current_time

            table_query_list.append(Dict)

        return Response(
            {
                "message_type": "success",
                "count": total_ransomeware_count,
                "filter": table_query_list,
            }
        )
    else:
        filter_list = [
            {
                "agent_id": 0,
                "agent_ip": 0,
                "ransomware_count": 0,
                "ransomware_value": "true",
                "past_time": past_time,
                "current_time": current_time,
            }
        ]
        return Response({"message_type": "success", "count": 0, "filter": filter_list})


# 4.b potential_ransomware_event table # Card Name: potential_ransomware_event (view more)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_incident_potential_ransomware_table(request):
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get("hids_incident_agent")
    ransomeware_count = request.GET.get("ransomware_count")

    if ransomeware_count is None:
        return Response(
            {"message_type": "d_not_f", "errors": "ransomeware_count_n_found"}
        )

    past_time = request.GET.get("past_time")
    current_time = request.GET.get("current_time")

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})

    agent_ip = request.GET.get("agent_ip")

    if agent_ip is None:
        return Response({"message_type": "d_not_f", "errors": "agent_ip_n_found"})

    agent_id = request.GET.get("agent_id")

    if agent_id is None:
        return Response({"message_type": "d_not_f", "errors": "agent_id_n_found"})

    # sql query to get table data
    table_query = f"SELECT @timestamp, agent_name, agent_ip, agent_id, id, rule_level, rule_description, rule_id, rule_groups, rule_pci_dss, rule_gpg13, rule_gdpr, rule_hipaa, rule_mitre_id, rule_mitre_tactic, rule_mitre_technique, syscheck_path FROM {indice_name}-* WHERE agent_id = {agent_id} AND agent_ip = '{agent_ip}' AND potential_ransomware_event = 'true' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) ORDER BY attack_epoch_time DESC limit {ransomeware_count};"

    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)

    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [
            "timestamp" if (item["name"] == "@timestamp") else item["name"]
            for item in run_sql.get("schema")
        ]

        table_query_list = []
        for i, row in enumerate(run_sql.get("datarows")):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)

        for item in table_query_list:
            if "timestamp" in item:
                with_fractional_part = item.get("timestamp")
                item["timestamp"] = with_fractional_part.split(".")[0]

        return Response(
            {
                "message_type": "success",
                "count": len(table_query_list),
                "table": table_query_list,
            }
        )
    else:
        return Response({"message_type": "d_not_f"})


# 5.a anomaly_label count # Card Name: anomaly_label
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_incident_anomaly_label(request):
    condition = request.GET.get("condition")
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get("hids_incident_agent")

    past_time, current_time = calculate_start_end_time(condition)

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "invalid_condition"})

    sql_query = f"SELECT agent_id, agent_ip, count(anomaly_label) FROM {indice_name}-* WHERE anomaly_label = 0 AND agent_id IS NOT NULL AND agent_ip IS NOT NULL AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) GROUP BY agent_id, agent_ip, anomaly_label;"

    search1 = opensearch_conn_using_db(sql_query, location_id, plan_id)

    if search1.get("total") not in exclude_values:
        agent_id, agent_id, anomaly_count = map(list, zip(*search1["datarows"]))
        total_anomaly_count = sum(anomaly_count)
        key_names = [
            "anomaly_label_count"
            if (item["name"] == "count(anomaly_label)")
            else item["name"]
            for item in search1.get("schema")
        ]

        table_query_list = []
        for i, key_values in enumerate(search1.get("datarows")):
            Dict = {}
            Dict.update(dict(zip(key_names, key_values)))
            Dict["anomaly_label_value"] = 0
            Dict["past_time"] = past_time
            Dict["current_time"] = current_time

            table_query_list.append(Dict)

        return Response(
            {
                "message_type": "success",
                "count": total_anomaly_count,
                "filter": table_query_list,
            }
        )
    else:
        filter_list = [
            {
                "agent_id": 0,
                "agent_ip": 0,
                "anomaly_label_count": 0,
                "anomaly_label_value": 0,
                "past_time": past_time,
                "current_time": current_time,
            }
        ]
        return Response({"message_type": "success", "count": 0, "filter": filter_list})


# 5.b anomaly_label table # Card Name: anomaly_label (view more)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_incident_anomaly_table(request):
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "errors": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get("hids_incident_agent")
    ransomeware_count = request.GET.get("anomaly_label_count")

    if ransomeware_count is None:
        return Response(
            {"message_type": "d_not_f", "errors": "ransomeware_count_n_found"}
        )

    past_time = request.GET.get("past_time")
    current_time = request.GET.get("current_time")

    if past_time is None:
        return Response({"message_type": "d_not_f", "errors": "past_time_not_found"})

    if current_time is None:
        return Response({"message_type": "d_not_f", "errors": "current_time_not_found"})

    agent_ip = request.GET.get("agent_ip")

    if agent_ip is None:
        return Response({"message_type": "d_not_f", "errors": "agent_ip_n_found"})

    agent_id = request.GET.get("agent_id")

    if agent_id is None:
        return Response({"message_type": "d_not_f", "errors": "agent_id_n_found"})

    # sql query to get table data
    table_query = f"SELECT @timestamp, agent_name, agent_ip, agent_id, id, rule_level, rule_description, rule_id, rule_groups, rule_pci_dss, rule_gpg13, rule_gdpr, rule_hipaa, rule_mitre_id, rule_mitre_tactic, rule_mitre_technique FROM {indice_name}-* WHERE agent_id = {agent_id} AND agent_ip = '{agent_ip}' AND anomaly_label = 0 AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) ORDER BY attack_epoch_time DESC limit {ransomeware_count};"

    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)

    # formatting above query output to {column_name: column_value}
    if run_sql.get("total") not in exclude_values:
        key_names = [
            "timestamp" if (item["name"] == "@timestamp") else item["name"]
            for item in run_sql.get("schema")
        ]

        table_query_list = []
        for i, row in enumerate(run_sql.get("datarows")):
            Dict = {}
            Dict.update(dict(zip(key_names, row)))
            table_query_list.append(Dict)

        for item in table_query_list:
            if "timestamp" in item:
                with_fractional_part = item.get("timestamp")
                item["timestamp"] = with_fractional_part.split(".")[0]

        return Response(
            {
                "message_type": "success",
                "count": len(table_query_list),
                "table": table_query_list,
            }
        )
    else:
        return Response({"message_type": "d_not_f"})
