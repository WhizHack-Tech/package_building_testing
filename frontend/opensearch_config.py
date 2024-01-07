#  ==================================================================================================
#  File Name: opensearch_config.py
#  Description: Config file to fire SQL queries on Opensearch data.
#  ---------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  ====================================================================================================

# request library function which connects to opensearch cluster 
# used to fire sql query on opensearch data

import json, requests
from django.core.exceptions import ObjectDoesNotExist
from .models import Agent_data
from django.db import connection

host = 'ec2-18-191-233-47.us-east-2.compute.amazonaws.com'
port = '9200'
db_username = 'admin'
db_password = 'admin'


def query(query_string):
    global host, port, db_username, db_password
    
    url = f"https://{host}:{port}/_plugins/_sql"
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        }

    payload = json.dumps({"query": query_string})
    response = requests.request("POST", url, data=payload, headers=headers, auth=(db_username,db_password), verify=False)
    response_content = response.json()
    return response_content

# for testing wazuh queries
def querywazuh(querywazuh_string):
    host = '20.235.163.218'
    port = '9200'
    db_username = 'admin'
    db_password = 'Diabolic-Cried-Monetary'
    
    url = f"https://{host}:{port}/_plugins/_sql"
    
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    payload = json.dumps({"querywazuh": querywazuh_string})

    # try:
    response = requests.post(url, data=payload, headers=headers, auth=(db_username, db_password),verify=False)
    response.raise_for_status()
    response_content = response.json()
    return response_content

# function for opensearch connection using db
def opensearch_conn_using_db(query_string, location_id, plan_id):
    try:
        agentobj = Agent_data.objects.get(org_location = location_id, updated_plan_id = plan_id)
        database_host = agentobj.db_host
        database_port = agentobj.db_port
        database_username = agentobj.db_username
        database_password = agentobj.db_password

        url = f"https://{database_host}:{database_port}/_plugins/_sql"
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            }

        payload = json.dumps({"query": query_string})
        response = requests.request("POST", url, data=payload, headers=headers, auth=(database_username,database_password), verify=False)
        response_content = response.json()
        return response_content
    
    except ObjectDoesNotExist:
        return "object_n_found"
    except Exception:
        return {"err":"invalid_opensearch_connection_details"}

