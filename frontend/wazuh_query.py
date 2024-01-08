#  ===========================================================================================================
#  File Name: wazuh_query.py
#  Description: This file contains old code used for wazuh.

#  -----------------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  ===========================================================================================================

# import json
# import requests
# from rest_framework.response import Response
# from django.http import HttpResponse
# from rest_framework.views import APIView
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from .helpers import getAgentNameOrgId
# from .wazuh_mitre_attack_page import *
# # from .wazuh_query import querywazuhwazuh
# # from .opensearch_config import querywazuh



# # wazuh querywazuhwazuh 

# import json, requests

# a = globals()
# exclude_values = [0,None]

# #urls for multiple function

# class WazuhQuriesSecurityEventPage(APIView):
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         organization_id = str(request.user.organization_id)
#         agent_details = getAgentNameOrgId(organization_id)
#         if (agent_details.get("wazuh_attach") != None):
#             # wazuh_attach = agent_details.get("wazuh_attach")
#             wazuh_attach = "xdr-wazuhlogs-whizhack-*"
#             print(f"wazuh_attach{wazuh_attach}")
#             start_date = request.data.get("start_date")
#             end_date = request.data.get("end_date") 
#             agent_id = request.data.get("agent_id")
#             security_alerts = SecurityAlerts(start_date,end_date,agent_id,wazuh_attach)
#             top_five_alert = TopFiveAlert(start_date,end_date,agent_id,wazuh_attach)
#             top_five_rule_groups = TopFiveRuleGroups(start_date,end_date,agent_id,wazuh_attach)
#             top_five_pci_dss_requirements = TopFivePciDssRequirements(start_date,end_date,agent_id,wazuh_attach)
#             alert_groups_evolution_security=AlertgroupsevolutionSecurity(start_date,end_date,agent_id,wazuh_attach)
#             top_tactics = TopTactics(start_date,end_date,agent_id,wazuh_attach)
#             rule_level_by_attack = RuleLevelByAttack(start_date,end_date,agent_id,wazuh_attach)
#             rule_level_by_tactics = RuleLevelByTactics(start_date, end_date,agent_id,wazuh_attach)
#             alerts_evolution_over_time = AlertsEvolutionOverTime(start_date, end_date,agent_id,wazuh_attach)
#             mitre_attack_by_tactic = MitreAttackByTactic(start_date, end_date,agent_id,wazuh_attach)


#             return Response({"security_alerts":security_alerts,"top_five_alert":top_five_alert,"top_five_rule_groups":top_five_rule_groups,"top_five_pci_dss_requirements":top_five_pci_dss_requirements,"alert_groups_evolution_security":alert_groups_evolution_security,"top_tactics":top_tactics,"rule_level_by_attack":rule_level_by_attack,"rule_level_by_tactics":rule_level_by_tactics,"alerts_evolution_over_time":alerts_evolution_over_time,
#             "mitre_attack_by_tactic":mitre_attack_by_tactic})
#         else:
#             return Response({"message":"agent not found."})

# # Group by  querywazuh to get data in table format

# from rest_framework.decorators import api_view
# from rest_framework.response import Response

# @api_view(['GET'])
# def UniquedataAgentId(request):
#     # sql_query = f"SELECT agent_id,agent_name,agent_ip from xdr-wazuhlogs-whizhack-* WHERE agent_ip IS NOT NULL Group By agent_id,agent_name,agent_ip;"
#     # print(f"sql_query{sql_query}")
   
#     api_response = querywazuh(f"SELECT agent_id, agent_name, agent_ip FROM xdr-wazuhlogs-whizhack-* WHERE agent_id IS NOT NULL GROUP BY agent_id, agent_name, agent_ip;")
#     print(f"api_response: {api_response}")

#     if api_response is not None and api_response.get("total") not in exclude_values:
#         key_names = [schema.get('name') for schema in api_response.get('schema')]
#         final_response = [dict(zip(key_names, row)) for row in api_response.get('datarows')]
#         return Response({"message_type": "data_found", "data": final_response})
#     else:
#         return Response({"message_type": "d_not_f"})

# # @api_view(['GET'])
# # def UniquedataAgentId(request):
# #     # sql_query = f"SELECT agent_id,agent_name,agent_ip from xdr-wazuhlogs-whizhack-* WHERE agent_ip IS NOT NULL Group By agent_id,agent_name,agent_ip;"
# #     # print(f"sql_query{sql_query}")
   
