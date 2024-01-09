#  ===============================================================================================
#  File Name: hids_event_wazuh_mitre_attack_page.py
#  Description: This file contains code for each card on HIDS Event Page.
#  Active URL: https://xdr-demo.zerohack.in/hids/events

#  ----------------------------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  ===============================================================================================

from collections import defaultdict

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..grouping_epoch_time import *
from ..helpers import (
    getIndexNameByLocationId,
    getMlDlAccuracyRanges,
    getPlatformAndBlacklistedItemsByLocationId,
    pre_check_parameters,
)
from ..opensearch_config import opensearch_conn_using_db
from ..time_filter_on_queries import calculate_start_end_time
from .hids_event_mitre_attack_page import *

# opensearch indices name = xdr-hids-incident-jay-jasi9552-*
a = globals()
exclude_values = [0, None]


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_event_uniquedata_agentid(request):
    condition = request.GET.get("condition")
    past_time, current_time = calculate_start_end_time(condition)
    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return Response({"message_type": "d_not_f", "err": "plan_id_n_found"})

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get("hids_event_agent")

    table_query = f"SELECT agent_id,agent_name,agent_ip FROM {indice_name}-* WHERE agent_ip IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} Group By agent_id,agent_name,agent_ip;"

    run_sql = opensearch_conn_using_db(table_query, location_id, plan_id)

    if run_sql.get("total") not in exclude_values:
        key_names = [item["name"] for item in run_sql.get("schema")]

        final_response = []
        for i in range(len(run_sql.get("datarows"))):
            row = run_sql.get("datarows")[i]
            item_dict = dict(zip(key_names, row))
            item_dict.update(
                {
                    "past_time": past_time,
                    "current_time": current_time,
                    "condition": condition,
                }
            )
            final_response.append(item_dict)
        return Response({"message_type": "success", "data": final_response})
    else:
        return Response({"message_type": "d_not_f"})


# Security Event Page Wazuh dashboard queries(card name = Security Alerts)
def hids_event_security_alerts_func(
    agent_id, indice_name, current_time, past_time, location_id, plan_id
):
    sql_query = f"SELECT * from {indice_name}-* WHERE agent_id = {agent_id} AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time};"

    api_response = opensearch_conn_using_db(sql_query, location_id, plan_id)

    if api_response.get("total") not in exclude_values:
        key_names = [
            "unique_id" if (item["name"] == "id") else item["name"]
            for item in api_response.get("schema")
        ]

        final_response = []
        for idx, row in enumerate(api_response.get("datarows"), start=1):
            response_data = dict(zip(key_names, row))
            response_data["id"] = idx  # Assign the dynamic unique_id
            final_response.append(response_data)

        return {"message_type": "data_found", "data": final_response}
    else:
        return {"message_type": "d_not_f"}


# Security Event Page Wazuh dashboard queries(card name = Top 5 Alert)
def hids_event_top_five_alert_func(
    agent_id, indice_name, current_time, past_time, location_id, plan_id
):
    api_response = opensearch_conn_using_db(
        f"SELECT rule_description,COUNT(rule_description) count FROM {indice_name}-* WHERE rule_description IS NOT NULL and agent_id = {agent_id} AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY rule_description ORDER BY count DESC LIMIT 5;",
        location_id,
        plan_id,
    )

    if api_response.get("total") not in exclude_values:
        list1, list2 = map(list, zip(*api_response["datarows"]))
        dict_storage = {"series": list2, "labels": list1}
        return {"message_type": "data_found", "data": dict_storage}
    else:
        return {"message_type": "d_not_f"}


# # Security Event Page Wazuh dashboard queries(card name = Top 5 rules groups)
def hids_event_top_five_rule_groups_func(
    agent_id, indice_name, current_time, past_time, location_id, plan_id
):
    api_response = opensearch_conn_using_db(
        f"SELECT rule_groups,COUNT(rule_groups) count FROM {indice_name}-* WHERE rule_groups IS NOT NULL  and agent_id = {agent_id} AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY rule_groups ORDER BY count DESC LIMIT 5;",
        location_id,
        plan_id,
    )

    if api_response.get("total") not in exclude_values:
        list1, list2 = map(list, zip(*api_response["datarows"]))
        dict_storage = {"series": list2, "labels": list1}
        return {"message_type": "data_found", "data": dict_storage}
    else:
        return {"message_type": "d_not_f"}


