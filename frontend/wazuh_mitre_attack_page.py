#  ===========================================================================================================
#  File Name: wazuh_mitre_attack_page.py
#  Description: This file contains old code used for wazuh.

#  -----------------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  ===========================================================================================================

# import json, requests
# from .opensearch_config import querywazuh


# g = globals()
# exclude_values = [0,None]

# # Mitre Attack Page-pie chart(card name = Top Tactics)
# def TopTactics(start_date, end_date,agent_id,wazuh_attach):
#     SQL_query = f"SELECT rule_mitre_tactic, count(rule_mitre_tactic) count from {wazuh_attach}-* WHERE rule_mitre_tactic IS NOT NULL AND DATE_FORMAT(timestamp,'%Y-%m-%d') >= '{start_date}' AND DATE_FORMAT(timestamp,'%Y-%m-%d') <= '{end_date}' AND agent_id = '{agent_id}' Group By rule_mitre_tactic ORDER BY count DESC LIMIT 5;"
#     api_response = querywazuh(SQL_query)
#     if api_response.get("total") not in exclude_values:
#         rule_mitre_tactic,count= map(list, zip(*api_response['datarows']))
#         reqd_dict = {"series":count , "labels":rule_mitre_tactic}
#         return {"message_type":"data_found","data":reqd_dict}
#     else:
#         return {"message_type":"d_not_f"}

# # Mitre Attack Page-pie chart(card name = Rule Level By Attack)
# def RuleLevelByAttack(start_date, end_date,agent_id,wazuh_attach):
#     SQL_query = f"SELECT rule_mitre_id, count(rule_mitre_id) count from {wazuh_attach}-* WHERE rule_mitre_id IS NOT NULL AND DATE_FORMAT(timestamp,'%Y-%m-%d') >= '{start_date}' AND DATE_FORMAT(timestamp,'%Y-%m-%d') <= '{end_date}' AND agent_id = '{agent_id}' Group By rule_mitre_id ORDER BY count DESC LIMIT 5;"
#     api_response = querywazuh(SQL_query)
#     if api_response.get("total") not in exclude_values:
#         rule_mitre_id,count= map(list, zip(*api_response['datarows']))
#         reqd_dict = {"series":count , "labels":rule_mitre_id}
#         return {"message_type":"data_found","data":reqd_dict}
#     else:
#         return {"message_type":"d_not_f"}

# # Mitre Attack Page-pie chart(card name = Rule Level By Tactics)
# def RuleLevelByTactics(start_date, end_date,agent_id,wazuh_attach):
#     SQL_query = f"SELECT rule_mitre_technique, count(rule_mitre_technique) count from {wazuh_attach}-* WHERE rule_mitre_technique IS NOT NULL AND DATE_FORMAT(timestamp,'%Y-%m-%d') >= '{start_date}' AND DATE_FORMAT(timestamp,'%Y-%m-%d') <= '{end_date}' AND agent_id = '{agent_id}' Group By rule_mitre_technique ORDER BY count DESC LIMIT 5;"
#     api_response = querywazuh(SQL_query)
#     if api_response.get("total") not in exclude_values:
#         rule_mitre_technique,count= map(list, zip(*api_response['datarows']))
#         reqd_dict = {"series":count , "labels":rule_mitre_technique}
#         return {"message_type":"data_found","data":reqd_dict}
#     else:
#         return {"message_type":"d_not_f"}

# # ########################################################################
# # Line chart

# # Mitre Attack Page-line chart(card name = Alerts evolution over time)
# def AlertsEvolutionOverTime(start_date, end_date,agent_id,wazuh_attach):
#     # rule_mitre_tactic
#     search1 = querywazuh(f"SELECT rule_mitre_tactic,count(rule_mitre_tactic) count FROM {wazuh_attach}-* WHERE rule_mitre_tactic IS NOT NULL and DATE_FORMAT(timestamp,'%Y-%m-%d') >= '{start_date}' and DATE_FORMAT(timestamp,'%Y-%m-%d') <= '{end_date}' and agent_id = '{agent_id}' GROUP BY rule_mitre_tactic ORDER BY count desc LIMIT 7;")
#     # print("AttackerIPCount--finding top7 attacker ip:",search1 )
#     if search1.get("total") not in exclude_values:
#         unique_tactics, list2 = map(list, zip(*search1['datarows']))
#         attacker_ip_tuple = tuple(unique_tactics)
#         updated_tuple = attacker_ip_tuple
#         if len(attacker_ip_tuple) == 1:
#             updated_tuple = attacker_ip_tuple+('0',)
#     else:
#         return {"message_type":"d_not_f"}