# #     api_response =   querywazuh(
# #         f"SELECT agent_id,agent_name,agent_ip from xdr-wazuhlogs-whizhack-* WHERE agent_id IS NOT NULL Group By agent_id,agent_name,agent_ip;")
# #     print(f"api_response: {api_response}")
# #     if api_response.get("total") not in exclude_values:     
# #         key_names = []
# #         for i in range(len( api_response.get('schema'))):
# #             key_names.append( api_response.get('schema')[i].get('name'))
# #         final_response = []
# #         for i in range(len(api_response.get('datarows'))):
# #             row =  api_response.get('datarows')[i]
# #             final_response.append(dict(zip(key_names, row)))
# #         return Response({"message_type":"data_found","data":final_response})
# #     else:
# #         return Response({"message_type":"d_not_f"})


# # Security Event Page Wazuh dashboard queries(card name = Security Alerts)
# def SecurityAlerts(start_date,end_date,agent_id,wazuh_attach):
#     querysql = f"SELECT * from {wazuh_attach}-* WHERE DATE_FORMAT(timestamp,'%Y-%m-%d') >= '{start_date}' AND DATE_FORMAT(timestamp,'%Y-%m-%d') <= '{end_date}' AND agent_id = '{agent_id};"
#     api_response = querywazuh(querysql)
#     # api_response =   querywazuh(
#     #     f"SELECT * from {wazuh_attach}-* WHERE DATE_FORMAT(timestamp,'%Y-%m-%d') >= '{start_date}' AND DATE_FORMAT(timestamp,'%Y-%m-%d') <= '{end_date}' AND agent_id = '{agent_id}';")
#     if api_response.get("total") not in exclude_values:    
#         key_names = []
#         for i in range(len( api_response.get('schema'))):
#             key_names.append( api_response.get('schema')[i].get('name'))
#         final_response = []
#         for i in range(len(api_response.get('datarows'))):
#             row =  api_response.get('datarows')[i]
#             final_response.append(dict(zip(key_names, row)))
#         return {"message_type":"data_found","data":final_response}
#     else:
#         return {"message_type":"d_not_f"}

# # Security Event Page Wazuh dashboard queries(card name = Top 5 Alert)
# def TopFiveAlert(start_date,end_date,agent_id,wazuh_attach):
#     api_response = querywazuh(f"SELECT rule_description,COUNT(rule_description) count FROM {wazuh_attach}-* WHERE rule_description IS NOT NULL AND DATE_FORMAT(timestamp,'%Y-%m-%d') >= '{start_date}' and DATE_FORMAT(timestamp,'%Y-%m-%d') <= '{end_date}' and agent_id = '{agent_id}' GROUP BY rule_description ORDER BY count DESC LIMIT 5;")
#     if api_response.get("total") not in exclude_values:
#         list1, list2 = map(list, zip(*api_response['datarows']))
#         dict_storage = {"series": list2, "labels": list1}
#         return {"message_type":"data_found","data":dict_storage}
#     else:
#         return {"message_type":"d_not_f"}

# # Security Event Page Wazuh dashboard queries(card name = Top 5 rules groups)
# def TopFiveRuleGroups(start_date,end_date,agent_id,wazuh_attach):
#     api_response = querywazuh(f"SELECT rule_groups,COUNT(rule_groups) count FROM {wazuh_attach}-* WHERE rule_groups IS NOT NULL AND DATE_FORMAT(timestamp,'%Y-%m-%d') >= '{start_date}' and DATE_FORMAT(timestamp,'%Y-%m-%d') <= '{end_date}' and agent_id = '{agent_id}' GROUP BY rule_groups ORDER BY count DESC LIMIT 5;")
#     if api_response.get("total") not in exclude_values:
#         list1, list2 = map(list, zip(*api_response['datarows']))
#         dict_storage = {"series": list2, "labels": list1}
#         return {"message_type":"data_found","data":dict_storage}
#     else:
#         return {"message_type":"d_not_f"}

# # Security Event Page Wazuh dashboard queries(card name = Top 5 PCI DSS Requirements)
# def TopFivePciDssRequirements(start_date,end_date,agent_id,wazuh_attach):
#     api_response = querywazuh(f"SELECT rule_pci_dss,COUNT(rule_pci_dss) count FROM {wazuh_attach}-* WHERE rule_pci_dss IS NOT NULL AND DATE_FORMAT(timestamp,'%Y-%m-%d') >= '{start_date}' and DATE_FORMAT(timestamp,'%Y-%m-%d') <= '{end_date}' and agent_id = '{agent_id}' GROUP BY rule_pci_dss ORDER BY count DESC LIMIT 5;")
#     if api_response.get("total") not in exclude_values:
#         list1, list2 = map(list, zip(*api_response['datarows']))
#         dict_storage = {"series": list2, "labels": list1}
#         return {"message_type":"data_found","data":dict_storage}
#     else:
#         return {"message_type":"d_not_f"}