# # Security Event Page Wazuh dashboard queries(card name = Top 5 PCI DSS Requirements)
def hids_event_top_five_pci_dssrequirements_func(
    agent_id, indice_name, current_time, past_time, location_id, plan_id
):
    sql_query = f"SELECT rule_pci_dss,COUNT(rule_pci_dss) count FROM {indice_name}-* WHERE rule_pci_dss IS NOT NULL AND agent_id = {agent_id} AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY rule_pci_dss ORDER BY count DESC LIMIT 5;"
    api_response = opensearch_conn_using_db(sql_query, location_id, plan_id)

    if api_response.get("total") not in exclude_values:
        list1, list2 = map(list, zip(*api_response["datarows"]))
        dict_storage = {"series": list2, "labels": list1}
        return {"message_type": "data_found", "data": dict_storage}
    else:
        return {"message_type": "d_not_f"}


# --------------------------line chart------------------
# Security Event Page Wazuh dashboard queries(card name = Alert groups evolution)
def hids_event_alert_groups_evolution_security_func(
    agent_id, indice_name, current_time, past_time, location_id, plan_id
):
    search1 = opensearch_conn_using_db(
        f"SELECT rule_hipaa,count(rule_hipaa) count FROM {indice_name}-* WHERE rule_hipaa IS NOT NULL AND agent_id = {agent_id} AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY rule_hipaa;",
        location_id,
        plan_id,
    )

    if search1.get("total") not in exclude_values:
        unique_rule, list2 = map(list, zip(*search1["datarows"]))
        attacker_ip_tuple = tuple(unique_rule)
        updated_tuple = attacker_ip_tuple
        if len(attacker_ip_tuple) == 1:
            updated_tuple = attacker_ip_tuple + ("0",)
    else:
        return {"message_type": "d_not_f"}
    search2 = opensearch_conn_using_db(
        f"SELECT rule_hipaa, DATE_FORMAT(@timestamp,'%Y-%m-%d'),count(rule_hipaa) count FROM {indice_name}-* WHERE rule_hipaa IN {updated_tuple} and agent_id = {agent_id} AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY DATE_FORMAT(@timestamp,'%Y-%m-%d'),rule_hipaa ORDER BY DATE_FORMAT(@timestamp,'%Y-%m-%d');",
        location_id,
        plan_id,
    )

    if search2.get("total") not in exclude_values:
        tactic_list, Dates, individual_ip_counts = map(list, zip(*search2["datarows"]))
        unique_dates = list(dict.fromkeys(Dates))
        n = len(unique_dates)
        nested_outer_list = []
        for u in range(len(unique_rule)):
            inner_list = []
            for i in range(len(search2["datarows"])):
                if unique_rule[u] == search2["datarows"][i][0]:
                    inner_list.append(search2["datarows"][i])
            nested_outer_list.append(inner_list)

        number_of_IPs = len(nested_outer_list)
        for i in range(number_of_IPs):
            a["IP_{0}".format(i)] = nested_outer_list[i]

        no_of_dates = len(unique_dates)
        for j in range(number_of_IPs):
            a["IP_{0}_count".format(j)] = [""] * no_of_dates

        for k in range(number_of_IPs):
            for i in range(len(a["IP_{0}".format(k)])):
                for j in range(len(unique_dates)):
                    if unique_dates[j] == a["IP_{0}".format(k)][i][1]:
                        a["IP_{0}_count".format(k)][j] = a["IP_{0}".format(k)][i][2]

        for k in range(number_of_IPs):
            for i in range(len(a["IP_{0}_count".format(k)])):
                if a["IP_{0}_count".format(k)][i] == "":
                    a["IP_{0}_count".format(k)][i] = 0

        for k in range(number_of_IPs):
            f"{'IP_{0}_count'.format(k)}", a["IP_{0}_count".format(k)]
        nd = {}
        series = []
        for k in range(number_of_IPs):
            rule_name = {}
            rule_name.update({"name": unique_rule[k]})
            rule_name.update({"data": a["IP_{0}_count".format(k)]})
            series.append(rule_name)

        nd.update({"labels": unique_dates})
        nd.update({"series": series})
        return {"message_type": "data_found", "data": nd}
    else:
        return {"message_type": "d_not_f"}


