#  ==================================================================================================================================================================
#  File Name: mldldetection_queries.py
#  Description: This file contains code for each chart on ml-dl-detection page of Client Dashboard. ml-dl-detection page is currently not active on dashboard.
#  -------------------------------------------------------------------------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  ====================================================================================================================================================================

from .opensearch_config import query

# list containing values to exclude from each query--> to avoid error on frontend page
exclude_values = [0,None]

 
ml_threat_list = ("A Network Trojan was detected", "Attempted Administrator Privilege Gain", "Successful Administrator Privilege Gain", "Attempted Denial of Service", "Attempted Information Leak", "Detection of a Denial of Service Attack", "Detection of a Network Scan", "Exploit Kit Activity Detected")

dl_threat_list = ("A Network Trojan was detected", "Attempted Denial of Service", "Attempted Information Leak", "Attempted User Privilege Gain", "Detection of a Network Scan")
 
# ml_threat_list = ('A Network Trojan was detected', 'Successful Administrator Privilege Gain', 'Attempted Denial of Service', 'Attempted Information Leak', 'Detection of a Denial of Service Attack', 'Exploit Kit Activity Detected')

# dl_threat_list = ('A Network Trojan was detected', 'Attempted Denial of Service', 'Attempted Information Leak', 'Attempted User Privilege Gain', 'Detection of a Network Scan')

# 1 Threat Logs card
def test_page_table(agent_name,start_date,end_date,platform,accuracy1, accuracy2):
    
    formed_sql = f"SELECT DATE_FORMAT(@timestamp, '%Y-%m-%d %h:%m:%s') @timestamp, attack_os, target_os, attacker_ip, attacker_mac, platform, target_ip, target_mac_address, ml_threat_class, dl_threat_class, ml_accuracy, dl_accuracy FROM {agent_name}-* WHERE ids_threat_severity IS NULL AND ml_threat_class NOT IN ('not alert') AND ml_threat_class in {ml_threat_list} AND dl_threat_class in {dl_threat_list} AND (ml_accuracy>{accuracy1}) AND (ml_accuracy<={accuracy2}) AND DATE_FORMAT(@timestamp, '%Y-%m-%d') >= '{start_date}' AND DATE_FORMAT(@timestamp, '%Y-%m-%d') <= '{end_date}' AND platform IN ({platform});"
 
    # print("table query---->mldldetection page", formed_sql)
    sql_query = query(formed_sql)
    # print(f"query o/p:{sql_query}")
    final_response = 0
   
    if sql_query.get("total") not in exclude_values:
        key_names = []
        for i in range(len(sql_query.get('schema'))):
            if i==0:
                key_names.append(sql_query.get('schema')[i].get('alias'))
            else:
                key_names.append(sql_query.get('schema')[i].get('name'))
        final_response = []
        for i in range(len(sql_query['datarows'])):
            row = sql_query.get('datarows')[i]
            final_response.append(dict(zip(key_names, row)))
        for i in range(len(final_response)):
            if final_response[i]['ml_threat_class'] == None:
                final_response[i]['ml_threat_class'] = "not alert"
            if final_response[i]['dl_threat_class'] == None:
                final_response[i]['dl_threat_class'] = "not alert"
    return final_response