#     # date wise count of a single attacker_ip
#     search2 = querywazuh(f"SELECT rule_mitre_tactic, DATE_FORMAT(timestamp,'%Y-%m-%d'),count(rule_mitre_tactic) count FROM {wazuh_attach}-* WHERE rule_mitre_tactic IN {updated_tuple} and DATE_FORMAT(timestamp,'%Y-%m-%d') >= '{start_date}' and DATE_FORMAT(timestamp,'%Y-%m-%d') <= '{end_date}' and agent_id = '{agent_id}' GROUP BY DATE_FORMAT(timestamp,'%Y-%m-%d'),rule_mitre_tactic ORDER BY DATE_FORMAT(timestamp,'%Y-%m-%d');")
    
#     # print("AttackerIPCount--datewise count of attacker ip:", search2)
#     if search2.get("total") not in exclude_values:
#         tactic_list, Dates, individual_tactic_counts = map(list, zip(*search2['datarows']))
#         # removing redundant elements from list with dates
#         unique_dates = list(dict.fromkeys(Dates))

#         #I creating nested list:each mitre tactic clubbed with multiple dates, count, name in separate list
#         # print(f"unique_tactics:{unique_tactics} and updated_tuple:{updated_tuple}")
#         nested_outer_list = []
#         for u in range(len(unique_tactics)):
#             inner_list = []
#             for i in range(len(search2['datarows'])):
#                 if unique_tactics[u] == search2['datarows'][i][0]:
#                     inner_list.append(search2['datarows'][i])
#             nested_outer_list.append(inner_list)
#         # print(f"nested_outer_list:{nested_outer_list}")

#         #II assigning [[mitre_name, count, date1],[mitre_name, count, date1]] to a global variable
#         number_of_mitre_tactic = len(nested_outer_list)
#         # print(f"number_of_IPs:{number_of_mitre_tactic}")
#         for i in range(number_of_mitre_tactic):
#             g['mitre_tactic_{0}'.format(i)] = nested_outer_list[i]

#         #III creating global variables named g['mitre_tactic_{index}_count']
#         no_of_dates = len(unique_dates)
#         for j in range(number_of_mitre_tactic):
#             g['mitre_tactic_{0}_count'.format(j)] = ['']*no_of_dates

#         # IV appending count values in global variables g['mitre_tactic_{0}_count']
#         for k in range(number_of_mitre_tactic):
#             for i in range(len(g['mitre_tactic_{0}'.format(k)])):
#                 for j in range(len(unique_dates)):
#                     if unique_dates[j] == g['mitre_tactic_{0}'.format(k)][i][1]:
#                         g['mitre_tactic_{0}_count'.format(k)][j] = g['mitre_tactic_{0}'.format(k)][i][2]

#         # # V appending 0 on dates where count is not present
#         for k in range(number_of_mitre_tactic):
#             for i in range(len(g['mitre_tactic_{0}_count'.format(k)])):
#                 if g['mitre_tactic_{0}_count'.format(k)][i] == "":
#                     g['mitre_tactic_{0}_count'.format(k)][i] = 0

#         # for k in range(number_of_mitre_tactic):
#         #     print(f"{'mitre_tactic_{0}_count'.format(k)}",g['mitre_tactic_{0}_count'.format(k)])
#         #     print(f"{'mitre_tactic_{0}'.format(k)}",g['mitre_tactic_{0}'.format(k)])

#         nd = {}
#         series =[]
#         for k in range(number_of_mitre_tactic):
#             mitre_name = {}
#             mitre_name.update({"name": unique_tactics[k]})
#             mitre_name.update({"data": g['mitre_tactic_{0}_count'.format(k)]})
#             series.append(mitre_name)
        
#         nd.update({"labels": unique_dates})
#         nd.update({"series":series})
#         return {"message_type":"data_found","data":nd}
#     else:
#         return {"message_type":"d_not_f"}