class HidsEventSecurityEventPage(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        location_id = request.user.location_id.id
        plan_idObj = request.user.location_id.activated_plan_id

        if plan_idObj is not None:
            plan_id = plan_idObj.id
        else:
            return Response({"message_type": "d_not_f", "err": "plan_id_n_found"})

        index_name_dict = getIndexNameByLocationId(location_id, plan_id)

        if index_name_dict.get("hids_event_agent") != None:
            indice_name = index_name_dict.get(
                "hids_event_agent"
            )  # (indice name(column_name table) = hids_event_agent)
            past_time = request.GET.get("past_time")
            current_time = request.GET.get("current_time")
            agent_id = request.GET.get("name")

            if agent_id is None:
                return Response({"message_type": "agent_id_not_found"})

            past_time = request.GET.get("past_time")
            current_time = request.GET.get("current_time")
            condition = request.GET.get("condition")
            if condition is None:
                return Response({"message_type": "condition_not_found"})

            if past_time is None:
                return Response({"message_type": "past_time_not_found"})

            if current_time is None:
                return Response({"message_type": "current_time_not_found"})

            hids_event_security_alerts = hids_event_security_alerts_func(
                agent_id, indice_name, current_time, past_time, location_id, plan_id
            )
            hids_event_top_five_alerts = hids_event_top_five_alert_func(
                agent_id, indice_name, current_time, past_time, location_id, plan_id
            )
            # hids_event_top_five_rule_groups = hids_event_top_five_rule_groups_func(agent_id,indice_name,current_time,past_time, location_id, plan_id)
            # hids_event_top_five_pci_dss_requirements = hids_event_top_five_pci_dssrequirements_func(agent_id,indice_name,current_time,past_time, location_id, plan_id)
            hids_event_alert_groups_evolution_security = (
                hids_event_alert_groups_evolution_security_func(
                    agent_id, indice_name, current_time, past_time, location_id, plan_id
                )
            )
            hids_event_top_tactics = hids_event_top_tactics_func(
                agent_id, indice_name, current_time, past_time, location_id, plan_id
            )
            # hids_event_rule_level_by_attack = hids_event_rule_level_byattack_func(
            #     agent_id, indice_name, current_time, past_time, location_id, plan_id
            # )
            # hids_event_rule_level_by_tactics = hids_event_rule_level_by_tactics_func(
            #     agent_id, indice_name, current_time, past_time, location_id, plan_id
            # )
            hids_event_alerts_evolution_over_time = (
                hids_event_alerts_evolution_overtime_func(
                    agent_id,
                    indice_name,
                    current_time,
                    past_time,
                    condition,
                    location_id,
                    plan_id,
                )
            )
            hids_event_mitre_attack_by_tactic = hids_event_mitre_attackby_tactic_func(
                agent_id, indice_name, current_time, past_time, location_id, plan_id
            )

            return Response(
                {
                    "hids_event_security_alerts": hids_event_security_alerts,
                    # "hids_event_top_five_alerts": hids_event_top_five_alerts,
                    # "hids_event_top_five_rule_groups": hids_event_top_five_rule_groups,
                    # "hids_event_top_five_pci_dss_requirements": hids_event_top_five_pci_dss_requirements,
                    "hids_event_alert_groups_evolution_security": hids_event_alert_groups_evolution_security,
                    "hids_event_top_tactics": hids_event_top_tactics,
                    # "hids_event_rule_level_by_attack": hids_event_rule_level_by_attack,
                    # "hids_event_rule_level_by_tactics": hids_event_rule_level_by_tactics,
                    "hids_event_alerts_evolution_over_time": hids_event_alerts_evolution_over_time,
                    "hids_event_mitre_attack_by_tactic": hids_event_mitre_attack_by_tactic,
                }
            )
        else:
            return Response({"message": "agent not found."})


############################################# Adding view more functionality in all charts of Security Event Page in HIDS Events #############################
# 1.a Security Event Page hids alert queries(card name = Top 5 Alert) #TopFiveAlert #pie chart
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_event_security_page_top_five_alert(request):
    parameters = pre_check_parameters(
        request, indice="hids_event_agent", type="pie_chart"
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

    search1 = opensearch_conn_using_db(
        f"SELECT rule_description, COUNT(agent_id) count FROM {indice_name}-* WHERE rule_description IS NOT NULL and agent_id = {agent_id} AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY rule_description ORDER BY count DESC LIMIT 5;",
        location_id,
        plan_id,
    )

    if search1.get("total") not in [0, None]:
        rule_description, rule_description_count = map(list, zip(*search1["datarows"]))

        pie_chart_dict = {"series": rule_description_count, "labels": rule_description}

        str_unique_description = str(rule_description).strip("[]")
        rule_description_tuple = "({})".format(str_unique_description)
    else:
        return Response({"message_type": "d_not_f"})

    # unique agent_id, agent_ip, rule_description wise count
    SQL_query2 = f"SELECT agent_id, agent_ip, rule_description, count(agent_id) as agent_count from {indice_name}-* WHERE rule_description IN {rule_description_tuple} AND rule_description IS NOT NULL AND agent_id IS NOT NULL AND agent_id = {agent_id} AND agent_ip IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY agent_id, agent_ip, rule_description;"

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
                "data": pie_chart_dict,
                "filter": table_query_list,
            }
        )
    else:
        return Response({"message_type": "d_not_f"})


