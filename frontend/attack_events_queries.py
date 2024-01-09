#  ===========================================================================================================================================================================================
#  File Name: attack_events_queries.py
#  Description: It contains all the code for each chart on NIDS Attack Events page on Client Dashboard. Currently NIDS Attack Events page is not active on Client Dashboard.

#  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  ===========================================================================================================================================================================================

from .opensearch_config import query
from .helpers import strToComma

# list containing values to exclude from each query--> to avoid error on frontend page
exclude_values = [0,None]
# Attacker City(Attack Event page)
def Geoip_city_name(agent_name, start_date, end_date, platform, severity):
    formed_sql = f"SELECT t.geoip_city, COUNT(t.geoip_city) count FROM {agent_name}-* as t WHERE t.geoip_city IS NOT NULL AND DATE_FORMAT(@timestamp,'%Y-%m-%d') >= '{start_date}' AND DATE_FORMAT(@timestamp,'%Y-%m-%d') <= '{end_date}' and platform IN ({platform}) and ids_threat_severity IN ({severity}) GROUP BY t.geoip_city ORDER BY count DESC LIMIT 7;"
    query_output = query(formed_sql)
    # print("Attack events page--> Geoipcityname", formed_sql)
    if query_output.get("total") not in exclude_values:
        list1, list2 = map(list, zip(*query_output['datarows']))
        required_dict = {"series": list2, "labels": list1}
    else:
        required_dict = {"series": ["null"], "labels": ["null"]}
    return required_dict

# Attacker Locations(Attack Event page)
def Attacker_Locations_Timestamp(agent_name, start_date, end_date, platform, severity):
    search = query(f"SELECT t.geoip_city, t.geoip_latitude,t.geoip_longitude, count(*) count FROM {agent_name}-* as t WHERE t.geoip_country_name IS NOT  NULL AND t.geoip_latitude IS NOT NULL AND t.geoip_longitude IS NOT NULL AND DATE_FORMAT(@timestamp,'%Y-%m-%d') >= '{start_date}' AND DATE_FORMAT(@timestamp,'%Y-%m-%d') <= '{end_date}' and platform IN ({platform}) and ids_threat_severity IN ({severity}) GROUP BY t.geoip_city,t.geoip_latitude,t.geoip_longitude ORDER BY count desc  LIMIT 50;")
    # print("AttackerLocationsTimestamp", search)
    d2 = []
    if search.get("total") not in exclude_values:
        res1, res2, res3, res4 = map(list, zip(*search['datarows']))
        latandlon = zip(res2, res3)
        for (m, n) in zip(latandlon, res1):
            d2.append({"position": m, "content": n})
    else:
        d2.append({"position": [0,0], "content": "null"})
    return d2

# Source Attack Countries(Attack Events Page)
def geoip_country_name(agent_name, start_date, end_date, platform, severity):
    query_output = query(f"SELECT t.geoip_country_name, COUNT(t.geoip_country_name) count FROM {agent_name}-* as t WHERE t.geoip_country_name IS NOT NULL and DATE_FORMAT(@timestamp,'%Y-%m-%d') >= '{start_date}' and DATE_FORMAT(@timestamp,'%Y-%m-%d') <= '{end_date}' and platform IN ({platform}) and ids_threat_severity IN ({severity}) GROUP BY t.geoip_country_name ORDER BY count DESC LIMIT 7;")
    # print("CountryCount:", query_output)
    if query_output.get("total") not in exclude_values:
        list1, list2 = map(list, zip(*query_output['datarows']))
        required_dict = {"series": list2, "labels": list1}
    else:
        required_dict = {"series": ["null"], "labels": ["null"]}
    return required_dict

# Attacker ASN(Attack Event Page)
def Asn_name_count(agent_name, start_date, end_date, platform, severity):
    SQL_query = f"SELECT t.geoip_asn_name, COUNT(t.geoip_asn_name) as count FROM {agent_name}-* as t WHERE t.geoip_asn_name IS NOT NULL and DATE_FORMAT(@timestamp,'%Y-%m-%d') >= '{start_date}' and DATE_FORMAT(@timestamp,'%Y-%m-%d') <= '{end_date}' and platform IN ({platform}) and ids_threat_severity IN ({severity}) GROUP BY t.geoip_asn_name ORDER BY count DESC LIMIT 7;"
    # print(f"query:{SQL_query}")
    query_output = query(SQL_query)
    if query_output.get("total") not in exclude_values:
        list1, list2 = map(list, zip(*query_output['datarows']))
        required_dict = {"series": list2, "labels": list1}
    else:
        required_dict = {"series": ["null"], "labels": ["null"]}
    return required_dict

