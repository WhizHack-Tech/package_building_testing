#  ============================================================
#  File Name: live_network_map.py
#  Description: This file contains code for Live Attack Map.
#  Active URL: https://xdr-demo.zerohack.in/live/map
#  ------------------------------------------------------------
#  Item Name: Whizhack Client Dashboard
#  Author URL: https://whizhack.in

#  ============================================================


import json, random
from django.shortcuts import render
from .models import Page_Permissions
from .helpers import getIndexNameByLocationId
from .sql_queries import map_query

def random_swap(arr):
    length = len(arr)
    for i in range(length):
        j = random.randint(0, length - 1)
        arr[i], arr[j] = arr[j], arr[i]


def form_json(item, log_type):
    formed_json = {
        "origin": {
            "name": item[2],
            "radius": 2,
            "fillKey": 'markers',
            "coordinates": [item[1], item[0]]
        },
        "destination": {
            "name": item[5],
            "radius": 2,
            "fillKey": 'markers',
            "coordinates": [item[4], item[3]]
        }
    }

    if log_type == "nids_alert":
        formed_json["options"] = {
            "strokeColor": "rgb(40, 199, 111)", # green color
            "strokeWidth": 1,
            "alertLable": "NIDS Alert"
        }

    elif log_type == "nids_event":
        formed_json["options"] = {
            "strokeColor": "rgb(112, 101, 236)", # blue color #7065ec
            "strokeWidth": 1,
            "alertLable": "NIDS Event"
        }

    elif log_type == "nids_incident":
        formed_json["options"] = {
            "strokeColor": "rgb(231, 76, 60)", # red color
            "strokeWidth": 1,
            "alertLable": "NIDS Incident"
        }
    
    elif log_type == "trace_alert":
        formed_json["options"] = {
            "strokeColor": "rgb(255, 159, 67)", #orange: #ff9f43 # RGB (255, 159, 67)
            "strokeWidth": 1,
            "alertLable": "Trace Alert"
        }

    elif log_type == "trace_event":
        formed_json["options"] = {
            "strokeColor": "rgb(0,207,232)", # blue: #00cfe8 # rgb(0,207,232)
            "strokeWidth": 1,
            "alertLable": "Trace Event"
        }

    elif log_type == "trace_incident":
        formed_json["options"] = {
            "strokeColor": "rgb(255, 255, 255)", # white
            "strokeWidth": 1,
            "alertLable": "Trace Incident"
        }
    
    formed_json["ids_threat_class"] = item[6] if item[6] else ""

    return formed_json


# live network map data using html template
def live_network_map(request):
    location_id = request.GET.get("location_id")
    conditions = request.GET.get("conditions")
    plan_id = request.GET.get("activated_plan_id")

    nids_status = False
    trace_status = False

    if conditions == None:
        conditions = "last_24_hours"

    agent_index_nids = {
        "alert" : None,
        "event" : None,
        "incident" : None
    }

    agent_index_trace = {
        "alert" : None,
        "event" : None,
        "incident" : None
    }

    try:
        page_permissions_obj = Page_Permissions.objects.get(location_id = location_id, updated_plan_id = plan_id)
        index_name = getIndexNameByLocationId(location_id, plan_id)
        
        if page_permissions_obj.env_nids:
            nids_status = True
            agent_index_nids.update({
                "alert" : index_name.get('nids_alert_agent'),
                "event" : index_name.get('nids_event_agent'),
                "incident" : index_name.get('nids_incident_agent'),
            })

        if page_permissions_obj.env_trace:
            trace_status = True
            agent_index_trace.update({
                "alert" : index_name.get('trace_alert_agent'),
                "event" : index_name.get('trace_event_agent'),
                "incident" : index_name.get('trace_incident_agent'),
            })

    except Page_Permissions.DoesNotExist:
        print("page permission not exist")
        nids_status = False
        trace_status = False
        pass

    formed_json, nids_json_data, trace_json_data = ([] for _ in range(3))

    if nids_status:
        nids_alert_json, nids_event_json, nids_incident_json = [], [], []
        agent_index_nids_alert = None
        if agent_index_nids.get('alert') != None:
            query = map_query(f"{agent_index_nids.get('alert')}-*", conditions, location_id, plan_id)
            agent_index_nids_alert = query.get('resolve_query')
            if agent_index_nids_alert.get("total") not in [0, None]:
                nids_alert_json = [form_json(row, "nids_alert") for row in agent_index_nids_alert['datarows']]

        agent_index_nids_event = None
        if agent_index_nids.get('event') != None:
            query = map_query(f"{agent_index_nids.get('event')}-*", conditions, location_id, plan_id)
            agent_index_nids_event = query.get('resolve_query')
            if agent_index_nids_event.get("total") not in [0, None]:
                nids_event_json = [form_json(row, "nids_event") for row in agent_index_nids_event['datarows']]

        
        agent_index_nids_incident = None
        if agent_index_nids.get('incident') != None:
            query = map_query(f"{agent_index_nids.get('incident')}-*", conditions, location_id, plan_id)
            agent_index_nids_incident = query.get('resolve_query')
            if agent_index_nids_incident.get("total") not in [0, None]:
                nids_incident_json = [form_json(row, "nids_incident") for row in agent_index_nids_incident['datarows']]  
        
        # combining nids json data together
        nids_json_data =  nids_alert_json + nids_event_json + nids_incident_json
    
    if trace_status:
        trace_alert_json, trace_event_json, trace_incident_json = [], [], []
        agent_index_trace_alert = None
        if agent_index_trace.get('alert') != None:
            query = map_query(f"{agent_index_trace.get('alert')}-*", conditions, location_id, plan_id)
            agent_index_trace_alert = query.get('resolve_query')
            if agent_index_trace_alert.get("total") not in [0, None]:
                trace_alert_json = [form_json(row, "trace_alert") for row in agent_index_trace_alert['datarows']]

        agent_index_trace_event = None
        if agent_index_trace.get('event') != None:
            query = map_query(f"{agent_index_trace.get('event')}-*", conditions, location_id, plan_id)
            agent_index_trace_event = query.get('resolve_query')
            if agent_index_trace_event.get("total") not in [0, None]:
                trace_event_json = [form_json(row, "trace_event") for row in agent_index_trace_event['datarows']]

        agent_index_trace_incident = None  
        if agent_index_trace.get('incident') != None:
            query = map_query(f"{agent_index_trace.get('incident')}-*", conditions, location_id, plan_id)
            agent_index_trace_incident = query.get('resolve_query')
            if agent_index_trace_incident.get("total") not in [0, None]:
                trace_incident_json = [form_json(row, "trace_incident") for row in agent_index_trace_incident['datarows']]
        
        # combining trace json data together
        trace_json_data = trace_alert_json + trace_event_json + trace_incident_json 

    formed_json = nids_json_data + trace_json_data

    random_swap(formed_json)
    json_data = json.dumps(formed_json)
    status_dict = {"nids": nids_status, "trace": trace_status}
    response = render(request, "frontend/map1.html", {'json_data': json_data, 'status':status_dict})
    response ['X-Frame-Options'] = "SAMEORIGIN always"
    if (nids_status == False) and (trace_status == False):
        response.status_code = 404
    return response