# 1.b Card name: Top 5 Alert (view more)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_event_security_page_top_five_alert_table(request):
    parameters = pre_check_parameters(
        request, indice="hids_event_agent", type="table", rule="rule_description"
    )
    if parameters.pop("error"):
        return Response(parameters)
    else:
        indice_name = parameters.get("indice_name")
        location_id = parameters.get("location_id")
        plan_id = parameters.get("plan_id")
        agent_id = parameters.get("agent_id")
        rule_description = parameters.get("rule_description")
        agent_ip = parameters.get("agent_ip")
        past_time = parameters.get("past_time")
        current_time = parameters.get("current_time")

    # sql query to get table data
    table_query = f"SELECT @timestamp, agent_name, agent_ip, agent_id, id, rule_level, rule_description, rule_id, rule_groups, rule_pci_dss, rule_gpg13, rule_gdpr, rule_hipaa, rule_mitre_id, rule_mitre_tactic, rule_mitre_technique FROM {indice_name}-* WHERE agent_id = {agent_id} AND agent_ip = '{agent_ip}' AND rule_description = '{rule_description}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) ORDER BY attack_epoch_time DESC limit 200000;"

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


# 2.a Security Event Page hids alert queries(card name = Top 5 Rule Groups) #TopFiveRuleGroups #pie chart
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_event_security_page_top_five_rule_groups(request):
    parameters = pre_check_parameters(
        request, indice="hids_event_agent", type="pie_chart"
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

    search1 = opensearch_conn_using_db(
        f"SELECT rule_groups, COUNT(agent_id) count FROM {indice_name}-* WHERE rule_groups IS NOT NULL and agent_id = {agent_id} AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY rule_groups ORDER BY count DESC LIMIT 5;",
        location_id,
        plan_id,
    )
    if search1.get("total") not in [0, None]:
        rule_groups, rule_groups_count = map(list, zip(*search1["datarows"]))

        pie_chart_dict = {"series": rule_groups_count, "labels": rule_groups}

        str_unique_groups = str(rule_groups).strip("[]")
        rule_groups_tuple = "({})".format(str_unique_groups)
    else:
        return Response({"message_type": "d_not_f"})

    # unique agent_id, agent_ip, rule_description wise count
    SQL_query2 = f"SELECT agent_id, agent_ip, rule_groups, count(agent_id) as agent_count from {indice_name}-* WHERE rule_groups IN {rule_groups_tuple} AND rule_groups IS NOT NULL AND agent_id IS NOT NULL AND agent_id = {agent_id} AND agent_ip IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY agent_id, agent_ip, rule_groups;"
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
                "data": pie_chart_dict,
                "filter": table_query_list,
            }
        )
    else:
        return Response({"message_type": "d_not_f"})


