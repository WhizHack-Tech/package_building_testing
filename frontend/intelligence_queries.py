#  ==================================================================================================
#  File Name: intelligence_queries.py
#  Description: This file contains code for each chart on intelligence page of Client Dashboard. Intelligence page is currently not active on dashboard.
#  ---------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  ====================================================================================================

from .opensearch_config import query

# list containing values to exclude from each query--> to avoid error on frontend page
exclude_values = [0,None]

# Top Victim IP addresses(intelligence page)
def Top_Victim_Ip_addresses(agent_name, start_date, end_date, platform, severity):
    formed_sql = f"SELECT target_ip,target_mac_address,count(target_ip) count FROM {agent_name}-* WHERE target_mac_address IS NOT NULL AND target_ip IS NOT NULL AND DATE_FORMAT(@timestamp,'%Y-%m-%d') >= '{start_date}' AND DATE_FORMAT(@timestamp,'%Y-%m-%d') <= '{end_date}' AND platform IN ({platform}) AND ids_threat_severity IN ({severity}) GROUP BY target_ip,target_mac_address ORDER BY count DESC LIMIT 7;"
    api_response = query(formed_sql)
    
    # print("Top victim ip addr---intelligence page query:",formed_sql)
    if api_response.get("total") not in exclude_values:
        key_names = []
        for i in range(len(api_response.get('schema'))):
            key_names.append(api_response.get('schema')[i].get('name'))
        final_response = []
        for i in range(len(api_response.get('datarows'))):
            row = api_response.get('datarows')[i]
            final_response.append(dict(zip(key_names, row)))
        return final_response
    else:
        return 0 

# Top Attacking IPs(intelligence page)
def Top_Attacking_IPs(agent_name, start_date, end_date, platform, severity):
    api_response = query(
        f"SELECT attacker_ip,attacker_mac,count(attacker_ip) count FROM {agent_name}-* WHERE attacker_mac IS NOT NULL AND DATE_FORMAT(@timestamp,'%Y-%m-%d') >= '{start_date}' AND DATE_FORMAT(@timestamp,'%Y-%m-%d') <= '{end_date}' AND platform IN ({platform}) AND ids_threat_severity IN ({severity}) GROUP BY attacker_ip,attacker_mac ORDER BY count DESC LIMIT 7;")
    
    if api_response.get("total") not in exclude_values:
        key_names = []
        for i in range(len(api_response.get('schema'))):
            key_names.append(api_response.get('schema')[i].get('name'))
        final_response = []
        for i in range(len(api_response.get('datarows'))):
            row = api_response.get('datarows')[i]
            final_response.append(dict(zip(key_names, row)))
        return final_response
    else:
        return 0

 
# Fastest Attackers(intelligence page)
def Fastest_Attackers(agent_name, start_date, end_date, platform, severity):
    api_response = query(
        f"SELECT attacker_ip,service_name,count(service_name) count FROM {agent_name}-* WHERE attacker_mac IS NOT NULL  AND DATE_FORMAT(@timestamp,'%Y-%m-%d') >= '{start_date}' AND DATE_FORMAT(@timestamp,'%Y-%m-%d') <= '{end_date}' AND platform IN ({platform}) AND ids_threat_severity IN ({severity}) GROUP BY attacker_ip,service_name ORDER BY count DESC LIMIT 7;")
    if api_response.get("total") not in exclude_values:
        key_names = []
        for i in range(len(api_response.get('schema'))):
            key_names.append(api_response.get('schema')[i].get('name'))
        final_response = []
        for i in range(len(api_response.get('datarows'))):
            row = api_response.get('datarows')[i]
            final_response.append(dict(zip(key_names, row)))
        return final_response
    else:
        return 0


# Geolocation Data(intelligence page)without any count
def Geolocation_Data(agent_name, start_date, end_date, platform, severity):
    api_response = query(
        f"SELECT attacker_ip,attacker_mac,DATE_FORMAT(@timestamp,'%Y-%m-%d'),geoip_asn_name,geoip_city FROM {agent_name}-* WHERE attacker_mac IS NOT NULL AND geoip_asn_name IS NOT NULL AND geoip_city IS NOT NULL AND DATE_FORMAT(@timestamp,'%Y-%m-%d') >= '{start_date}' AND DATE_FORMAT(@timestamp,'%Y-%m-%d') <= '{end_date}' AND platform IN ({platform}) AND ids_threat_severity IN ({severity}) limit 7 ;")
    if api_response.get("total") not in exclude_values:
        key_names = []
        for i in range(len(api_response.get('schema'))):
            key_names.append(api_response.get('schema')[i].get('name'))
        final_response = []
        for i in range(len(api_response.get('datarows'))):
            row = api_response.get('datarows')[i]
            final_response.append(dict(zip(key_names, row)))
        return final_response
    else:
        return 0 