# 2 High Severity Events count card
# (displays total of--->internal,external, lateral movements attack)
def critical_threats_count(agent_name,start_date,end_date,platform,accuracy1, accuracy2):    
    sql_query = f"SELECT COUNT(type_of_threat) FROM {agent_name}-* WHERE type_of_threat IS NOT NULL AND ids_threat_severity IS NULL AND ml_threat_class IN {ml_threat_list} AND ml_threat_class NOT IN ('not alert', 'Normal Traffic', 'None', 'null') AND dl_threat_class IN {dl_threat_list} AND dl_threat_class NOT IN ('not alert', 'null', 'Normal Traffic', 'None') AND (ml_accuracy>{accuracy1}) AND (ml_accuracy<={accuracy2}) AND DATE_FORMAT(@timestamp, '%Y-%m-%d') >= '{start_date}' AND DATE_FORMAT(@timestamp, '%Y-%m-%d') <= '{end_date}' AND platform IN ({platform});"
    #qu = f"SELECT COUNT(type_of_threat) FROM {agent_name}-* WHERE type_of_threat IS NOT NULL AND ids_threat_severity IS NULL AND ml_threat_class NOT IN ('not alert') AND dl_threat_class NOT IN ('not alert', 'null') AND (ml_accuracy>{accuracy1}) AND (ml_accuracy<={accuracy2}) AND (dl_accuracy>{accuracy1}) AND (dl_accuracy<={accuracy2}) AND DATE_FORMAT(@timestamp, '%Y-%m-%d') >= '{start_date}' AND DATE_FORMAT(@timestamp, '%Y-%m-%d') <= '{end_date}' AND platform IN ({platform});"
    severity1_attack_count = query(sql_query)
    # print(f"critical threats count:{sql_query}")
    severity_count_filter = 0
 
    if severity1_attack_count.get("total") not in exclude_values:
        count_str = str(severity1_attack_count['datarows'])[2:-2]
        severity_count_filter = int(count_str)
    return severity_count_filter

# 3 Lateral movements attack count card
def lateral_attack_count(agent_name,start_date,end_date,platform,accuracy1, accuracy2):    
    lateral_attack_count = query(f"SELECT COUNT(type_of_threat) FROM {agent_name}-* WHERE type_of_threat = 'Lateral Movement' AND platform IN ({platform}) AND ids_threat_severity IS NULL AND ml_threat_class IN {ml_threat_list} AND dl_threat_class IN {dl_threat_list} AND (ml_accuracy>{accuracy1}) AND (ml_accuracy<={accuracy2}) AND DATE_FORMAT(@timestamp, '%Y-%m-%d') >= '{start_date}' AND DATE_FORMAT(@timestamp, '%Y-%m-%d') <= '{end_date}';")
    # print("lateral_attack_func",lateral_attack_count)
    if lateral_attack_count.get("total") not in exclude_values:
        count_str = str(lateral_attack_count['datarows'])[2:-2]
        mov_count_filter = int(count_str)
    else:
        mov_count_filter = 0
    return mov_count_filter

# 4 Internal Attack Count Card-->Compromised Host Activity 
def internalCompromised_attack_count(agent_name,start_date,end_date,platform,accuracy1, accuracy2):    
    internalCompromised_attack_count = query(f"SELECT COUNT(type_of_threat) FROM {agent_name}-* WHERE type_of_threat = 'Internal Compromised Machine' AND platform IN ({platform}) AND ids_threat_severity IS NULL AND ml_threat_class IN {ml_threat_list} AND dl_threat_class IN {dl_threat_list} AND (ml_accuracy>{accuracy1}) AND (ml_accuracy<={accuracy2}) AND DATE_FORMAT(@timestamp, '%Y-%m-%d') >= '{start_date}' AND DATE_FORMAT(@timestamp, '%Y-%m-%d') <= '{end_date}';")
    # print("internalCompromised_attack_func",internalCompromised_attack_count)
    if internalCompromised_attack_count.get("total") not in exclude_values:
        count_str = str(internalCompromised_attack_count['datarows'])[2:-2]
        com_count_filter = int(count_str)
    else:
        com_count_filter = 0
    return com_count_filter

# 5 External Attacks count card
def external_attack_count(agent_name,start_date,end_date,platform,accuracy1, accuracy2):
    external_attack_count = query(f"SELECT count(type_of_threat) FROM {agent_name}-* WHERE type_of_threat IN ('External Attack', 'Attack on External Server') AND ids_threat_severity IS NULL AND ml_threat_class IN {ml_threat_list} AND dl_threat_class IN {dl_threat_list} AND (ml_accuracy>{accuracy1}) AND (ml_accuracy<={accuracy2}) AND DATE_FORMAT(@timestamp, '%Y-%m-%d') >= '{start_date}' AND DATE_FORMAT(@timestamp, '%Y-%m-%d') <= '{end_date}' AND platform IN ({platform});")
 
    # print("external_attack_count_func", external_attack_count)
    eat_count_filter = 0
 
    if external_attack_count.get("total") not in exclude_values:
        count_str = str(external_attack_count['datarows'])[2:-2]
        eat_count_filter = int(count_str)
    return eat_count_filter