# # ## Security Event Page Wazuh dashboard queries(card name = First card status)
# # def StatusFirstCard(start_date,end_date,agent_id):
# #     api_response = querywazuhwazuh(
# #         f"SELECT agent_id,agent_ip,agent_name,decoder_name,location,rule_level,rule_id from xdr-wazuhlogs-zerohack-* WHERE DATE_FORMAT(timestamp,'%Y-%m-%d') >= '{start_date}' AND DATE_FORMAT(timestamp,'%Y-%m-%d') <= '{end_date}' AND agent_id = '{agent_id}' GROUP BY agent_id,agent_ip,agent_name,decoder_name,location,rule_level,rule_id;")
# #     if api_response.get("total") not in exclude_values:    
# #         key_names = []
# #         for i in range(len( api_response.get('schema'))):
# #             key_names.append( api_response.get('schema')[i].get('name'))
# #         final_response = []
# #         for i in range(len(api_response.get('datarows'))):
# #             row =  api_response.get('datarows')[i]
# #             final_response.append(dict(zip(key_names, row)))
# #         return {"message_type":"data_found","data":final_response}
# #     else:
# #         return {"message_type":"d_not_f"}



# #--------------------------line chart------------------
# # Security Event Page Wazuh dashboard queries(card name = Alert groups evolution)
# def AlertgroupsevolutionSecurity(start_date, end_date,agent_id,wazuh_attach):
#     search1 = querywazuh(f"SELECT rule_hipaa,count(rule_hipaa) count FROM {wazuh_attach}-* WHERE rule_hipaa IS NOT NULL and DATE_FORMAT(timestamp,'%Y-%m-%d') >= '{start_date}' and DATE_FORMAT(timestamp,'%Y-%m-%d') <= '{end_date}' and agent_id = '{agent_id}' GROUP BY rule_hipaa;")
    
#     if search1.get("total") not in exclude_values:
#         unique_rule, list2 = map(list, zip(*search1['datarows']))
#         attacker_ip_tuple = tuple(unique_rule)
#         updated_tuple = attacker_ip_tuple
#         if len(attacker_ip_tuple) == 1:
#             updated_tuple = attacker_ip_tuple+('0',)
#     else:
#         return {"message_type":"d_not_f"}
#     search2 = querywazuh(f"SELECT rule_hipaa, DATE_FORMAT(timestamp,'%Y-%m-%d'),count(rule_hipaa) count FROM {wazuh_attach}-* WHERE rule_hipaa IN {updated_tuple} and DATE_FORMAT(timestamp,'%Y-%m-%d') >= '{start_date}' and DATE_FORMAT(timestamp,'%Y-%m-%d') <= '{end_date}' and agent_id = '{agent_id}' GROUP BY DATE_FORMAT(timestamp,'%Y-%m-%d'),rule_hipaa ORDER BY DATE_FORMAT(timestamp,'%Y-%m-%d');")

#     if search2.get("total") not in exclude_values:
#         tactic_list, Dates, individual_ip_counts = map(list, zip(*search2['datarows']))
#         unique_dates = list(dict.fromkeys(Dates))
#         n = len(unique_dates)
#         nested_outer_list = []
#         for u in range(len(unique_rule)):
#             inner_list = []
#             for i in range(len(search2['datarows'])):
#                 if unique_rule[u] == search2['datarows'][i][0]:
#                     inner_list.append(search2['datarows'][i])
#             nested_outer_list.append(inner_list)

#         number_of_IPs = len(nested_outer_list)
#         for i in range(number_of_IPs):
#             a['IP_{0}'.format(i)] = nested_outer_list[i]

#         no_of_dates = len(unique_dates)
#         for j in range(number_of_IPs):
#             a['IP_{0}_count'.format(j)] = ['']*no_of_dates

 
#         for k in range(number_of_IPs):
#             for i in range(len(a['IP_{0}'.format(k)])):
#                 for j in range(len(unique_dates)):
#                     if unique_dates[j] == a['IP_{0}'.format(k)][i][1]:
#                         a['IP_{0}_count'.format(k)][j] = a['IP_{0}'.format(k)][i][2]

#         for k in range(number_of_IPs):
#             for i in range(len(a['IP_{0}_count'.format(k)])):
#                 if a['IP_{0}_count'.format(k)][i] == "":
#                     a['IP_{0}_count'.format(k)][i] = 0


#         for k in range(number_of_IPs):
#             f"{'IP_{0}_count'.format(k)}",a['IP_{0}_count'.format(k)]
#         nd = {}
#         series =[]
#         for k in range(number_of_IPs):
#             rule_name = {}
#             rule_name.update({"name": unique_rule[k]})
#             rule_name.update({"data": a['IP_{0}_count'.format(k)]})
#             series.append(rule_name)

#         nd.update({"labels": unique_dates})
#         nd.update({"series":series})
#         return {"message_type":"data_found","data":nd}
#     else:
#         return {"message_type":"d_not_f"}
    




# # -------------------------------completed previous querywazuhwazuh----------------------------
