#  ==========================================================================================================================================================================================================================
#  File Name: helpers.py
#  Description: This file contains helper functions which are used in functionalities like: creating api logs, get indice name from agent table on basis location_id, get blacklisted ip, classes from blacklisted table.
#  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  ==========================================================================================================================================================================================================================

from time import gmtime, strftime

from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import (
    Agent_data,
    Attach_Location,
    Client_data,
    Init_Configs,
    Page_Permissions,
    blacklisted_data,
)
from .serializers import Email_Config_Serializer, LogsSerializer, UserProfileSerializer
from .time_filter_on_queries import calculate_start_end_time


# test code
@permission_classes([IsAuthenticated])
def api_logs_make(request, log_type=0, description=0):
    userDataS = UserProfileSerializer(request.user)
    ip = request.META.get("HTTP_X_FORWARDED_FOR")
    browser_type = request.META["HTTP_USER_AGENT"]
    req_method = request.method

    if ip:
        ip = ip.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")

    makeData = {
        "table_name": "client_data",
        "client_id": userDataS.data["id"],
        "org_id": userDataS.data["organization_id"],
        "type": log_type,
        "ip": ip,
        "browser_type": browser_type,
        "req_method": req_method,
        "description": description,
        "date_time": strftime("%Y-%m-%d %H:%M:%S", gmtime()),
    }
    convertPostData = request.post = makeData

    valid_data_serializer = LogsSerializer(data=convertPostData)
    valid_data_serializer.is_valid()
    valid_data_serializer.save()


def helper_init_configs(email_id, config_type_param):
    try:
        clientObj = Client_data.objects.get(email=email_id)
        loc_id = clientObj.location_id
        plan_id = loc_id.activated_plan_id
        queryObj = Init_Configs.objects.filter(
            location_id=loc_id, config_type=config_type_param, updated_plan_id=plan_id
        ).first()
        return {
            "init_id": queryObj.id,
            "config_type": queryObj.config_type,
            "email_ids": queryObj.email_ids,
            "platform_val": queryObj.platform_val,
            "severity_val": queryObj.severity_val,
            "time_interval_val": queryObj.time_interval_val,
            "time_interval_name": queryObj.time_interval_name,
            "is_active": queryObj.is_active,
            "location_id": queryObj.location_id,
            "plan_id": plan_id,
        }
    except ObjectDoesNotExist:
        return {"data": "d_not_f"}


def getAgentNameOrgId(org_id):
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT a.organization_id, a.attach_agent_group, a.attach_agent_network, b.city, b.state, c.country_name, a.wazuh_attach_agent FROM agent_details a LEFT JOIN organization_location b ON a.org_location_id = b.id LEFT JOIN country c ON b.country_id = c.id WHERE a.organization_id = %s LIMIT 1",
            [org_id],
        )

        row = cursor.fetchone()

        if row:
            agent_name = {
                "org_id": str(row[0]),
                "agent_group": str(row[1]),
                "agent_network": str(row[2]),
                "city": str(row[3]),
                "state": str(row[4]),
                "country": str(row[5]),
                "wazuh_attach": str(row[6]),
            }
        else:
            agent_name = None
    finally:
        cursor.close()

    return agent_name


def helper_init_configs_mult(config_type_param):
    try:
        queryObj = Init_Configs.objects.filter(config_type=config_type_param).all()
        obj_Serializer = Email_Config_Serializer(queryObj, many=True)
        return obj_Serializer.data
    except ObjectDoesNotExist:
        return {"data": "d_not_f"}


def update_time(t_id, update_time):
    try:
        initObj = Init_Configs.objects.get(id=t_id)
        initObj.time_interval_name = update_time
        initObj.save()
    except ObjectDoesNotExist:
        return {"data": "d_not_f"}


def strToComma(strParam):
    simpleStr = ""
    strParam = strParam.split(",")

    for i in strParam:
        simpleStr += f"'{i}',"

    return simpleStr.rstrip(",")