# Victim tcp services attacked(intelligence page)repeat mac AND ip
def Victimtcp_servicesattacked(agent_name, start_date, end_date, platform, severity):
    api_response = query(
        f"SELECT target_ip,target_mac_address,tcp_port, count(target_ip)count FROM {agent_name}-* WHERE target_ip IS NOT NULL AND tcp_port IS NOT NULL AND DATE_FORMAT(@timestamp,'%Y-%m-%d') >= '{start_date}' AND DATE_FORMAT(@timestamp,'%Y-%m-%d') <= '{end_date}' AND platform IN ({platform}) AND ids_threat_severity IN ({severity}) GROUP BY target_ip,target_mac_address,tcp_port ORDER BY count DESC LIMIT 7;")
    if api_response.get("total") not in exclude_values:
        key_names = []
        for i in range(len(api_response.get('schema'))):
            key_names.append(api_response.get('schema')[i].get('name'))
        final_response = []
        for i in range(len(api_response.get('datarows'))):
            row = api_response.get('datarows')[i]
            final_response.append(dict(zip(key_names, row)))
        return final_response
    else:
        return 0

# Victim udp services attacked(intelligence page)repeat mac AND ip with count
def Victim_udp_services_attacked(agent_name, start_date, end_date, platform, severity):
    api_response = query(
        f"SELECT target_ip,target_mac_address,udp_port, count(target_ip) count FROM {agent_name}-* WHERE target_ip IS NOT NULL AND udp_port IS NOT NULL AND DATE_FORMAT(@timestamp,'%Y-%m-%d') >= '{start_date}' AND DATE_FORMAT(@timestamp,'%Y-%m-%d') <= '{end_date}' AND platform IN ({platform}) AND ids_threat_severity IN ({severity}) GROUP BY target_ip,target_mac_address,udp_port ORDER BY count DESC LIMIT 7;")
    if api_response.get("total") not in exclude_values:
        key_names = []
        for i in range(len(api_response.get('schema'))):
            key_names.append(api_response.get('schema')[i].get('name'))
        final_response = []
        for i in range(len(api_response.get('datarows'))):
            row = api_response.get('datarows')[i]
            final_response.append(dict(zip(key_names, row)))
        return final_response
    else:
        return 0  

# Top Attack Types (Victims)(intelligence page)repeat mac AND ip with count
def Top_Attack_Types_Victims(agent_name, start_date, end_date, platform, severity):
    api_response = query(
        f"SELECT target_ip,target_mac_address,type_of_threat, count(target_ip) count FROM {agent_name}-* WHERE target_ip IS NOT NULL AND type_of_threat IS NOT NULL AND DATE_FORMAT(@timestamp,'%Y-%m-%d') >= '{start_date}' AND DATE_FORMAT(@timestamp,'%Y-%m-%d') <= '{end_date}' AND platform IN ({platform}) AND ids_threat_severity IN ({severity}) GROUP BY target_ip,target_mac_address,type_of_threat ORDER BY count DESC LIMIT 7;")
    if api_response.get("total") not in exclude_values:
        key_names = []
        for i in range(len(api_response.get('schema'))):
            key_names.append(api_response.get('schema')[i].get('name'))
        final_response = []
        for i in range(len(api_response.get('datarows'))):
            row = api_response.get('datarows')[i]
            final_response.append(dict(zip(key_names, row)))
        return final_response
    else:
        return 0 

# Top Attacker Types (Attackers)(intelligence page)repeat mac AND ip
def Top_Attack_Types_Attackers(agent_name, start_date, end_date, platform, severity):
    api_response = query(
        f"SELECT attacker_ip,attacker_mac,type_of_threat, count(attacker_ip) count FROM {agent_name}-* WHERE attacker_ip IS NOT NULL AND type_of_threat IS NOT NULL  AND DATE_FORMAT(@timestamp,'%Y-%m-%d') >= '{start_date}' AND DATE_FORMAT(@timestamp,'%Y-%m-%d') <= '{end_date}' AND platform IN ({platform}) AND ids_threat_severity IN ({severity}) GROUP BY attacker_ip,attacker_mac,type_of_threat ORDER BY count DESC LIMIT 7;")
    if api_response.get("total") not in exclude_values:
        key_names = []
        for i in range(len(api_response.get('schema'))):
            key_names.append(api_response.get('schema')[i].get('name'))
        final_response = []
        for i in range(len(api_response.get('datarows'))):
            row = api_response.get('datarows')[i]
            final_response.append(dict(zip(key_names, row)))
        return final_response
    else:
        return 0 