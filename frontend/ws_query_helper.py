#  ===========================================================================================================
#  File Name: ws_query_helper.py
#  Description: To send email notifications using Web Socket on Client Dashboard.

#  -----------------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  ===========================================================================================================

from datetime import date,datetime,timezone,timedelta
import pytz, dateutil.parser
import threading
import time
from .mail_to import send_email_from_app_multiple
from .views import getAgentName, opensearch_conn_using_db
from .helpers import helper_init_configs, helper_init_configs_mult, getAgentNameOrgId,update_time,strToComma, getActivePagesAgentName, getPlatformAndBlacklistedItemsByLocationId,getAgentNameNotificationEmail
from .time_filter_on_queries import ws_notification_start_end_epoch_time
from .hc_email_noti_sensor_alert import sensor_alert_notification_time_loop
from .ransomware_email_noti import ransomware_noti_time_loop

global_utc_now = datetime.now().utcnow()
global_UTC_now = dateutil.parser.parse(str(global_utc_now))
global_interval_set = global_utc_now + timedelta(seconds=1)
global_interval_get = dateutil.parser.parse(str(global_interval_set))

global_UTC_now = int(round(global_UTC_now.replace(tzinfo=timezone.utc).timestamp() * 1000))   
global_interval_time = int(round(global_interval_get.replace(tzinfo=timezone.utc).timestamp() * 1000))

def _main(email_id):
    notification_UI_res = []
    notification_email = []
    if email_id is not None:
        try:
            active_agent_names = getActivePagesAgentName(email_id)
            notification_UI_res = notification_UI(active_agent_names,email_id)
        except Exception as e:
            pass

    return {"notificationRes":notification_UI_res,"notificationEmail":notification_email}