def getIndexNameByLocationId(location_id, plan_id):
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT a.organization_id, a.attach_agent_group, a.attach_agent_network, b.city, b.state, c.country_name, a.wazuh_attach_agent, a.nids_event_agent, a.nids_alert_agent, a.nids_incident_agent, a.nids_assets_agent, a.nids_nmap_agent, a.nids_global_agent, a.trace_event_agent, a.trace_alert_agent, a.trace_incident_agent, a.trace_global_agent, a.trace_dpi_agent, a.hids_event_agent, a.hids_alert_agent, a.hids_incident_agent, a.hids_assets_agent, a.soar_agent, a.tps_agent, a.ess_agent, a.sbs_agent, a.tptf_agent, a.mm_agent, a.hc_agent FROM agent_details a LEFT JOIN organization_location b ON a.org_location_id = b.id LEFT JOIN country c ON b.country_id = c.id WHERE a.org_location_id = %s AND b.activated_plan_id = %s LIMIT 1",
            [location_id, plan_id],
        )

        row = cursor.fetchone()

        if row:
            agent_name = {
                "org_id": str(row[0]),
                "agent_group": str(row[1]),
                "agent_network": str(row[2]),
                "city": str(row[3]),
                "state": str(row[4]),
                "country": str(row[5]),
                "wazuh_attach": str(row[6]),
                "nids_event_agent": str(row[7]),
                "nids_alert_agent": str(row[8]),
                "nids_incident_agent": str(row[9]),
                "nids_assets_agent": str(row[10]),
                "nids_nmap_agent": str(row[11]),
                "nids_global_agent": str(row[12]),
                "trace_event_agent": str(row[13]),
                "trace_alert_agent": str(row[14]),
                "trace_incident_agent": str(row[15]),
                "trace_global_agent": str(row[16]),
                "trace_dpi_agent": str(row[17]),
                "hids_event_agent": str(row[18]),
                "hids_alert_agent": str(row[19]),
                "hids_incident_agent": str(row[20]),
                "hids_assets_agent": str(row[21]),
                "soar_agent": str(row[22]),
                "tps_agent": str(row[23]),
                "ess_agent": str(row[24]),
                "sbs_agent": str(row[25]),
                "tptf_agent": str(row[26]),
                "mm_agent": str(row[27]),
                "hc_agent": str(row[28]),
            }
        else:
            agent_name = None
    finally:
        cursor.close()

    return agent_name


# get platform, blacklisted items using location_id
def getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id):
    try:
        init_obj = Init_Configs.objects.filter(
            location_id=location_id,
            config_type="dashboard_filter",
            updated_plan_id=plan_id,
        ).first()
        blacklisted_obj = blacklisted_data.objects.filter(
            location_id=location_id, updated_plan_id=plan_id
        ).first()
        detail_dict = {}

        if init_obj is not None:
            platform = init_obj.platform_val
            accuracy_value = init_obj.accuracy_val

            # formatting platform
            if platform.startswith("(") and platform.endswith(")"):
                platform_tuple = platform
            elif platform.startswith("[") and platform.endswith("]"):
                _platform = platform.strip("[]")
                platform_tuple = "(" + _platform + ")"
            elif "," in platform:
                _platform = tuple(platform.split(","))
                platform_tuple = str(_platform)
            else:
                platform_tuple = "('{}')".format(platform)

            # updating detail_dict for init_config_values
            detail_dict["platform_tuple"] = platform_tuple
            detail_dict["accuracy_val"] = accuracy_value

        if blacklisted_obj is not None:
            blacklisted_class_tuple = blacklisted_obj.blacklisted_class
            blacklisted_ip_tuple = blacklisted_obj.blacklisted_ip

            # updating detail_dict for blacklisted ip, threat_class values
            detail_dict["blacklisted_class_tuple"] = blacklisted_class_tuple
            detail_dict["blacklisted_ip_tuple"] = blacklisted_ip_tuple

    except Exception:
        detail_dict = {}

    return detail_dict