# Ports (Attack Event page)
def Tcp_port_count(agent_name, start_date, end_date, platform, severity):
    query_output = query(f"SELECT t.tcp_port, count(t.tcp_port) count FROM {agent_name}-* as t WHERE t.tcp_port IS NOT NULL and DATE_FORMAT(@timestamp,'%Y-%m-%d') >= '{start_date}' and DATE_FORMAT(@timestamp,'%Y-%m-%d') <= '{end_date}' and platform IN ({platform}) and ids_threat_severity IN ({severity}) GROUP BY t.tcp_port ORDER BY count desc LIMIT 7;")
    # print("TcpCount", query_output)
    if query_output.get("total") not in exclude_values:
        list1, list2 = map(list, zip(*query_output['datarows']))
        required_dict = {"series": list2, "labels": list1}
    else:
        required_dict = {"series": ["null"], "labels": ["null"]}
    return required_dict

# Attacker MAC Addresses(Attack Event page)
def Frequent_Attacker_Mack_Addresses(agent_name, start_date, end_date, platform, severity):
    query_output = query(f"SELECT t.target_mac_address, COUNT(t.target_mac_address) count FROM {agent_name}-* as t WHERE t.target_mac_address IS NOT NULL and  DATE_FORMAT(@timestamp,'%Y-%m-%d') >= '{start_date}' and DATE_FORMAT(@timestamp,'%Y-%m-%d') <= '{end_date}' and platform IN ({platform}) and ids_threat_severity IN ({severity}) GROUP BY t.target_mac_address ORDER BY count DESC LIMIT 7;")
    # print("FrequentAttackerMackAddresses:",query_output)
    if query_output.get("total") not in exclude_values:
        list1, list2 = map(list, zip(*query_output['datarows']))
        required_dict = {"series": list2, "labels": list1}
    else:
        required_dict = {"series": ["null"], "labels": ["null"]}
    return required_dict


g = globals()
# "Attacker IPs" count by date in series, seriesname & label format----top 7 on basis of count #Attacker IPs (Attack Event page)

def Attacker_IP_count(agent_name, start_date, end_date, platform, severity):
    # find attacker_ip with max count
    search1 = query(f"SELECT attacker_ip,count(attacker_ip) count FROM {agent_name}-* WHERE attacker_ip IS NOT NULL and DATE_FORMAT(@timestamp,'%Y-%m-%d') >= '{start_date}' and DATE_FORMAT(@timestamp,'%Y-%m-%d') <= '{end_date}' and platform IN ({platform}) and ids_threat_severity IN ({severity}) GROUP BY attacker_ip ORDER BY count desc LIMIT 7;")
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
    search2 = query(f"SELECT attacker_ip, DATE_FORMAT(@timestamp,'%Y-%m-%d'),count(attacker_ip) count FROM {agent_name}-* WHERE attacker_ip IN {updated_tuple} and DATE_FORMAT(@timestamp,'%Y-%m-%d') >= '{start_date}' and DATE_FORMAT(@timestamp,'%Y-%m-%d') <= '{end_date}' and platform IN ({platform}) and ids_threat_severity IN ({severity}) GROUP BY DATE_FORMAT(@timestamp,'%Y-%m-%d'),attacker_ip ORDER BY DATE_FORMAT(@timestamp,'%Y-%m-%d');")
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

# To count Frequency of attacks in categories & series format # Frequency of attacks (Attack Event page)
def Frequency_of_attacks(agent_name, start_date, end_date, platform, severity):
    SQL_query = query(f"SELECT DATE_FORMAT(@timestamp, '%Y-%m-%d') Date, count(*) FROM {agent_name}-* WHERE DATE_FORMAT(@timestamp,'%Y-%m-%d') >= '{start_date}' AND DATE_FORMAT(@timestamp,'%Y-%m-%d') <= '{end_date}' and platform IN ({platform}) and ids_threat_severity IN ({severity}) GROUP BY DATE_FORMAT(@timestamp,'%Y-%m-%d') ORDER BY DATE_FORMAT(@timestamp, '%Y-%m-%d');")
    # print("FrequencyOfAttacks:", SQL_query)
    if SQL_query.get("total") not in exclude_values:
        Dates, count_of_attacks = map(list, zip(*SQL_query['datarows']))
        required_dict = {"categories": Dates, "series": count_of_attacks}
    else:
        required_dict = {"categories": ["null"], "series": ["null"]}
    return required_dict

# Service Name (Attack_Event Page) to count groub by query by baby
def Service_Name(agent_name, start_date, end_date, platform, severity):
    api_response = query(f"SELECT service_name, count(service_name) count FROM {agent_name}-* WHERE service_name NOT LIKE 'NA' AND DATE_FORMAT(@timestamp,'%Y-%m-%d') >= '{start_date}' AND DATE_FORMAT(@timestamp,'%Y-%m-%d') <= '{end_date}' and platform IN ({platform}) and ids_threat_severity IN ({severity}) GROUP BY service_name ORDER BY count DESC LIMIT 6;")
    service_name_count = []
    # print("Service_name:", api_response)
    if api_response.get("total") not in exclude_values:
        service_name,service_count= map(list, zip(*api_response['datarows']))
        for (key, value) in zip(service_name,service_count):
            dict = {}
            dict.update({"name":key, "val":value})
            service_name_count.append(dict)
    return service_name_count





    