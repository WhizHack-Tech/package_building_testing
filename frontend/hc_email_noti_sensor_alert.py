#  ===========================================================================================================
#  File Name: hc_email_noti_sensor_alert.py
#  Description: To send Health Check email notifications for sensor alert on Client Dashboard.

#  -----------------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  ===========================================================================================================

# Health check sensor alert email notification
# after every 5 minutes check if level is "stopped"--> if "yes" then send mail
import threading
import time
from .mail_to import send_email_from_app_multiple
from .views import opensearch_conn_using_db
from .helpers import helper_init_configs_mult,getAgentNameSensorAlertNotiEmail


def sensor_alert_by_email(agent_data,is_active,email_ids, email_type):
    email_ids = email_ids.split(",")

    hc_indice_name = agent_data.get('hc_agent')
    location_id = agent_data.get('location_id')
    plan_id = agent_data.get('plan_id')
    org_name = agent_data.get('org_name')
    location_name = agent_data.get('location_name')
    
    sensor_alert_email_data = {}
    # health check query
    level_name = "stopped"
    hc_query = f"SELECT sensor_type, @timestamp, sensor_id, level, ram_utilization, cpu_utilization, disk_remaining FROM {hc_indice_name}-* WHERE level = '{level_name}' ORDER BY attack_epoch_time DESC;"

    run_hc_query = opensearch_conn_using_db(hc_query, location_id, plan_id)
    health_check_query_length = run_hc_query.get("total")

    # health check query data output
    if run_hc_query.get("total") is None:
        health_check_query_length = 0

    if health_check_query_length > 0:
        
        hc_key_mapping = {
                        "sensor_type": 'Sensor Type',
                        "@timestamp": 'Timestamp',
                        "sensor_id": 'Sensor ID',
                        "level": 'Level',
                        "ram_utilization": "RAM Utilization",
                        "cpu_utilization": "CPU Utilization",
                        "disk_remaining": "Disk Remaining"
                    }

        key_names = [hc_key_mapping.get(n.get('name')) for n in run_hc_query.get('schema') if hc_key_mapping.get(n.get('name'))]

        hc_data_email = []
        for i, row in enumerate(run_hc_query.get('datarows')):
            Dict = {"Organization Name":org_name, "Location Name":location_name}
            Dict.update(dict(zip(key_names, row)))
            hc_data_email.append(Dict)

        for item in hc_data_email:
            if "Timestamp" in item:
                with_fractional_part = item.get('Timestamp')
                item['Timestamp'] = with_fractional_part.split(".")[0]

        sensor_alert_email_data['Health Check Data'] = hc_data_email
        
        if email_type == "client" and is_active == False:
            pass
        else:
            # send mail
            # mail_send_status = send_email_from_app_multiple(email_ids,"Health Check Sensor Alert Notification",{"data":sensor_alert_email_data, "level_name": level_name},"frontend/hc_sensor_alert.html")
            # print(mail_send_status)
            send_email_from_app_multiple(email_ids,"Health Check Sensor Alert Notification",{"data":sensor_alert_email_data, "level_name": level_name},"frontend/hc_sensor_alert.html")


def sensor_alert_notification_time_loop():
    while True:
        configs_data = helper_init_configs_mult("email_config_live")
        for rows in configs_data:
            client_email_id = rows.get('sensor_alert_client')
            admin_email_id = rows.get('sensor_alert_admin')

            if (client_email_id is not None):
                active_agent_names = getAgentNameSensorAlertNotiEmail(client_email_id.split(",")[0])
                email_type = "client"
                if (active_agent_names is not None):
                    sensor_alert_by_email(active_agent_names,rows.get("is_active"),client_email_id, email_type)
            
            if (admin_email_id is not None):
                active_agent_names = getAgentNameSensorAlertNotiEmail(admin_email_id.split(",")[0])
                email_type = "admin"
                if (active_agent_names is not None):
                    sensor_alert_by_email(active_agent_names,rows.get("is_active"),admin_email_id, email_type)

        time.sleep(5*60)# sleep time in seconds....i.e,here sleep for 5 minutes applied
 



# for admin--> dont check "is_active" is True or not
# for client--> first check "is_active" is True then send mail
# if "is_active" is True: send mail to admin, client
# if "is_active" is False: send mail to admin