# get accuracy1, accuracy2 values using accuracy_val for ML DL cards
def getMlDlAccuracyRanges(accuracy_val):
    accuracy1 = 0
    accuracy2 = 0
    # case 1. above 90% ---- >90 and <=100
    if accuracy_val == 1:
        accuracy1 = 90
        accuracy2 = 100
    # case 2. above 75% ---- >75 and <=90
    elif accuracy_val == 2:
        accuracy1 = 75
        accuracy2 = 90
    # case 3. above 65% ----- >65 and <=75
    elif accuracy_val == 3:
        accuracy1 = 65
        accuracy2 = 75
    return accuracy1, accuracy2


# get agent_names of active pages# for notification_UI
def getActivePagesAgentName(email_id):
    try:
        clientObj = Client_data.objects.get(email=email_id)
        loc_id = clientObj.location_id
        plan_id = loc_id.activated_plan_id
        pageObj = Page_Permissions.objects.get(
            location_id=loc_id, updated_plan_id=plan_id
        )
        env_trace = pageObj.env_trace
        env_hids = pageObj.env_hids
        env_nids = pageObj.env_nids
        # get agent_details obj having same loc_id
        agentObj = Agent_data.objects.filter(
            org_location=loc_id, updated_plan_id=plan_id
        ).first()
        agent_dict = {}
        if agentObj is not None:
            if env_trace:
                agent_dict["trace_agent"] = agentObj.trace_incident_agent

            if env_hids:
                agent_dict["hids_agent"] = {
                    "hids_alert_agent": agentObj.hids_alert_agent,
                    "hids_event_agent": agentObj.hids_event_agent,
                    "hids_incident_agent": agentObj.hids_incident_agent,
                }

            if env_nids:
                agent_dict["nids_agent"] = agentObj.nids_incident_agent

        return agent_dict
    except ObjectDoesNotExist:
        return {"data": "d_not_f"}


# get agent_names of active pages# for notification_email
def getAgentNameNotificationEmail(email_id):
    try:
        clientObj = Client_data.objects.get(email=email_id)
        locObj = clientObj.location_id
        plan_id = locObj.activated_plan_id
        pageObj = Page_Permissions.objects.get(
            location_id=locObj, updated_plan_id=plan_id
        )
        env_trace = pageObj.env_trace
        env_hids = pageObj.env_hids
        env_nids = pageObj.env_nids
        # get agent_details obj having same loc_id
        agentObj = Agent_data.objects.filter(
            org_location=locObj, updated_plan_id=plan_id
        ).first()
        agent_dict = {}
        if agentObj is not None:
            if env_trace:
                agent_dict["trace_agent"] = agentObj.trace_incident_agent

            if env_hids:
                agent_dict["hids_agent"] = agentObj.hids_incident_agent

            if env_nids:
                agent_dict["nids_agent"] = agentObj.nids_incident_agent

            # get city, state, country from location table
            agent_dict["location_id"] = locObj.id
            agent_dict["city"] = locObj.city
            agent_dict["state"] = locObj.state
            agent_dict["country"] = locObj.country_id.country_name
            agent_dict["plan_id"] = plan_id

        return agent_dict
    except ObjectDoesNotExist:
        return {"data": "d_not_f"}


# get agent_names of active pages # For Health check notification_email
def getAgentNameSensorAlertNotiEmail(email_id):
    try:
        clientObj = Client_data.objects.get(email=email_id)
        locObj = clientObj.location_id
        plan_id = locObj.activated_plan_id
        pageObj = Page_Permissions.objects.get(
            location_id=locObj, updated_plan_id=plan_id
        )
        env_hc = pageObj.env_hc
        # get agent_details obj having same loc_id
        agentObj = Agent_data.objects.filter(
            org_location=locObj, updated_plan_id=plan_id
        ).first()
        agent_dict = {}
        if agentObj is not None:
            if env_hc:
                agent_dict["hc_agent"] = agentObj.hc_agent

            # get location_id, org_name, location_name from location table
            agent_dict["location_id"] = locObj.id
            agent_dict["org_name"] = locObj.org_id.organization_name
            agent_dict["location_name"] = locObj.branchcode
            agent_dict["plan_id"] = plan_id

        return agent_dict
    except ObjectDoesNotExist:
        return None


