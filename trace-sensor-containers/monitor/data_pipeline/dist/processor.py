# Filename : Trace Data Pipeline
# Purpose/Description : The code in this file takes processed data from from TRACE Components such as honeypots, P0f, FATT, IDS and DPI Engines and sends it to the OpenSearch datastore and AWS S3 for presentation and Storage.
# Author : Nikhilesh Kumar, Nikhil Garg
# Copyright (c) : Whizhack Technologies (P) Ltd.
# Revisions/Modifications : Mahesh Banerjee

import json, os, gc, warnings, subprocess, sys,time, ndjson
import pandas as pd
import numpy as np
import time
from dateutil.tz import tzutc, UTC
from ipaddress import ip_address

# Setting initial variables for pandas.
pd.options.mode.chained_assignment = None
warnings.filterwarnings('ignore')


def honeynet_data_load(honeynet_path):

    honeynet_dataframe = pd.read_json(honeynet_path, lines=True)
    honeynet_required_list = ['os', 'dest_ip','dest_port','src_ip', 'src_port', 'tag','event_type', 'proto','app_proto', 'alert.signature', 'alert.category', 'alert.severity', 'alert.metadata.affected_product', 'alert.metadata.attack_target', 'alert.metadata.deployment', 'alert.metadata.tag', 'http.hostname', 'http.url', 'http.http_user_agent', 'http.http_method', 'anomaly.app_proto', 'anomaly.type', 'anomaly.event', 'anomaly.layer', 'app','files.md5', 'files.filename', 'files.state',  'username', 'password', 'alert.metadata.mitre_tactics_id', 'alert.metadata.mitre_tactics_name', 'alert.metadata.mitre_techniques_id', 'alert.metadata.mitre_techniques_name', 'alert.metadata.malware_family', 'alert.metadata.cve'] 
    for i in honeynet_required_list:
        if i not in honeynet_dataframe.columns:
            honeynet_dataframe[i] = np.nan
       
    # Take necessary features
    honeynet_dataframe = honeynet_dataframe[['os', 'dest_ip','dest_port','src_ip', 'src_port', 'tag','event_type', 'proto','app_proto', 'alert.signature', 'alert.category', 'alert.severity', 'alert.metadata.affected_product', 'alert.metadata.attack_target', 'alert.metadata.deployment', 'alert.metadata.tag', 'http.hostname', 'http.url', 'http.http_user_agent', 'http.http_method', 'anomaly.app_proto', 'anomaly.type', 'anomaly.event', 'anomaly.layer', 'app','files.md5', 'files.filename', 'files.state', 'username', 'password', 'alert.metadata.mitre_tactics_id', 'alert.metadata.mitre_tactics_name', 'alert.metadata.mitre_techniques_id', 'alert.metadata.mitre_techniques_name', 'alert.metadata.malware_family', 'alert.metadata.cve']]
    honeynet_dataframe = honeynet_dataframe.dropna(axis=0, subset=['dest_ip', 'src_ip']).reset_index(drop = True)
    honeynet_dataframe.drop_duplicates()

    return honeynet_dataframe

def dpi_data_load(dpi_path):

    dpi_dataframe = pd.read_json(dpi_path, lines=True)
    dpi_required_list = ['timestamp', 'stream_identity', 'operation_environment', 'operation_mode', 'stream_packets', 'stream_bytes', 'largest_chunk_bytes', 'largest_chunk_packets', 'synchronize_flags', 'acknowledgement_flags', 'finish_flags', 'push_flags', 'payload', 'stream_protocols', 'eth_src_mac', 'eth_dst_mac', 'src_ip', 'dst_ip', 'service_name', 'icmp_code', 'payload_string', 'human_analysis', 'src_port', 'dst_port', 'dhcp_client_ip', 'dhcp_relay_server_ip', 'dhcp_options', 'matched_signatures'] 
    for i in dpi_required_list:
        if i not in dpi_dataframe.columns:
            dpi_dataframe[i] = np.nan

    # Take necessary features
    dpi_dataframe = dpi_dataframe[['timestamp', 'stream_identity', 'operation_environment', 'operation_mode', 'stream_packets', 'stream_bytes', 'largest_chunk_bytes', 'largest_chunk_packets', 'synchronize_flags', 'acknowledgement_flags', 'finish_flags', 'push_flags', 'payload', 'stream_protocols', 'eth_src_mac', 'eth_dst_mac', 'src_ip', 'dst_ip', 'service_name', 'icmp_code', 'payload_string', 'human_analysis', 'src_port', 'dst_port', 'dhcp_client_ip', 'dhcp_relay_server_ip', 'dhcp_options', 'matched_signatures']]
    dpi_dataframe.drop_duplicates()

    return dpi_dataframe