def notification_UI(active_agent_names,email_id):
    global global_interval_time

    init_configs = helper_init_configs(email_id,"notification_live")
    time_interval_val = int(init_configs.get("time_interval_val"))
    platform_val = init_configs.get("platform_val")
    is_active = init_configs.get("is_active")
    location_id = init_configs.get("location_id")
    plan_id = init_configs.get("plan_id")
    t_id = init_configs.get("init_id")
    time_interval_name = int(init_configs.get("time_interval_name"))
    final_response_UI = []

    # getting epoch_time values using different function #past_time is the past time(eg. last 5 min time in epoch format) and current_time is the current/now time in epoch format
    past_time, current_time, future_time_epoch = ws_notification_start_end_epoch_time(time_interval_val)
    
    if is_active == True:
        if(current_time > time_interval_name):

            update_time(t_id,future_time_epoch)

            # checking which agent is active accordingly creating query for that indice
            if 'hids_agent' in active_agent_names:
            
                hids_incident_agent = active_agent_names['hids_agent']['hids_incident_agent']

                # hids_incident query
                hids_query = f"SELECT @timestamp, agent_name, agent_ip, agent_id, rule_level, rule_description, rule_id, rule_groups, rule_pci_dss, rule_gpg13, rule_gdpr, rule_mitre_id, rule_mitre_tactic, rule_mitre_technique FROM {hids_incident_agent}-* WHERE (attack_epoch_time >= {past_time} and attack_epoch_time <= {current_time}) AND (agent_name IS NOT NULL) AND (agent_ip IS NOT NULL) AND (agent_id IS NOT NULL) AND (rule_level IS NOT NULL) AND (rule_description IS NOT NULL) AND (rule_id IS NOT NULL) AND (rule_groups IS NOT NULL) AND (rule_pci_dss IS NOT NULL) AND (rule_gpg13 IS NOT NULL) AND (rule_gdpr IS NOT NULL) AND (rule_mitre_id IS NOT NULL) AND (rule_mitre_tactic IS NOT NULL) AND (rule_mitre_technique IS NOT NULL) ORDER BY attack_epoch_time desc"

                hidsQueryCheck = opensearch_conn_using_db(hids_query, location_id, plan_id)
                hids_check_query_length = hidsQueryCheck.get("total")

                # hids query data output
                if hidsQueryCheck.get("total") is None:
                    hids_check_query_length = 0
                
                hids_data_UI , hids_key_names_UI = [], []
                if hids_check_query_length > 0:

                    hids_key_mapping_UI = {
                        "@timestamp": 'Timestamp',
                        "agent_name": 'Agent Name',
                        "agent_ip": 'Agent IP',
                        "agent_id": 'Agent ID',
                        "rule_level": 'Rule Level',
                        "rule_description": 'Rule Description',
                        "rule_id": 'Rule ID',
                        "rule_groups": 'Rule Groups',
                        "rule_pci_dss": 'Rule PCI DSS',
                        "rule_gpg13": 'Rule Gpg13',
                        "rule_gdpr": 'Rule Gdpr',
                        "rule_mitre_id": 'Rule Mitre ID',
                        "rule_mitre_tactic": 'Rule Mitre Tactic',
                        "rule_mitre_technique": 'Rule Mitre Technique',
                    }

                    hids_key_names_UI = [hids_key_mapping_UI.get(n.get('name')) for n in hidsQueryCheck.get('schema') if hids_key_mapping_UI.get(n.get('name'))]
                        
                    for i in range(0, len(hidsQueryCheck.get('datarows'))):
                        row = hidsQueryCheck.get('datarows')[i]
                        row_dict = dict(zip(hids_key_names_UI, row))
                        row_dict["Product Name"] = "Host Intrusion Detection System (HIDS)"
                        hids_data_UI.append(row_dict)

                # ransomware dashboard notification code
                hids_alert_agent = active_agent_names['hids_agent']['hids_alert_agent']
                hids_event_agent = active_agent_names['hids_agent']['hids_event_agent']

                for i,log_type_agent_name in enumerate([hids_alert_agent, hids_event_agent, hids_incident_agent]):

                    # hids_query for the 3 different log_type
                    hids_query = f"SELECT @timestamp, agent_ip, agent_name, syscheck_path, rule_description, rule_mitre_tactic, rule_mitre_technique FROM {log_type_agent_name}-* WHERE (attack_epoch_time >= {past_time} and attack_epoch_time <= {current_time}) AND (agent_ip IS NOT NULL) AND (agent_name IS NOT NULL) AND (syscheck_path IS NOT NULL) AND (rule_description IS NOT NULL) AND (rule_mitre_tactic IS NOT NULL) AND (rule_mitre_technique IS NOT NULL) AND potential_ransomware_event = 'true' ORDER BY attack_epoch_time desc;"

                    hidsAlertQueryCheck = opensearch_conn_using_db(hids_query, location_id, plan_id)
                    hids_ransomware_query_length = hidsAlertQueryCheck.get("total")
                    
                    # hids query data output
                    if hidsAlertQueryCheck.get("total") is None:
                        hids_ransomware_query_length = 0
                    
                    hids_key_names_ransomware = []

                    if hids_ransomware_query_length > 0:

                        hids_key_mapping = {
                            "@timestamp": 'Timestamp',
                            "agent_ip": 'Agent IP',
                            "agent_name": 'Agent Name',
                            "syscheck_path": 'System Check Path',
                            "rule_description": 'Rule Description',
                            "rule_mitre_tactic": 'Rule Mitre Tactic',
                            "rule_mitre_technique": 'Rule Mitre Technique',
                        
                        }

                        hids_key_names_ransomware = [hids_key_mapping.get(n.get('name')) for n in hidsAlertQueryCheck.get('schema') if hids_key_mapping.get(n.get('name'))]
                            
                        for i in range(0, len(hidsAlertQueryCheck.get('datarows'))):
                            row = hidsAlertQueryCheck.get('datarows')[i]
                            row_dict = dict(zip(hids_key_names_ransomware, row))
                            
                            if log_type_agent_name == hids_alert_agent:
                                row_dict["Product Name"] = "Ransomware Host Intrusion Detection System (HIDS) Alerts"
                            elif log_type_agent_name == hids_event_agent:
                                row_dict["Product Name"] = "Ransomware Host Intrusion Detection System (HIDS) Events"
                            elif log_type_agent_name == hids_incident_agent:
                                row_dict["Product Name"] = "Ransomware Host Intrusion Detection System (HIDS) Incidents"

                            hids_data_UI.append(row_dict)
                        
                for item in hids_data_UI:
                    if "Timestamp" in item:
                        with_fractional_part = item.get('Timestamp')
                        item['Timestamp'] = with_fractional_part.split(".")[0]

            if 'nids_agent' in active_agent_names:
                agent_name = active_agent_names['nids_agent']
                
                detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

                if not detail_dict:
                    # got empty dict
                    return {"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"}
                
                blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
                blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
                
                s1 = f"AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
                s2 = f" AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""

                # nids_incident query
                nids_query = f"SELECT attacker_ip, target_ip, ids_threat_class, count(*) as total_count FROM {agent_name}-* WHERE (attacker_ip IS NOT NULL) and (target_ip IS NOT NULL) and (ids_threat_class IS NOT NULL) "+s1+s2+f" and (attack_epoch_time >= {past_time} and attack_epoch_time <= {current_time}) and platform IN {platform_val} GROUP BY attacker_ip,target_ip,ids_threat_class ORDER BY total_count desc"

                nidsQueryCheck = opensearch_conn_using_db(nids_query, location_id, plan_id)
                nids_check_query_length = nidsQueryCheck.get("total")

                # nids query data output
                if nidsQueryCheck.get("total") is None:
                    nids_check_query_length = 0
                
                nids_data_UI , nids_key_names_UI = [], []

                if nids_check_query_length > 0:

                    nids_key_names_UI = {
                        "attacker_ip": 'Attacker IP',
                        "target_ip": 'Target IP',
                        "ids_threat_class": 'IDS Threat Class',
                        "count(*)": 'Count'
                    }

                    nids_key_names_UI = [nids_key_names_UI.get(n.get('name')) for n in nidsQueryCheck.get('schema') if nids_key_names_UI.get(n.get('name'))]
                        
                    for i in range(0, len(nidsQueryCheck.get('datarows'))):
                        row = nidsQueryCheck.get('datarows')[i]
                        row_dict = dict(zip(nids_key_names_UI, row))
                        row_dict["Product Name"] = "Network Intrusion Detection System (NIDS)"
                        nids_data_UI.append(row_dict)
            
            if 'trace_agent' in active_agent_names:
                agent_name = active_agent_names['trace_agent']
                detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

                if not detail_dict:
                    # got empty dict
                    return {"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"}
                
                blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
                blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
                
                s1 = f"AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
                s2 = f" AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""

                # trace_incident query
                trace_query = f"SELECT attacker_ip, target_ip,type_of_threat, sensor_name, count(*) as total_count FROM {agent_name}-* WHERE (attacker_ip IS NOT NULL) and (target_ip IS NOT NULL) "+s1+s2+f" and (attack_epoch_time >= {past_time} and attack_epoch_time <= {current_time}) and (ids_threat_class IS NOT NULL) GROUP BY attacker_ip,target_ip,type_of_threat,sensor_name ORDER BY total_count desc"

                traceQueryCheck = opensearch_conn_using_db(trace_query, location_id, plan_id)
                trace_check_query_length = traceQueryCheck.get("total")

                # trace query data output
                if traceQueryCheck.get("total") is None:
                    trace_check_query_length = 0
                
                trace_data_UI , trace_key_names_UI = [], []

                if trace_check_query_length > 0:

                    trace_key_names_UI = {
                        "attacker_ip": 'Attacker IP',
                        "target_ip": 'Target IP',
                        "type_of_threat": 'Type of Threat',
                        "sensor_name": 'Sensor Name',
                        "count(*)": 'Count',
                    }

                    trace_key_names_UI = [trace_key_names_UI.get(n.get('name')) for n in traceQueryCheck.get('schema') if trace_key_names_UI.get(n.get('name'))]
                        
                    for i in range(0, len(traceQueryCheck.get('datarows'))):
                        row = traceQueryCheck.get('datarows')[i]
                        row_dict = dict(zip(trace_key_names_UI, row))
                        row_dict["Product Name"] = "Threat Reconnaissance And Classification Engine (TRACE)"
                        trace_data_UI.append(row_dict)

            final_response_UI = hids_data_UI + nids_data_UI + trace_data_UI

    return final_response_UI