# 6 Top Attacker Cities card
def Geoip_city_count(agent_name, start_date, end_date, platform, accuracy1, accuracy2):
    query_output = query(f"SELECT t.geoip_city, COUNT(t.geoip_city) count FROM {agent_name}-* as t WHERE t.geoip_city IS NOT NULL and t.ids_threat_severity IS NULL and t.ml_threat_class IN {ml_threat_list} and dl_threat_class IN {dl_threat_list} and (t.ml_accuracy>{accuracy1}) and (t.ml_accuracy<={accuracy2}) and DATE_FORMAT(@timestamp,'%Y-%m-%d') >= '{start_date}' and DATE_FORMAT(@timestamp,'%Y-%m-%d') <= '{end_date}' and t.platform IN ({platform}) GROUP BY t.geoip_city ORDER BY count DESC LIMIT 7;")
    # print("Geoipcityname", query_output)
    if query_output.get("total") not in exclude_values:
        list1, list2 = map(list, zip(*query_output['datarows']))
        required_dict = {"series": list2, "labels": list1}
    else:
        required_dict = {"series": ["null"], "labels": ["null"]}
    return required_dict

# 7 Top Source Attack Countries card
def geoip_country_count(agent_name, start_date, end_date, platform, accuracy1, accuracy2):
    query_output = query(f"SELECT t.geoip_country_name, COUNT(t.geoip_country_name) count FROM {agent_name}-* as t WHERE t.geoip_country_name IS NOT NULL and t.ids_threat_severity IS NULL and t.ml_threat_class IN {ml_threat_list} and dl_threat_class IN {dl_threat_list} and (t.ml_accuracy>{accuracy1}) and (t.ml_accuracy<={accuracy2}) and DATE_FORMAT(@timestamp,'%Y-%m-%d') >= '{start_date}' and DATE_FORMAT(@timestamp,'%Y-%m-%d') <= '{end_date}' and t.platform IN ({platform}) GROUP BY t.geoip_country_name ORDER BY count DESC LIMIT 7;")
    # print("CountryCount:", query_output)
    if query_output.get("total") not in exclude_values:
        list1, list2 = map(list, zip(*query_output['datarows']))
        required_dict = {"series": list2, "labels": list1}
    else:
        required_dict = {"series": ["null"], "labels": ["null"]}
    return required_dict

# 8 Top Attacker ASN card
def Asn_count_func(agent_name, start_date, end_date, platform, accuracy1, accuracy2):
    query_output = query(f"SELECT t.geoip_asn_name, COUNT(t.geoip_asn_name) count FROM {agent_name}-* as t WHERE t.geoip_asn_name IS NOT NULL and t.ids_threat_severity IS NULL and t.ml_threat_class IN {ml_threat_list} and t.dl_threat_class IN {dl_threat_list} and (t.ml_accuracy>{accuracy1}) and (t.ml_accuracy<={accuracy2}) and DATE_FORMAT(@timestamp,'%Y-%m-%d') >= '{start_date}' and DATE_FORMAT(@timestamp,'%Y-%m-%d') <= '{end_date}' and t.platform IN ({platform}) GROUP BY t.geoip_asn_name ORDER BY count DESC LIMIT 7;")
    # print("AsnCount:", query_output)
    if query_output.get("total") not in exclude_values:
        list1, list2 = map(list, zip(*query_output['datarows']))
        required_dict = {"series": list2, "labels": list1}
    else:
        required_dict = {"series": ["null"], "labels": ["null"]}
    return required_dict