# 2.b Card name: Top 5 Rule Groups (view more)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_event_security_page_top_five_rule_groups_table(request):
    parameters = pre_check_parameters(
        request, indice="hids_event_agent", type="table", rule="rule_groups"
    )
    if parameters.pop("error"):
        return Response(parameters)
    else:
        indice_name = parameters.get("indice_name")
        location_id = parameters.get("location_id")
        plan_id = parameters.get("plan_id")
        agent_id = parameters.get("agent_id")
        rule_groups = parameters.get("rule_groups")
        agent_ip = parameters.get("agent_ip")
        past_time = parameters.get("past_time")
        current_time = parameters.get("current_time")

    # sql query to get table data
    table_query = f"SELECT @timestamp, agent_name, agent_ip, agent_id, id, rule_level, rule_description, rule_id, rule_groups, rule_pci_dss, rule_gpg13, rule_gdpr, rule_hipaa, rule_mitre_id, rule_mitre_tactic, rule_mitre_technique FROM {indice_name}-* WHERE agent_id = {agent_id} AND agent_ip = '{agent_ip}' AND rule_groups = '{rule_groups}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) ORDER BY attack_epoch_time DESC limit 200000;"

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


# 3.a Security Event Page hids alert queries(card name = Top 5 Pci Dss Requirements) #TopFivePciDss #pie chart
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_event_security_page_top_five_rule_pci_dss(request):
    parameters = pre_check_parameters(
        request, indice="hids_event_agent", type="pie_chart"
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

    search1 = opensearch_conn_using_db(
        f"SELECT rule_pci_dss, COUNT(agent_id) count FROM {indice_name}-* WHERE rule_pci_dss IS NOT NULL and agent_id = {agent_id} AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY rule_pci_dss ORDER BY count DESC LIMIT 5;",
        location_id,
        plan_id,
    )
    if search1.get("total") not in [0, None]:
        rule_pci_dss, rule_pci_dss_count = map(list, zip(*search1["datarows"]))

        pie_chart_dict = {"series": rule_pci_dss_count, "labels": rule_pci_dss}

        str_unique_groups = str(rule_pci_dss).strip("[]")
        rule_pci_dss_tuple = "({})".format(str_unique_groups)
    else:
        return Response({"message_type": "d_not_f"})

    # unique agent_id, agent_ip, rule_description wise count
    SQL_query2 = f"SELECT agent_id, agent_ip, rule_pci_dss, count(agent_id) as agent_count from {indice_name}-* WHERE rule_pci_dss IN {rule_pci_dss_tuple} AND rule_pci_dss IS NOT NULL AND agent_id IS NOT NULL AND agent_id = {agent_id} AND agent_ip IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY agent_id, agent_ip, rule_pci_dss;"
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
                "data": pie_chart_dict,
                "filter": table_query_list,
            }
        )
    else:
        return Response({"message_type": "d_not_f"})


# 3.b Card name: Top 5 Rule Pci Dss (view more)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_event_security_page_top_five_rule_pci_dss_table(request):
    parameters = pre_check_parameters(
        request, indice="hids_event_agent", type="table", rule="rule_pci_dss"
    )
    if parameters.pop("error"):
        return Response(parameters)
    else:
        indice_name = parameters.get("indice_name")
        location_id = parameters.get("location_id")
        plan_id = parameters.get("plan_id")
        agent_id = parameters.get("agent_id")
        rule_pci_dss = parameters.get("rule_pci_dss")
        agent_ip = parameters.get("agent_ip")
        past_time = parameters.get("past_time")
        current_time = parameters.get("current_time")

    # sql query to get table data
    table_query = f"SELECT @timestamp, agent_name, agent_ip, agent_id, id, rule_level, rule_description, rule_id, rule_groups, rule_pci_dss, rule_gpg13, rule_gdpr, rule_hipaa, rule_mitre_id, rule_mitre_tactic, rule_mitre_technique FROM {indice_name}-* WHERE agent_id = {agent_id} AND agent_ip = '{agent_ip}' AND rule_pci_dss = '{rule_pci_dss}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) ORDER BY attack_epoch_time DESC limit 200000;"

    print(table_query)
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