def notification_by_email(agent_data,is_active,email_ids,time_interval_val,platform_val,t_id,time_interval_name): # time_interval_name is the future epoch time which we store in init_config table, time_interval_val is email notification time value set by user in minutes/hours
    email_ids = email_ids.split(",")
    country = agent_data.get('country')
    state = agent_data.get('state')
    city = agent_data.get('city')
    location_id = agent_data.get('location_id')
    plan_id = agent_data.get('plan_id')
    email_data = {}


    # getting epoch_time values using different function #past_time (eg. last 5 min time in epoch format) and current_time is now time in epoch format
    past_time, current_time, future_time_epoch = ws_notification_start_end_epoch_time(time_interval_val)

    if is_active == True:
        if (current_time > time_interval_name):

            # update future time in db (eg. if time_interval_val is 5 min then we find out epoch time after 5 min and update it in db)
            update_time(t_id,future_time_epoch)

            # checking which agent is active accordingly creating query for that indice
            if 'hids_agent' in agent_data:
                agent_name = agent_data['hids_agent']

                # hids_incident query
                hids_query = f"SELECT @timestamp, agent_name, agent_ip, agent_id, rule_level, rule_description, rule_id, rule_groups, rule_pci_dss, rule_gpg13, rule_gdpr, rule_mitre_id, rule_mitre_tactic, rule_mitre_technique FROM {agent_name}-* WHERE (attack_epoch_time >= {past_time} and attack_epoch_time <= {current_time}) AND (agent_name IS NOT NULL) AND (agent_ip IS NOT NULL) AND (agent_id IS NOT NULL) AND (rule_level IS NOT NULL) AND (rule_description IS NOT NULL) AND (rule_id IS NOT NULL) AND (rule_groups IS NOT NULL) AND (rule_pci_dss IS NOT NULL) AND (rule_gpg13 IS NOT NULL) AND (rule_gdpr IS NOT NULL) AND (rule_mitre_id IS NOT NULL) AND (rule_mitre_tactic IS NOT NULL) AND (rule_mitre_technique IS NOT NULL) ORDER BY attack_epoch_time desc"

                hidsQueryCheck = opensearch_conn_using_db(hids_query, location_id, plan_id)
                hids_check_query_length = hidsQueryCheck.get("total")
                hids_data_email = []
                # hids query data output
                if hidsQueryCheck.get("total") is None:
                    hids_check_query_length = 0
                
                hids_key_names_email = []
                if hids_check_query_length > 0:

                    hids_key_mapping = {
                        "@timestamp": 'Timestamp',
                        "agent_name": 'Agent Name',
                        "agent_ip": 'Agent IP',
                        "agent_id": 'Agent ID',
                        "rule_level": 'Rule Level',
                        "rule_description": 'Rule Description',
                        "rule_id": 'Rule ID',
                        "rule_groups": 'Rule Groups',
                        "rule_pci_dss": 'Rule PCI DSS',
                        "rule_gpg13": 'Rule Gpg13',
                        "rule_gdpr": 'Rule Gdpr',
                        "rule_mitre_id": 'Rule Mitre ID',
                        "rule_mitre_tactic": 'Rule Mitre Tactic',
                        "rule_mitre_technique": 'Rule Mitre Technique',
                    }

                    hids_key_names_email = [hids_key_mapping.get(n.get('name')) for n in hidsQueryCheck.get('schema') if hids_key_mapping.get(n.get('name'))]
                        
                    for i in range(0, len(hidsQueryCheck.get('datarows'))):
                        row = hidsQueryCheck.get('datarows')[i]
                        hids_data_email.append(dict(zip(hids_key_names_email, row)))
                    email_data['Host Intrusion Detection System (HIDS)'] = hids_data_email

            if 'nids_agent' in agent_data:
                agent_name = agent_data['nids_agent']
                
                detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

                if not detail_dict:
                    # got empty dict
                    return {"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"}
                
                blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
                blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
                
                s1 = f"AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
                s2 = f" AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""

                # nids_incident query
                nids_query = f"SELECT attacker_ip, target_ip, ids_threat_class, count(*) as total_count FROM {agent_name}-* WHERE (attacker_ip IS NOT NULL) and (target_ip IS NOT NULL) and (ids_threat_class IS NOT NULL) "+s1+s2+f" and (attack_epoch_time >= {past_time} and attack_epoch_time <= {current_time}) and platform IN {platform_val} GROUP BY attacker_ip,target_ip,ids_threat_class ORDER BY total_count desc"

                nidsQueryCheck = opensearch_conn_using_db(nids_query, location_id, plan_id)
                nids_check_query_length = nidsQueryCheck.get("total")

                nids_data_email = []
                # nids query data output
                if nidsQueryCheck.get("total") is None:
                    nids_check_query_length = 0
                
                nids_key_names_email = []

                if nids_check_query_length > 0:

                    nids_key_mapping = {
                        "attacker_ip": 'Attacker IP',
                        "target_ip": 'Target IP',
                        "ids_threat_class": 'IDS Threat Class',
                        "count(*)": 'Count'
                    }

                    nids_key_names_email = [nids_key_mapping.get(n.get('name')) for n in nidsQueryCheck.get('schema') if nids_key_mapping.get(n.get('name'))]
                        
                    for i in range(0, len(nidsQueryCheck.get('datarows'))):
                        row = nidsQueryCheck.get('datarows')[i]
                        nids_data_email.append(dict(zip(nids_key_names_email, row)))
                    email_data['Network Intrusion Detection System (NIDS)'] = nids_data_email
            
            if 'trace_agent' in agent_data:
                agent_name = agent_data['trace_agent']
                
                detail_dict = getPlatformAndBlacklistedItemsByLocationId(location_id, plan_id)

                if not detail_dict:
                    # got empty dict
                    return {"message_type":"d_not_f", "errors": "plat_blacklist_dict_empty"}
                
                blacklisted_class_tuple = detail_dict.get("blacklisted_class_tuple")
                blacklisted_ip_tuple = detail_dict.get("blacklisted_ip_tuple")
                
                s1 = f"AND ids_threat_class NOT IN {blacklisted_class_tuple} " if blacklisted_class_tuple is not None else ""
                s2 = f" AND attacker_ip NOT IN {blacklisted_ip_tuple}" if blacklisted_ip_tuple is not None else ""

                # trace_incident query
                trace_query = f"SELECT attacker_ip, target_ip, type_of_threat, sensor_name, count(*) as total_count FROM {agent_name}-* WHERE (attacker_ip IS NOT NULL) and (target_ip IS NOT NULL) "+s1+s2+f" and (attack_epoch_time >= {past_time} and attack_epoch_time <= {current_time}) and (ids_threat_class IS NOT NULL) GROUP BY attacker_ip,target_ip,type_of_threat,sensor_name ORDER BY total_count desc"

                traceQueryCheck = opensearch_conn_using_db(trace_query, location_id, plan_id)
                trace_check_query_length = traceQueryCheck.get("total")

                trace_data_email = []
                # trace query data output
                if traceQueryCheck.get("total") is None:
                    trace_check_query_length = 0
                
                trace_key_names_email = []

                if trace_check_query_length > 0:

                    trace_key_mapping = {
                        "attacker_ip": 'Attacker IP',
                        "target_ip": 'Target IP',
                        "type_of_threat": 'Type of Threat',
                        "sensor_name": 'Sensor Name',
                        "count(*)": 'Count'
                    }

                    trace_key_names_email = [trace_key_mapping.get(n.get('name')) for n in traceQueryCheck.get('schema') if trace_key_mapping.get(n.get('name'))]
                        
                    for i in range(0, len(traceQueryCheck.get('datarows'))):
                        row = traceQueryCheck.get('datarows')[i]
                        trace_data_email.append(dict(zip(trace_key_names_email, row)))
                    email_data['Threat Reconnaissance And Classification Engine (TRACE)'] = trace_data_email

            if email_data is not None and len(email_data) >= 1: 
                
                time_for_template_dict = {1: "1 minute",
                                2: "2 minutes",
                                5: "5 minutes",
                                15: "15 minutes",
                                30: "30 minutes",
                                60: "1 hour",
                                360: "6 hours",
                                720: "12 hours",
                                1440: "24 hours"}

                if time_interval_val in time_for_template_dict:
                    time_interval_val = time_for_template_dict[time_interval_val]   

                send_email_from_app_multiple(email_ids,"Security Alert Notification",{"data":email_data,"send_time":time_interval_val,"agent_name":agent_name,"country":country,"state":state,"city":city},"frontend/alert_mail.html")
                # mail_send_status = send_email_from_app_multiple(email_ids,"Security Alert Notification",{"data":email_data,"send_time":time_interval_val,"agent_name":agent_name,"country":country,"state":state,"city":city},"frontend/alert_mail.html")
                # print(mail_send_status)

def notification_time_loop():
    while True:

        configs_data = helper_init_configs_mult("email_config_live")
        for rows in configs_data:
            email_id = rows.get('email_ids')

            if email_id is not None:
                active_agent_names = getAgentNameNotificationEmail(email_id.split(",")[0])                

            if active_agent_names:        
                if rows.get("time_interval_val") == None:
                    time_interval_val = 0
                else:
                    time_interval_val = int(rows.get("time_interval_val"))

            if time_interval_val > 0:
                notification_by_email(active_agent_names,rows.get("is_active"),rows.get("email_ids"),time_interval_val,rows.get("platform_val"),rows.get("id"),int(rows.get("time_interval_name")))
 
        time.sleep(60)# sleep time in seconds

notification_thread = threading.Thread(target = notification_time_loop)
sensor_alert_noti_threadobj = threading.Thread(target = sensor_alert_notification_time_loop)
ransomware_noti_thread = threading.Thread(target = ransomware_noti_time_loop)
notification_thread.start()

sensor_alert_noti_threadobj.daemon = True
sensor_alert_noti_threadobj.start()

ransomware_noti_thread.daemon = True
ransomware_noti_thread.start()