# 9 Ports (Attack Event page)
def Tcp_port_count_func(agent_name, start_date, end_date, platform, accuracy1, accuracy2):
    query_output = query(f"SELECT t.tcp_port, count(t.tcp_port) count FROM {agent_name}-* as t WHERE t.tcp_port IS NOT NULL and t.ids_threat_severity IS NULL and t.ml_threat_class IN {ml_threat_list} and t.dl_threat_class IN {dl_threat_list} and (t.ml_accuracy>{accuracy1}) and (t.ml_accuracy<={accuracy2}) and DATE_FORMAT(@timestamp,'%Y-%m-%d') >= '{start_date}' and DATE_FORMAT(@timestamp,'%Y-%m-%d') <= '{end_date}' and t.platform IN ({platform}) GROUP BY t.tcp_port ORDER BY count desc LIMIT 7;")
    # print("TcpCount", query_output)
    if query_output.get("total") not in exclude_values:
        list1, list2 = map(list, zip(*query_output['datarows']))
        required_dict = {"series": list2, "labels": list1}
    else:
        required_dict = {"series": ["null"], "labels": ["null"]}
    return required_dict

# 10 Attacker MAC Addresses(Attack Event page)
def Attacker_Mac_Addresses(agent_name, start_date, end_date, platform, accuracy1, accuracy2):
    query_output = query(f"SELECT t.target_mac_address, COUNT(t.target_mac_address) count FROM {agent_name}-* as t WHERE t.target_mac_address IS NOT NULL and t.ids_threat_severity IS NULL and t.ml_threat_class IN {ml_threat_list} and (t.ml_accuracy>{accuracy1}) and t.dl_threat_class IN {dl_threat_list} and (t.ml_accuracy<={accuracy2}) and DATE_FORMAT(@timestamp,'%Y-%m-%d') >= '{start_date}' and DATE_FORMAT(@timestamp,'%Y-%m-%d') <= '{end_date}' and t.platform IN ({platform}) GROUP BY t.target_mac_address ORDER BY count DESC LIMIT 7;")
    # print("FrequentAttackerMackAddresses:",query_output)
    if query_output.get("total") not in exclude_values:
        list1, list2 = map(list, zip(*query_output['datarows']))
        required_dict = {"series": list2, "labels": list1}
    else:
        required_dict = {"series": ["null"], "labels": ["null"]}
    return required_dict

# 11 Attack Frequency card--> displays frequency of attacks 
def Frequency_of_attacks_func(agent_name, start_date, end_date, platform, accuracy1, accuracy2):
    SQL_query = query(f"SELECT DATE_FORMAT(@timestamp, '%Y-%m-%d') Date, count(*) FROM {agent_name}-* WHERE ids_threat_severity IS NULL and ml_threat_class IN {ml_threat_list} and dl_threat_class IN {dl_threat_list} and (ml_accuracy>{accuracy1}) and (ml_accuracy<={accuracy2}) and DATE_FORMAT(@timestamp,'%Y-%m-%d') >= '{start_date}' and DATE_FORMAT(@timestamp,'%Y-%m-%d') <= '{end_date}' and platform IN ({platform}) GROUP BY DATE_FORMAT(@timestamp,'%Y-%m-%d') ORDER BY DATE_FORMAT(@timestamp, '%Y-%m-%d');")
    # print("FrequencyOfAttacks:", SQL_query)
    if SQL_query.get("total") not in exclude_values:
        Dates, count_of_attacks = map(list, zip(*SQL_query['datarows']))
        required_dict = {"categories": Dates, "series": count_of_attacks}
    else:
        required_dict = {"categories": ["null"], "series": ["null"]}
    return required_dict