# 4.a Mitre Attack Page hids alert queries(card name = Rule Level by attack ID) #RuleLevelAttackID #pie chart
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_event_mitre_attack_page_rule_level_by_attack_id(request):
    parameters = pre_check_parameters(
        request, indice="hids_event_agent", type="pie_chart"
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

    search1 = opensearch_conn_using_db(
        f"SELECT rule_mitre_id, COUNT(agent_id) count FROM {indice_name}-* WHERE rule_mitre_id IS NOT NULL and agent_id = {agent_id} AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY rule_mitre_id ORDER BY count DESC LIMIT 5;",
        location_id,
        plan_id,
    )
    if search1.get("total") not in [0, None]:
        rule_mitre_id, rule_mitre_id_count = map(list, zip(*search1["datarows"]))

        pie_chart_dict = {"series": rule_mitre_id_count, "labels": rule_mitre_id}

        str_unique_groups = str(rule_mitre_id).strip("[]")
        rule_mitre_id_tuple = "({})".format(str_unique_groups)
    else:
        return Response({"message_type": "d_not_f"})

    # unique agent_id, agent_ip, rule_description wise count
    SQL_query2 = f"SELECT agent_id, agent_ip, rule_mitre_id, count(agent_id) as agent_count from {indice_name}-* WHERE rule_mitre_id IN {rule_mitre_id_tuple} AND rule_mitre_id IS NOT NULL AND agent_id IS NOT NULL AND agent_id = {agent_id} AND agent_ip IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY agent_id, agent_ip, rule_mitre_id;"
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
                "data": pie_chart_dict,
                "filter": table_query_list,
            }
        )
    else:
        return Response({"message_type": "d_not_f"})


# 4.b Card name: Rule Level by attack ID (view more)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_event_mitre_attack_page_rule_level_by_attack_id_table(request):
    parameters = pre_check_parameters(
        request, indice="hids_event_agent", type="table", rule="rule_mitre_id"
    )
    if parameters.pop("error"):
        return Response(parameters)
    else:
        indice_name = parameters.get("indice_name")
        location_id = parameters.get("location_id")
        plan_id = parameters.get("plan_id")
        agent_id = parameters.get("agent_id")
        rule_mitre_id = parameters.get("rule_mitre_id")
        agent_ip = parameters.get("agent_ip")
        past_time = parameters.get("past_time")
        current_time = parameters.get("current_time")

    # sql query to get table data
    table_query = f"SELECT @timestamp, agent_name, agent_ip, agent_id, id, rule_level, rule_description, rule_id, rule_groups, rule_pci_dss, rule_gpg13, rule_gdpr, rule_hipaa, rule_mitre_id, rule_mitre_tactic, rule_mitre_technique FROM {indice_name}-* WHERE agent_id = {agent_id} AND agent_ip = '{agent_ip}' AND rule_mitre_id = '{rule_mitre_id}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) ORDER BY attack_epoch_time DESC limit 200000;"

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