def data_cleaner(honeynet_dataframe):

    # Initializing Timestamp for logging
    #======================
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    # Mapping the IP types as internal or external
    #======================
    honeynet_dataframe['src_host_type']= honeynet_dataframe['src_ip'].apply([lambda x: 'internal' if ip_address(x).is_private else 'external'])
    honeynet_dataframe['dst_host_type']= honeynet_dataframe['src_ip'].apply([lambda x: 'internal' if ip_address(x).is_private else 'external'])
    honeynet_dataframe["timestamp"] = timestamp

    #Required Columns:
    #==================
    new_columns = ['service_name','attacker_ip','attack_timestamp','target_ip','ids_threat_class','ids_threat_type','ids_threat_severity','type_of_threat', 'attacker_port', 'target_port', 'attacker_os', 'attack_epoch_time', 'files_filename', 'files_md5', 'files_state', 'anomaly_event', 'anomaly_app_proto', 'http_url', 'brut_username', 'brut_password', 'activity_type', 'mitre_tactics_id', 'mitre_tactics_name', 'mitre_techniques_id', 'mitre_techniques_name', 'malware_type', 'attacker_host_type', 'malware_cve_id', 'intel_source_feed_name', 'http_useragent']
    for i in range(len(new_columns)):
        last_column = len(honeynet_dataframe.columns)
        honeynet_dataframe.insert(loc=last_column, column=new_columns[i],value=None)
    del last_column
    gc.collect()
    
    # Resetting any broken indexes.
    #=============================
    honeynet_dataframe = honeynet_dataframe.reset_index(drop=True)
    for i in range(len(honeynet_dataframe.src_host_type)):
        if (honeynet_dataframe['src_host_type'][i] == 'external') and (honeynet_dataframe['dst_host_type'][i] == 'internal'):
            # If the source is external and destination is internal then we will assume the machine is being attacked.
            honeynet_dataframe['attacker_ip'][i] = honeynet_dataframe['src_ip'][i]
            honeynet_dataframe['target_ip'][i] = honeynet_dataframe['dest_ip'][i]
            honeynet_dataframe['ids_threat_class'][i] = honeynet_dataframe['alert.category'][i]
            honeynet_dataframe['ids_threat_type'][i] = honeynet_dataframe['alert.signature'][i]
            honeynet_dataframe['ids_threat_severity'][i] = honeynet_dataframe['alert.severity'][i]
            honeynet_dataframe['type_of_threat'][i] = 'External Attack'
            honeynet_dataframe['attack_timestamp'][i] = honeynet_dataframe['timestamp'][i] 
            honeynet_dataframe['service_name'][i] = honeynet_dataframe['app_proto'][i]
            ##### Addition columns
            if (honeynet_dataframe['event_type'][i] == 'alert'):
                honeynet_dataframe['activity_type'][i] = honeynet_dataframe['alert.category'][i]  
            else:
                honeynet_dataframe['activity_type'][i] = honeynet_dataframe['event_type'][i]
            honeynet_dataframe['mitre_tactics_id'][i] = honeynet_dataframe['alert.metadata.mitre_tactics_id'][i]
            honeynet_dataframe['mitre_tactics_name'][i] = honeynet_dataframe['alert.metadata.mitre_tactics_name'][i]
            honeynet_dataframe['mitre_techniques_id'][i] = honeynet_dataframe['alert.metadata.mitre_techniques_id'][i]
            honeynet_dataframe['mitre_techniques_name'][i] = honeynet_dataframe['alert.metadata.mitre_techniques_name'][i]
            honeynet_dataframe['malware_type'][i] = honeynet_dataframe['alert.metadata.malware_family'][i]
            honeynet_dataframe['attacker_host_type'][i] = honeynet_dataframe['alert.metadata.attack_target'][i]
            honeynet_dataframe['malware_cve_id'][i] = honeynet_dataframe['alert.metadata.cve'][i]
            honeynet_dataframe['intel_source_feed_name'][i] = honeynet_dataframe['alert.metadata.tag'][i]
            honeynet_dataframe['target_port'][i] = honeynet_dataframe['dest_port'][i]
            honeynet_dataframe['attacker_port'][i] = honeynet_dataframe['src_port'][i]

            honeynet_dataframe['tag'][i] = honeynet_dataframe['tag'][i]
            honeynet_dataframe['files_filename'][i] = honeynet_dataframe['files.filename'][i]
            honeynet_dataframe['files_md5'][i] = honeynet_dataframe['files.md5'][i]
            honeynet_dataframe['files_state'][i] = honeynet_dataframe['files.state'][i]
            honeynet_dataframe['anomaly_event'][i] = honeynet_dataframe['anomaly.event'][i]
            honeynet_dataframe['anomaly_app_proto'][i] = honeynet_dataframe['anomaly.app_proto'][i]
            honeynet_dataframe['http_url'][i] = honeynet_dataframe['http.url'][i]
            honeynet_dataframe['http_useragent'][i] = honeynet_dataframe['http.http_user_agent'][i]
            honeynet_dataframe['brut_username'][i] = honeynet_dataframe['username'][i]
            honeynet_dataframe['brut_password'][i] = honeynet_dataframe['password'][i]   


        elif (honeynet_dataframe['src_host_type'][i] == 'internal') and (honeynet_dataframe['dst_host_type'][i] == 'external'):
            # If the source is internal and connection is being made externally then we will assume the machine is talking to a CNC server as internal people cannot do anything bad.
            honeynet_dataframe['attacker_ip'][i] = honeynet_dataframe['src_ip'][i]
            honeynet_dataframe['target_ip'][i] = honeynet_dataframe['dest_ip'][i]
            honeynet_dataframe['ids_threat_class'][i] = honeynet_dataframe['alert.category'][i]
            honeynet_dataframe['ids_threat_type'][i] = honeynet_dataframe['alert.signature'][i]
            honeynet_dataframe['ids_threat_severity'][i] = honeynet_dataframe['alert.severity'][i]
            honeynet_dataframe['type_of_threat'][i] = 'Internal Compromised Machine'
            honeynet_dataframe['attack_timestamp'][i] = honeynet_dataframe['timestamp'][i] 
            honeynet_dataframe['service_name'][i] = honeynet_dataframe['app_proto'][i]
            ##### Addition columns
            if (honeynet_dataframe['event_type'][i] == 'alert'):
                honeynet_dataframe['activity_type'][i] = honeynet_dataframe['alert.category'][i]  
            else:
                honeynet_dataframe['activity_type'][i] = honeynet_dataframe['event_type'][i]
            honeynet_dataframe['mitre_tactics_id'][i] = honeynet_dataframe['alert.metadata.mitre_tactics_id'][i]
            honeynet_dataframe['mitre_tactics_name'][i] = honeynet_dataframe['alert.metadata.mitre_tactics_name'][i]
            honeynet_dataframe['mitre_techniques_id'][i] = honeynet_dataframe['alert.metadata.mitre_techniques_id'][i]
            honeynet_dataframe['mitre_techniques_name'][i] = honeynet_dataframe['alert.metadata.mitre_techniques_name'][i]
            honeynet_dataframe['malware_type'][i] = honeynet_dataframe['alert.metadata.malware_family'][i]
            honeynet_dataframe['attacker_host_type'][i] = honeynet_dataframe['alert.metadata.attack_target'][i]
            honeynet_dataframe['malware_cve_id'][i] = honeynet_dataframe['alert.metadata.cve'][i]
            honeynet_dataframe['intel_source_feed_name'][i] = honeynet_dataframe['alert.metadata.tag'][i]
            honeynet_dataframe['target_port'][i] = honeynet_dataframe['dest_port'][i]
            honeynet_dataframe['attacker_port'][i] = honeynet_dataframe['src_port'][i]

            honeynet_dataframe['tag'][i] = honeynet_dataframe['tag'][i]
            honeynet_dataframe['files_filename'][i] = honeynet_dataframe['files.filename'][i]
            honeynet_dataframe['files_md5'][i] = honeynet_dataframe['files.md5'][i]
            honeynet_dataframe['files_state'][i] = honeynet_dataframe['files.state'][i]
            honeynet_dataframe['anomaly_event'][i] = honeynet_dataframe['anomaly.event'][i]
            honeynet_dataframe['anomaly_app_proto'][i] = honeynet_dataframe['anomaly.app_proto'][i]
            honeynet_dataframe['http_url'][i] = honeynet_dataframe['http.url'][i]
            honeynet_dataframe['http_useragent'][i] = honeynet_dataframe['http.http_user_agent'][i]
            honeynet_dataframe['brut_username'][i] = honeynet_dataframe['username'][i]
            honeynet_dataframe['brut_password'][i] = honeynet_dataframe['password'][i]
        elif (honeynet_dataframe['src_host_type'][i] == 'internal') and (honeynet_dataframe['dst_host_type'][i] == 'internal'):
            # If the source is internal and connection is being made internally then it is either the case of internal communication or a possible insider attack.
            honeynet_dataframe['attacker_ip'][i] = honeynet_dataframe['src_ip'][i]
            honeynet_dataframe['target_ip'][i] = honeynet_dataframe['dest_ip'][i]
            honeynet_dataframe['ids_threat_class'][i] = honeynet_dataframe['alert.category'][i]
            honeynet_dataframe['ids_threat_type'][i] = honeynet_dataframe['alert.signature'][i]
            honeynet_dataframe['ids_threat_severity'][i] = honeynet_dataframe['alert.severity'][i]
            honeynet_dataframe['type_of_threat'][i] = 'Lateral Movement'
            honeynet_dataframe['attack_timestamp'][i] = honeynet_dataframe['timestamp'][i] 
            honeynet_dataframe['service_name'][i] = honeynet_dataframe['app_proto'][i]
            ##### Addition columns
            if (honeynet_dataframe['event_type'][i] == 'alert'):
                honeynet_dataframe['activity_type'][i] = honeynet_dataframe['alert.category'][i]  
            else:
                honeynet_dataframe['activity_type'][i] = honeynet_dataframe['event_type'][i]
            honeynet_dataframe['mitre_tactics_id'][i] = honeynet_dataframe['alert.metadata.mitre_tactics_id'][i]
            honeynet_dataframe['mitre_tactics_name'][i] = honeynet_dataframe['alert.metadata.mitre_tactics_name'][i]
            honeynet_dataframe['mitre_techniques_id'][i] = honeynet_dataframe['alert.metadata.mitre_techniques_id'][i]
            honeynet_dataframe['mitre_techniques_name'][i] = honeynet_dataframe['alert.metadata.mitre_techniques_name'][i]
            honeynet_dataframe['malware_type'][i] = honeynet_dataframe['alert.metadata.malware_family'][i]
            honeynet_dataframe['attacker_host_type'][i] = honeynet_dataframe['alert.metadata.attack_target'][i]
            honeynet_dataframe['malware_cve_id'][i] = honeynet_dataframe['alert.metadata.cve'][i]
            honeynet_dataframe['intel_source_feed_name'][i] = honeynet_dataframe['alert.metadata.tag'][i]
            honeynet_dataframe['target_port'][i] = honeynet_dataframe['dest_port'][i]
            honeynet_dataframe['attacker_port'][i] = honeynet_dataframe['src_port'][i]

            honeynet_dataframe['tag'][i] = honeynet_dataframe['tag'][i]
            honeynet_dataframe['files_filename'][i] = honeynet_dataframe['files.filename'][i]
            honeynet_dataframe['files_md5'][i] = honeynet_dataframe['files.md5'][i]
            honeynet_dataframe['files_state'][i] = honeynet_dataframe['files.state'][i]
            honeynet_dataframe['anomaly_event'][i] = honeynet_dataframe['anomaly.event'][i]
            honeynet_dataframe['anomaly_app_proto'][i] = honeynet_dataframe['anomaly.app_proto'][i]
            honeynet_dataframe['http_url'][i] = honeynet_dataframe['http.url'][i]
            honeynet_dataframe['http_useragent'][i] = honeynet_dataframe['http.http_user_agent'][i]
            honeynet_dataframe['brut_username'][i] = honeynet_dataframe['username'][i]
            honeynet_dataframe['brut_password'][i] = honeynet_dataframe['password'][i]
        else:
            # If the source is external and connection is being made to an external server then it is a case of attack on External Server by an externaly location server on perimeter.
            honeynet_dataframe['attacker_ip'][i] = honeynet_dataframe['src_ip'][i]
            honeynet_dataframe['target_ip'][i] = honeynet_dataframe['dest_ip'][i]
            honeynet_dataframe['ids_threat_class'][i] = honeynet_dataframe['alert.category'][i]
            honeynet_dataframe['ids_threat_type'][i] = honeynet_dataframe['alert.signature'][i]
            honeynet_dataframe['ids_threat_severity'][i] = honeynet_dataframe['alert.severity'][i]
            honeynet_dataframe['type_of_threat'][i] = 'Attack on External Server'
            honeynet_dataframe['attack_timestamp'][i] = honeynet_dataframe['timestamp'][i] 
            honeynet_dataframe['service_name'][i] = honeynet_dataframe['app_proto'][i]
            ##### Addition columns
            if (honeynet_dataframe['event_type'][i] == 'alert'):
                honeynet_dataframe['activity_type'][i] = honeynet_dataframe['alert.category'][i]  
            else:
                honeynet_dataframe['activity_type'][i] = honeynet_dataframe['event_type'][i]
            honeynet_dataframe['mitre_tactics_id'][i] = honeynet_dataframe['alert.metadata.mitre_tactics_id'][i]
            honeynet_dataframe['mitre_tactics_name'][i] = honeynet_dataframe['alert.metadata.mitre_tactics_name'][i]
            honeynet_dataframe['mitre_techniques_id'][i] = honeynet_dataframe['alert.metadata.mitre_techniques_id'][i]
            honeynet_dataframe['mitre_techniques_name'][i] = honeynet_dataframe['alert.metadata.mitre_techniques_name'][i]
            honeynet_dataframe['malware_type'][i] = honeynet_dataframe['alert.metadata.malware_family'][i]
            honeynet_dataframe['attacker_host_type'][i] = honeynet_dataframe['alert.metadata.attack_target'][i]
            honeynet_dataframe['malware_cve_id'][i] = honeynet_dataframe['alert.metadata.cve'][i]
            honeynet_dataframe['intel_source_feed_name'][i] = honeynet_dataframe['alert.metadata.tag'][i]
            honeynet_dataframe['target_port'][i] = honeynet_dataframe['dest_port'][i]
            honeynet_dataframe['attacker_port'][i] = honeynet_dataframe['src_port'][i]

            honeynet_dataframe['tag'][i] = honeynet_dataframe['tag'][i]
            honeynet_dataframe['files_filename'][i] = honeynet_dataframe['files.filename'][i]
            honeynet_dataframe['files_md5'][i] = honeynet_dataframe['files.md5'][i]
            honeynet_dataframe['files_state'][i] = honeynet_dataframe['files.state'][i]
            honeynet_dataframe['anomaly_event'][i] = honeynet_dataframe['anomaly.event'][i]
            honeynet_dataframe['anomaly_app_proto'][i] = honeynet_dataframe['anomaly.app_proto'][i]
            honeynet_dataframe['http_url'][i] = honeynet_dataframe['http.url'][i]
            honeynet_dataframe['http_useragent'][i] = honeynet_dataframe['http.http_user_agent'][i]
            honeynet_dataframe['brut_username'][i] = honeynet_dataframe['username'][i]
            honeynet_dataframe['brut_password'][i] = honeynet_dataframe['password'][i]
   
    # Dropping used fields.
    #=============================================

    honeynet_dataframe = honeynet_dataframe.drop(['src_host_type', 'dst_host_type', 'timestamp', 'os', 'dest_ip','dest_port','src_ip', 'src_port','event_type', 'proto','app_proto', 'alert.signature', 'alert.category', 'alert.severity', 'alert.metadata.affected_product', 'alert.metadata.attack_target', 'alert.metadata.deployment', 'alert.metadata.tag', 'http.hostname', 'http.url', 'http.http_user_agent', 'http.http_method', 'anomaly.app_proto', 'anomaly.type', 'anomaly.event', 'anomaly.layer', 'app','files.md5', 'files.filename', 'files.state', 'anomaly.app_proto', 'username', 'password', 'alert.metadata.mitre_tactics_id', 'alert.metadata.mitre_tactics_name', 'alert.metadata.mitre_techniques_id', 'alert.metadata.mitre_techniques_name', 'alert.metadata.malware_family', 'alert.metadata.attack_target', 'alert.metadata.cve', 'alert.metadata.tag'], axis=1)

    # Adding Timezone of the machine
    #============================
    offset = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
    calculated_offset = offset / 60 / 60 * -1
    honeynet_dataframe['timezone'] = "UTC"+ f"{calculated_offset}"
    print(honeynet_dataframe.head)
    return honeynet_dataframe