# get agent_names of active pages #HIDS ransomeware check and send data on email
def getAgentNameRansomwareEmailNoti(email_id):
    try:
        clientObj = Client_data.objects.get(email=email_id)
        locObj = clientObj.location_id
        plan_id = locObj.activated_plan_id
        pageObj = Page_Permissions.objects.get(
            location_id=locObj, updated_plan_id=plan_id
        )
        env_hids = pageObj.env_hids
        # get agent_details obj having same loc_id
        agentObj = Agent_data.objects.filter(
            org_location=locObj, updated_plan_id=plan_id
        ).first()
        agent_dict = {}
        if agentObj is not None:
            if env_hids:
                agent_dict["hids_alert_agent"] = agentObj.hids_alert_agent
                agent_dict["hids_event_agent"] = agentObj.hids_event_agent
                agent_dict["hids_incident_agent"] = agentObj.hids_incident_agent

            # get location_id, org_name, location_name from location table
            agent_dict["location_id"] = locObj.id
            agent_dict["org_name"] = locObj.org_id.organization_name
            agent_dict["location_name"] = locObj.branchcode
            agent_dict["plan_id"] = plan_id

        return agent_dict
    except ObjectDoesNotExist:
        return {"data": "d_not_f"}


# update ransomware epoch time in init_config table
def update_ransomware_epoch_time(t_id, update_time):
    try:
        initObj = Init_Configs.objects.get(id=t_id)
        initObj.ransomware_noti_epoch_val = update_time
        initObj.save()
    except ObjectDoesNotExist:
        return {"data": "d_not_f"}


def pre_check_parameters(
    request,
    indice,
    type,
    rule=None,
):
    
    agent_id = request.GET.get("agent_id")
    condition = request.GET.get("condition")

    if agent_id is None:
        return {"error": True, "message_type": "agent_id_not_found"}

    location_id = request.user.location_id.id
    plan_idObj = request.user.location_id.activated_plan_id

    if plan_idObj is not None:
        plan_id = plan_idObj.id
    else:
        return {"error": True, "message_type": "d_not_f", "errors": "plan_id_n_found"}

    index_name_dict = getIndexNameByLocationId(location_id, plan_id)
    indice_name = index_name_dict.get(indice)

    response_dict = {
        "error": False,
        "indice_name": indice_name,
        "location_id": location_id,
        "plan_id": plan_id,
        "agent_id": agent_id
    }
    if condition and type in ["pie_chart", "line_chart", "bar_chart"]:
        
        if condition is None:
            return {"error": True, "message_type": "condition_not_found"}

        past_time, current_time = calculate_start_end_time(condition)

        if past_time is None:
            return {
                "error": True,
                "message_type": "d_not_f",
                "errors": "invalid_condition",
            }
        response_dict.update(
            {
                "current_time": current_time,
                "past_time": past_time,
                "condition": condition
            }
        )

    if type == "table":
        if rule:
            rule_request = request.GET.get(rule)
            agent_ip = request.GET.get("agent_ip")
            
            if rule_request is None:
                return {
                    "error": True,
                    "message_type": "d_not_f",
                    "errors": f"{rule}_not_found",
                }
            
            if agent_ip is None:
                return {
                    "error": True,
                    "message_type": "d_not_f",
                    "errors": "agent_ip_not_found",
                }
            
            response_dict.update(
            {
                "agent_ip": agent_ip,
                rule: rule_request,
            }
        )
            
        past_time = request.GET.get("past_time")
        current_time = request.GET.get("current_time")

        if past_time is None:
            return {
                "error": True,
                "message_type": "d_not_f",
                "errors": "past_time_not_found",
            }

        if current_time is None:
            return {
                "error": True,
                "message_type": "d_not_f",
                "errors": "current_time_not_found",
            }

        response_dict.update(
            {
                "current_time": current_time,
                "past_time": past_time,
            }
        )

    return response_dict