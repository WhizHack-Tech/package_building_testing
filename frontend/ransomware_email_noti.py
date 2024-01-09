#  ===========================================================================================================
#  File Name: ransomware_noti.py
#  Description: To send Email notifications if Ransomware found in Hids logs.

#  -----------------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  ===========================================================================================================

# HIDS Ransomware notifications
# after every "3 minutes" (fixed time) check if potential_ransomware_event = "true" --> if "yes" then send mail containing ransomware data
import threading, time, datetime
from .mail_to import send_email_from_app_multiple
from .views import opensearch_conn_using_db
from .helpers import helper_init_configs_mult,getAgentNameRansomwareEmailNoti, update_ransomware_epoch_time
from .time_filter_on_queries import ws_notification_start_end_epoch_time


def ransomware_email_notification(agent_data,ransomware_noti_is_active,email_ids,t_id,ransomware_noti_epoch): # ransomware_noti_epoch is the future epoch time which we store in init_config table, t_id is the object id in init_config table where we update ransomware_noti_epoch
    email_ids = email_ids.split(",")
    # print(f"time now:{datetime.datetime.now()}")
    # country = agent_data.get('country')
    # state = agent_data.get('state')
    # city = agent_data.get('city')
    location_id = agent_data.get('location_id')
    plan_id = agent_data.get('plan_id')
    email_data = {}


    # getting epoch_time values using different function #past_time (eg. last 3 min time in epoch format) and current_time is now time in epoch format
    past_time, current_time, future_time_epoch = ws_notification_start_end_epoch_time(3)

    if ransomware_noti_is_active == True:
        if (current_time > ransomware_noti_epoch):
            # update future time in db (eg. if default fixed time is 3 min then we find out epoch time after 3 min and update it in db)
            update_ransomware_epoch_time(t_id,future_time_epoch)

            # checking which agent is active accordingly creating query for that indice
            hids_alert_agent = agent_data['hids_alert_agent']
            hids_event_agent = agent_data['hids_event_agent']
            hids_incident_agent = agent_data['hids_incident_agent']

            for i,log_type_agent_name in enumerate([hids_alert_agent, hids_event_agent, hids_incident_agent]):

                # hids_query for the 3 different log_type
                hids_query = f"SELECT @timestamp, agent_ip, agent_name, syscheck_path, rule_description, rule_mitre_tactic, rule_mitre_technique FROM {log_type_agent_name}-* WHERE (attack_epoch_time >= {past_time} and attack_epoch_time <= {current_time}) AND (agent_ip IS NOT NULL) AND (agent_name IS NOT NULL) AND (syscheck_path IS NOT NULL) AND (rule_description IS NOT NULL) AND (rule_mitre_tactic IS NOT NULL) AND (rule_mitre_technique IS NOT NULL) AND potential_ransomware_event = 'true' ORDER BY attack_epoch_time desc;"

                hidsAlertQueryCheck = opensearch_conn_using_db(hids_query, location_id, plan_id)
                hids_alert_query_length = hidsAlertQueryCheck.get("total")
                hids_data_email = []
                # hids query data output
                if hidsAlertQueryCheck.get("total") is None:
                    hids_alert_query_length = 0
                
                hids_key_names_email = []

                if hids_alert_query_length > 0:

                    hids_key_mapping = {
                        "@timestamp": 'Timestamp',
                        "agent_ip": 'Agent IP',
                        "agent_name": 'Agent Name',
                        "syscheck_path": 'System Check Path',
                        "rule_description": 'Rule Description',
                        "rule_mitre_tactic": 'Rule Mitre Tactic',
                        "rule_mitre_technique": 'Rule Mitre Technique',
                    
                    }

                    hids_key_names_email = [hids_key_mapping.get(n.get('name')) for n in hidsAlertQueryCheck.get('schema') if hids_key_mapping.get(n.get('name'))]
                        
                    for i in range(0, len(hidsAlertQueryCheck.get('datarows'))):
                        row = hidsAlertQueryCheck.get('datarows')[i]
                        hids_data_email.append(dict(zip(hids_key_names_email, row)))
                    
                    for item in hids_data_email:
                        if "Timestamp" in item:
                            with_fractional_part = item.get('Timestamp')
                            item['Timestamp'] = with_fractional_part.split(".")[0]

                    if log_type_agent_name == hids_alert_agent:
                        email_data['Host Intrusion Detection System (HIDS) Alerts'] = hids_data_email
                    if log_type_agent_name == hids_event_agent:
                        email_data['Host Intrusion Detection System (HIDS) Events'] = hids_data_email
                    if log_type_agent_name == hids_incident_agent:
                        email_data['Host Intrusion Detection System (HIDS) Incidents'] = hids_data_email

            if email_data is not None and len(email_data) >= 1: 

                mail_send_status = send_email_from_app_multiple(email_ids,"Possible Ransomware Attack",{"data":email_data},"frontend/ransomware_email_noti.html")
                # mail_send_status = send_email_from_app_multiple(email_ids,"Security Alert Notification",{"data":email_data,"send_time":time_interval_val,"agent_name":agent_name,"country":country,"state":state,"city":city},"frontend/ransomware_email_noti.html")
                print(f"ransomware email noti mail status {mail_send_status}")


def ransomware_noti_time_loop():
    while True:
        configs_data = helper_init_configs_mult("email_config_live")
        for rows in configs_data:
            email_id = rows.get('email_ids')

            if email_id is not None:
                active_agent_names = getAgentNameRansomwareEmailNoti(email_id.split(",")[0])                

            if active_agent_names:
                t_id = rows.get("id")
                ransomware_email_notification(active_agent_names,rows.get("ransomware_noti_is_active"),rows.get("email_ids"),t_id,int(rows.get("ransomware_noti_epoch_val")))
 
        time.sleep(3*60)# sleep time in seconds....i.e,here sleep for 3 minutes applied


# if "ransomware_noti_is_active" is True and potential_ransomware_event = 'true': send mail
# if "ransomware_noti_is_active" is False and potential_ransomware_event = 'true': do not send mail