def logger(honeynet_data, dpi_data):

    # Filtering data with alert severity  having value 1 for incident logs
    #=============================
    trace_incident_df = honeynet_data[~honeynet_data["ids_threat_severity"].isin([2.0,2,3.0,3,np.nan])]
    trace_incident_df['attack_epoch_time'] = pd.to_datetime(trace_incident_df['attack_timestamp'])
    trace_incident_df = trace_incident_df.drop(["ids_threat_severity"], axis=1)

    # Filtering data with alert severity  having value 2 for alert logs
    #=============================
    trace_alert_df = honeynet_data[~honeynet_data["ids_threat_severity"].isin([1,1.0,3.0,3,np.nan])]
    trace_alert_df['attack_epoch_time'] = pd.to_datetime(trace_alert_df['attack_timestamp'])
    trace_alert_df = trace_alert_df.drop(["ids_threat_severity"], axis=1)
    

    # Filtering data with alert severity  having value 3 or greater for event logs
    #=============================
    trace_event_df = honeynet_data[~honeynet_data["ids_threat_severity"].isin([1,1.0,2,2.0,np.nan])]
    trace_event_df['attack_epoch_time'] = pd.to_datetime(trace_event_df['attack_timestamp'])
    trace_event_df = trace_event_df.drop(["ids_threat_severity"], axis=1)

    # Deleting used dataframe
    #=============================
    del honeynet_data
    gc.collect()

    # Dumping data to files
    #=============================
    trace_incident_df.to_json('/app/trace_incident.json', orient = 'records', lines = True)
    trace_alert_df.to_json('/app/trace_alert.json', orient = 'records', lines = True)
    trace_event_df.to_json('/app/trace_event.json', orient = 'records', lines = True)
    dpi_data.to_json('/app/trace_dpi.json', orient = 'records', lines = True)
    
    # Deleting used dataframe
    #=============================
    del trace_incident_df, trace_alert_df, trace_event_df, dpi_data
    gc.collect()

    return None

def core_pipeline(dpi_path,honeynet_path):

    # Reading data
    #=============================
    honeynet_data = honeynet_data_load(honeynet_path)
    dpi_data = dpi_data_load(dpi_path)
    
    # Processing and Cleaning data
    #=============================
    clean_data = data_cleaner(honeynet_data)

    # Logging data to Files
    #=============================
    logger(clean_data, dpi_data)
    
    # Placing Files to be transmitted
    #==================================
    subprocess.run(["bash","/app/mover.sh"])

    return None

def main():

    # Fetching Source File Locations
    #==================================
    dpi_to_process_file_location = sys.argv[1]
    honeynet_to_process_file_location = sys.argv[2]
    print("[i] Starting Data Processing.")
    core_pipeline( dpi_to_process_file_location, honeynet_to_process_file_location)

if __name__ == "__main__":
    main()