# 5.a Mitre Attack Page hids alert queries(card name = Mitre Attack Techniques) #MitreAttackTechniques #pie chart
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_event_mitre_attack_page_rule_mitre_technique(request):
    parameters = pre_check_parameters(
        request, indice="hids_event_agent", type="pie_chart"
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

    search1 = opensearch_conn_using_db(
        f"SELECT rule_mitre_technique, COUNT(agent_id) count FROM {indice_name}-* WHERE rule_mitre_technique IS NOT NULL and agent_id = {agent_id} AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY rule_mitre_technique ORDER BY count DESC LIMIT 5;",
        location_id,
        plan_id,
    )
    if search1.get("total") not in [0, None]:
        rule_mitre_technique, rule_mitre_technique_count = map(
            list, zip(*search1["datarows"])
        )

        pie_chart_dict = {
            "series": rule_mitre_technique_count,
            "labels": rule_mitre_technique,
        }

        str_unique_groups = str(rule_mitre_technique).strip("[]")
        rule_mitre_technique_tuple = "({})".format(str_unique_groups)
    else:
        return Response({"message_type": "d_not_f"})

    # unique agent_id, agent_ip, rule_description wise count
    SQL_query2 = f"SELECT agent_id, agent_ip, rule_mitre_technique, count(agent_id) as agent_count from {indice_name}-* WHERE rule_mitre_technique IN {rule_mitre_technique_tuple} AND rule_mitre_technique IS NOT NULL AND agent_id IS NOT NULL AND agent_id = {agent_id} AND agent_ip IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY agent_id, agent_ip, rule_mitre_technique;"
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
                "data": pie_chart_dict,
                "filter": table_query_list,
            }
        )
    else:
        return Response({"message_type": "d_not_f"})


# 5.b Card name: Mitre Attack Techniques (view more)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_event_mitre_attack_page_rule_mitre_technique_table(request):
    parameters = pre_check_parameters(
        request, indice="hids_event_agent", type="table", rule="rule_mitre_technique"
    )
    if parameters.pop("error"):
        return Response(parameters)
    else:
        indice_name = parameters.get("indice_name")
        location_id = parameters.get("location_id")
        plan_id = parameters.get("plan_id")
        agent_id = parameters.get("agent_id")
        rule_mitre_technique = parameters.get("rule_mitre_technique")
        agent_ip = parameters.get("agent_ip")
        past_time = parameters.get("past_time")
        current_time = parameters.get("current_time")

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

# Alert Groups Evolution(line chart)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_event_security_page_alert_groups_evolution(request):

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

    search1 = opensearch_conn_using_db(
        f"SELECT rule_hipaa,count(agent_id) count FROM {indice_name}-* WHERE rule_hipaa IS NOT NULL AND agent_id = {agent_id} AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY rule_hipaa;",
        location_id,
        plan_id,
    )

    if search1.get("total") not in exclude_values:
        unique_rule, list2 = map(list, zip(*search1["datarows"]))
        attacker_ip_tuple = tuple(unique_rule)
        updated_tuple = attacker_ip_tuple
        if len(attacker_ip_tuple) == 1:
            updated_tuple = attacker_ip_tuple + ("0",)
    else:
        return Response({"message_type": "d_not_f"})

    search2 = opensearch_conn_using_db(
        f"SELECT rule_hipaa, DATE_FORMAT(@timestamp,'%Y-%m-%d'),count(agent_id) count FROM {indice_name}-* WHERE rule_hipaa IN {updated_tuple} and agent_id = {agent_id} AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY DATE_FORMAT(@timestamp,'%Y-%m-%d'),rule_hipaa ORDER BY DATE_FORMAT(@timestamp,'%Y-%m-%d');",
        location_id,
        plan_id,
    )

    if search2.get("total") not in exclude_values:
        tactic_list, Dates, individual_ip_counts = map(list, zip(*search2["datarows"]))
        unique_dates = list(dict.fromkeys(Dates))
        n = len(unique_dates)
        nested_outer_list = []
        for u in range(len(unique_rule)):
            inner_list = []
            for i in range(len(search2["datarows"])):
                if unique_rule[u] == search2["datarows"][i][0]:
                    inner_list.append(search2["datarows"][i])
            nested_outer_list.append(inner_list)

        number_of_IPs = len(nested_outer_list)
        for i in range(number_of_IPs):
            a["IP_{0}".format(i)] = nested_outer_list[i]

        no_of_dates = len(unique_dates)
        for j in range(number_of_IPs):
            a["IP_{0}_count".format(j)] = [""] * no_of_dates

        for k in range(number_of_IPs):
            for i in range(len(a["IP_{0}".format(k)])):
                for j in range(len(unique_dates)):
                    if unique_dates[j] == a["IP_{0}".format(k)][i][1]:
                        a["IP_{0}_count".format(k)][j] = a["IP_{0}".format(k)][i][2]

        for k in range(number_of_IPs):
            for i in range(len(a["IP_{0}_count".format(k)])):
                if a["IP_{0}_count".format(k)][i] == "":
                    a["IP_{0}_count".format(k)][i] = 0

        for k in range(number_of_IPs):
            f"{'IP_{0}_count'.format(k)}", a["IP_{0}_count".format(k)]
        nd = {}
        series = []
        for k in range(number_of_IPs):
            rule_name = {}
            rule_name.update({"name": unique_rule[k]})
            rule_name.update({"data": a["IP_{0}_count".format(k)]})
            series.append(rule_name)

        nd.update({"labels": unique_dates})
        nd.update({"series": series})

    # unique agent_id, agent_ip, rule_hipaa wise count
    SQL_query2 = f"SELECT agent_id, agent_ip, rule_hipaa, count(agent_id) as rule_hipaa_count from {indice_name}-* WHERE rule_hipaa IN {updated_tuple} AND rule_hipaa IS NOT NULL AND agent_id IS NOT NULL AND agent_id = {agent_id} AND agent_ip IS NOT NULL AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time} GROUP BY agent_id, agent_ip, rule_hipaa;"

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
                "pie_chart": nd,
                "filter": table_query_list,
            }
        )

    else:
        return Response({"message_type": "d_not_f"})