# # Mitre Attack Page-Bar chart(card name = Mitre Attacks By Tactic)
# def MitreAttackByTactic(start_date, end_date,agent_id,wazuh_attach):
#     search1 = querywazuh(f"SELECT rule_mitre_tactic,count(rule_mitre_tactic) count FROM {wazuh_attach}-* WHERE rule_mitre_tactic IS NOT NULL and DATE_FORMAT(timestamp,'%Y-%m-%d') >= '{start_date}' and DATE_FORMAT(timestamp,'%Y-%m-%d') <= '{end_date}' and agent_id = '{agent_id}' GROUP BY rule_mitre_tactic ORDER BY count desc LIMIT 7;")
#     # print("AttackerIPCount--finding top7 attacker ip:",search1 )
#     if search1.get("total") not in exclude_values:
#         unique_tactics, list2 = map(list, zip(*search1['datarows']))
#         attacker_ip_tuple = tuple(unique_tactics)
#         updated_tuple = attacker_ip_tuple
#         if len(attacker_ip_tuple) == 1:
#             updated_tuple = attacker_ip_tuple+('0',)
#     else:
#         return {"message_type":"d_not_f"}

 

#     # date wise count of a single attacker_ip
#     search2 = querywazuh(f"SELECT rule_mitre_tactic, DATE_FORMAT(timestamp,'%Y-%m-%d'),count(rule_mitre_tactic) count FROM {wazuh_attach}-* WHERE rule_mitre_tactic IN {updated_tuple} and DATE_FORMAT(timestamp,'%Y-%m-%d') >= '{start_date}' and DATE_FORMAT(timestamp,'%Y-%m-%d') <= '{end_date}' and agent_id = '{agent_id}' GROUP BY DATE_FORMAT(timestamp,'%Y-%m-%d'),rule_mitre_tactic ORDER BY DATE_FORMAT(timestamp,'%Y-%m-%d');")

#     # print("AttackerIPCount--datewise count of attacker ip:", search2)
#     if search2.get("total") not in exclude_values:
#         tactic_list, Dates, individual_tactic_counts = map(list, zip(*search2['datarows']))
#         # removing redundant elements from list with dates
#         unique_dates = list(dict.fromkeys(Dates))

 

#         #I creating nested list:each mitre tactic clubbed with multiple dates, count, name in separate list
#         # print(f"unique_tactics:{unique_tactics} and updated_tuple:{updated_tuple}")
#         nested_outer_list = []
#         for u in range(len(unique_tactics)):
#             inner_list = []
#             for i in range(len(search2['datarows'])):
#                 if unique_tactics[u] == search2['datarows'][i][0]:
#                     inner_list.append(search2['datarows'][i])
#             nested_outer_list.append(inner_list)
#         # print(f"nested_outer_list:{nested_outer_list}")

 

#         #II assigning [[mitre_name, count, date1],[mitre_name, count, date1]] to a global variable
#         number_of_mitre_tactic = len(nested_outer_list)
#         # print(f"number_of_IPs:{number_of_mitre_tactic}")
#         for i in range(number_of_mitre_tactic):
#             g['mitre_tactic_{0}'.format(i)] = nested_outer_list[i]

 

#         #III creating global variables named g['mitre_tactic_{index}_count']
#         no_of_dates = len(unique_dates)
#         for j in range(number_of_mitre_tactic):
#             g['mitre_tactic_{0}_count'.format(j)] = ['']*no_of_dates

 

#         # IV appending count values in global variables g['mitre_tactic_{0}_count']
#         for k in range(number_of_mitre_tactic):
#             for i in range(len(g['mitre_tactic_{0}'.format(k)])):
#                 for j in range(len(unique_dates)):
#                     if unique_dates[j] == g['mitre_tactic_{0}'.format(k)][i][1]:
#                         g['mitre_tactic_{0}_count'.format(k)][j] = g['mitre_tactic_{0}'.format(k)][i][2]

 

#         # # V appending 0 on dates where count is not present
#         for k in range(number_of_mitre_tactic):
#             for i in range(len(g['mitre_tactic_{0}_count'.format(k)])):
#                 if g['mitre_tactic_{0}_count'.format(k)][i] == "":
#                     g['mitre_tactic_{0}_count'.format(k)][i] = 0

 

#         # for k in range(number_of_mitre_tactic):
#         #     print(f"{'mitre_tactic_{0}_count'.format(k)}",g['mitre_tactic_{0}_count'.format(k)])
#         #     print(f"{'mitre_tactic_{0}'.format(k)}",g['mitre_tactic_{0}'.format(k)])

 

#         nd = {}
#         series =[]
#         for k in range(number_of_mitre_tactic):
#             mitre_name = {}
#             mitre_name.update({"name": unique_tactics[k]})
#             mitre_name.update({"data": g['mitre_tactic_{0}_count'.format(k)]})
#             series.append(mitre_name)

#         nd.update({"labels": unique_dates})
#         nd.update({"series":series})
#         return {"message_type":"data_found","data":nd}
#     else:
#         return {"message_type":"d_not_f"}




# #-------------------------------completed previous query----------------------------