# 12 Top Attacked Services card -->Service Name to count groub by query by baby
def Service_Name_func(agent_name, start_date, end_date, platform, accuracy1, accuracy2):
    api_response = query(f"SELECT service_name, count(service_name) count FROM {agent_name}-* WHERE service_name NOT LIKE 'NA' and ids_threat_severity IS NULL and ml_threat_class IN {ml_threat_list} and dl_threat_class IN {dl_threat_list} and (ml_accuracy>{accuracy1}) and (ml_accuracy<={accuracy2}) and DATE_FORMAT(@timestamp,'%Y-%m-%d') >= '{start_date}' and DATE_FORMAT(@timestamp,'%Y-%m-%d') <= '{end_date}' and platform IN ({platform}) GROUP BY service_name ORDER BY count DESC LIMIT 12;")
    service_name_count = []
    if api_response.get("total") not in exclude_values:
        service_name,service_count= map(list, zip(*api_response['datarows']))
        for (key, value) in zip(service_name,service_count):
            dict = {}
            dict.update({"name":key, "val":value})
            service_name_count.append(dict)
    return service_name_count

g = globals()
# Attacker IPs Card --->"Attacker IPs" count by date in series, seriesname & label format----top 7 on basis of count 

def Attacker_IP_count_func(agent_name, start_date, end_date, platform, accuracy1, accuracy2):
    # find attacker_ip with max count
    search1 = query(f"SELECT attacker_ip,count(attacker_ip) count FROM {agent_name}-* WHERE attacker_ip IS NOT NULL and ids_threat_severity IS NULL and ml_threat_class IN {ml_threat_list} and dl_threat_class IN {dl_threat_list} and (ml_accuracy>{accuracy1}) and (ml_accuracy<={accuracy2}) and DATE_FORMAT(@timestamp,'%Y-%m-%d') >= '{start_date}' and DATE_FORMAT(@timestamp,'%Y-%m-%d') <= '{end_date}' and platform IN ({platform}) GROUP BY attacker_ip ORDER BY count desc LIMIT 7;")
    # print("AttackerIPCount--finding top7 attacker ip:",search1 )
    if search1.get("total") not in exclude_values:
        unique_IP, list2 = map(list, zip(*search1['datarows']))
        attacker_ip_tuple = tuple(unique_IP)
        updated_tuple = attacker_ip_tuple
        if len(attacker_ip_tuple) == 1:
            updated_tuple = attacker_ip_tuple+('0',)
    else:
        nd = {"series1": ["null"], "series1name": "null", "series2": ["null"], "series2name": "null", "series3": ["null"], "series3name": "null",  "series4": ["null"], "series4name": "null",  "series5": ["null"], "series5name": "null",  "series6": ["null"], "series6name": "null",  "series7": ["null"], "series7name": "null", "labels": ["null"]}
        return nd

    # date wise count of a single attacker_ip
    search2 = query(f"SELECT attacker_ip, DATE_FORMAT(@timestamp,'%Y-%m-%d'),count(attacker_ip) count FROM {agent_name}-* WHERE attacker_ip IN {updated_tuple} and ids_threat_severity IS NULL and ml_threat_class IN {ml_threat_list} and dl_threat_class IN {dl_threat_list} and (ml_accuracy>{accuracy1}) and (ml_accuracy<={accuracy2}) and DATE_FORMAT(@timestamp,'%Y-%m-%d') >= '{start_date}' and DATE_FORMAT(@timestamp,'%Y-%m-%d') <= '{end_date}' and platform IN ({platform}) GROUP BY DATE_FORMAT(@timestamp,'%Y-%m-%d'),attacker_ip ORDER BY DATE_FORMAT(@timestamp,'%Y-%m-%d');")
    # print("AttackerIPCount--datewise count of attacker ip:", search2)
    if search2.get("total") not in exclude_values:
        Attacker_IP, Dates, individual_ip_counts = map(list, zip(*search2['datarows']))
        # removing redundant elements from list with dates
        unique_dates = list(dict.fromkeys(Dates))

        n = len(unique_dates)
        same_ip_clubbed_together = []
        for u in range(len(unique_IP)):
            inner_list = []
            for i in range(len(search2['datarows'])):
                if unique_IP[u] == search2['datarows'][i][0]:
                    inner_list.append(search2['datarows'][i])
            same_ip_clubbed_together.append(inner_list)

        number_of_IPs = len(same_ip_clubbed_together)
        for i in range(number_of_IPs):
            g['IP_{0}'.format(i)] = same_ip_clubbed_together[i]

        no_of_dates = len(unique_dates)
        for j in range(number_of_IPs):
            g['IP_{0}_count'.format(j)] = ['']*no_of_dates

        for k in range(number_of_IPs):
            for i in range(len(g['IP_{0}'.format(k)])):
                for j in range(len(unique_dates)):
                    if unique_dates[j] == g['IP_{0}'.format(k)][i][1]:
                        g['IP_{0}_count'.format(
                            k)][j] = g['IP_{0}'.format(k)][i][2]

        for k in range(number_of_IPs):
            for i in range(len(g['IP_{0}_count'.format(k)])):
                if g['IP_{0}_count'.format(k)][i] == "":
                    g['IP_{0}_count'.format(k)][i] = None

        nd = {}
        for k in range(number_of_IPs):
            nd[f"series{k+1}"] = g['IP_{0}_count'.format(k)]
            nd[f"series{k+1}name"] = unique_IP[k]

        nd.update({"labels": unique_dates})
        return nd
    else:
        nd = {"series1": ["null"], "series1name": "null", "series2": ["null"], "series2name": "null", "series3": ["null"], "series3name": "null",  "series4": ["null"], "series4name": "null",  "series5": ["null"], "series5name": "null",  "series6": ["null"], "series6name": "null",  "series7": ["null"], "series7name": "null", "labels": ["null"]}
        return nd