# Alert Groups Evolution(line chart) # view more
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_event_security_page_alert_groups_evolution_table(request):

    parameters = pre_check_parameters(
        request, indice="hids_event_agent", type="table", rule="rule_hipaa"
    )
    if parameters.pop("error"):
        return Response(parameters)
    else:
        indice_name = parameters.get("indice_name")
        location_id = parameters.get("location_id")
        plan_id = parameters.get("plan_id")
        agent_id = parameters.get("agent_id")
        rule_hipaa = parameters.get("rule_hipaa")
        agent_ip = parameters.get("agent_ip")
        past_time = parameters.get("past_time")
        current_time = parameters.get("current_time")

    # sql query to get table data
    table_query = f"SELECT @timestamp, agent_name, agent_ip, agent_id, id, rule_level, rule_description, rule_id, rule_groups, rule_pci_dss, rule_gpg13, rule_gdpr, rule_hipaa, rule_mitre_id, rule_mitre_tactic, rule_mitre_technique FROM {indice_name}-* WHERE agent_id = {agent_id} AND agent_ip = '{agent_ip}' AND rule_hipaa = '{rule_hipaa}' AND (attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time}) ORDER BY attack_epoch_time DESC limit 200000;"

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
                "rule_hipaa": rule_hipaa,
                "table": table_query_list,
            }
        )
    else:
        return Response({"message_type": "d_not_f"})


# Security Alerts (table)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hids_event_security_logs_table(request):
    parameters = pre_check_parameters(
        request, indice="hids_event_agent", type="table"
    )
    if parameters.pop("error"):
        return Response(parameters)
    else:
        indice_name = parameters.get("indice_name")
        location_id = parameters.get("location_id")
        plan_id = parameters.get("plan_id")
        agent_id = parameters.get("agent_id")
        past_time = parameters.get("past_time")
        current_time = parameters.get("current_time")

    sql_query = f"SELECT * FROM {indice_name}-* WHERE agent_id = {agent_id} AND attack_epoch_time >= {past_time} AND attack_epoch_time <= {current_time};"

    api_response = opensearch_conn_using_db(sql_query, location_id, plan_id)

    if api_response.get("total") not in exclude_values:
        key_names = [
            "unique_id" if (item["name"] == "id") else item["name"]
            for item in api_response.get("schema")
        ]

        final_response = []
        for idx, row in enumerate(api_response.get("datarows"), start=1):
            response_data = dict(zip(key_names, row))
            response_data["id"] = idx  # Assign the dynamic unique_id
            final_response.append(response_data)

        return Response({"message_type": "data_found", "data": final_response})
    else:
        return Response({"message_type": "d_not_f"})