#14 Detected Threat Type Card (i) ML --> To count all ml threat class of values and keys #9
def Ml_Threat_Count(agent_name,start_date,end_date,platform,accuracy1, accuracy2):    
    api_response=query(f"SELECT ml_threat_class, count(ml_threat_class) count FROM {agent_name}-* WHERE ml_threat_class IS NOT NULL and ml_threat_class IN {ml_threat_list} and dl_threat_class IN {dl_threat_list} and ids_threat_severity IS NULL and (ml_accuracy>{accuracy1}) and (ml_accuracy<={accuracy2}) and platform IN ({platform}) and DATE_FORMAT(@timestamp, '%Y-%m-%d') >= '{start_date}' and DATE_FORMAT(@timestamp, '%Y-%m-%d') <= '{end_date}' GROUP BY ml_threat_class ORDER BY count desc LIMIT 7")
    temp_ml_threat_list = []
    if api_response.get("total") not in exclude_values:
        ml_threat_class_name,ml_threat_class_count= map(list, zip(*api_response['datarows']))
        for (key, value) in zip(ml_threat_class_name,ml_threat_class_count):
            dict = {}
            dict.update({"name":key,"val":value})
            temp_ml_threat_list.append(dict)
    return temp_ml_threat_list

#15 Detected Threat Type Card (i) DL-->To count all dl threat class of values and keys #10
def Dl_Threat_Count(agent_name,start_date,end_date,platform,accuracy1, accuracy2):
    api_response=query(f"SELECT dl_threat_class, count(dl_threat_class) count FROM {agent_name}-* WHERE dl_threat_class IS NOT NULL and dl_threat_class !='undefined class' and ml_threat_class IN {ml_threat_list} and dl_threat_class IN {dl_threat_list} and ids_threat_severity IS NULL and (ml_accuracy>{accuracy1}) and (ml_accuracy<={accuracy2}) and platform IN ({platform}) and DATE_FORMAT(@timestamp, '%Y-%m-%d') >= '{start_date}' and DATE_FORMAT(@timestamp, '%Y-%m-%d') <= '{end_date}' GROUP BY dl_threat_class ORDER BY count desc LIMIT 7")
    dl_threat_temp_list = []
    if api_response.get("total") not in exclude_values:
        dl_threat_class_name,dl_threat_class_count= map(list, zip(*api_response['datarows']))  
        for (key, value) in zip(dl_threat_class_name,dl_threat_class_count):
            dict = {}
            dict.update({"name":key,"val":value})
            dl_threat_temp_list.append(dict)
    return dl_threat_temp_list