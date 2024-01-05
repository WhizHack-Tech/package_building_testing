# Filename : Asset Profiler
# Purpose/Description : The code in this file takes processed data from listener adds visted domians and their reputation related information to it and sends it to the database for presentation.
# Author : Amisha Prashar
# Copyright (c) : Whizhack Technologies (P) Ltd.
# Revisions/Modifications : N/A

import json, os, gc, pickle, warnings, subprocess, sys,time, ndjson
import pandas as pd
import polars as pl
import numpy as np
import subprocess
import threading
from ua_parser import user_agent_parser
from dateutil.tz import tzutc, UTC
from ipaddress import ip_address
import ipaddress
import socket
# Setting initial variables for pandas.
pd.options.mode.chained_assignment = None
warnings.filterwarnings('ignore')

def list2Str(lst):
    try:
        if isinstance(lst, list):
            return",".join(lst)
        else:
            return lst
    except:
        print('Error in casting list: ', lst, sys.exc_info()[0])
        
def dns_lookup(attacker_ip, final_data):
    try:
        hostname = socket.gethostbyaddr(attacker_ip)[0]
        final_data['domain_name'] = hostname
    except socket.herror:
        final_data['domain_name'] = attacker_ip
       
def search_json(global_threat_dict_path, search_value, final_data):
    with open(global_threat_dict_path, 'r') as json_file:
        data = ndjson.load(json_file)
        for item in data:
            if search_value in item.values():
                items = list(item.values())
                final_data['attacker_domain'] = items[3]
                final_data['malware_type'] = items[4]
                final_data['intel_source_feed_name'] = items[5]
        final_data['attacker_domain'] = None
        final_data['malware_type'] = None
        final_data['intel_source_feed_name'] = None
    
def asset_profiler(packet_path, global_threat_dict_path): 
    raw_dataframe = pd.read_json(packet_path, lines=True)
    required_columns = ['id','timestamp', 'app_linkage','layer.ip.ip.src_host', 'layer.ip.ip.dst_host','layer.eth.eth.src', 'layer.eth.eth.dst','layer.tcp.tcp.srcport','layer.udp.udp.srcport','layer.tcp.tcp.dstport','layer.udp.udp.dstport']
    available_columns = []
    sanitised_dataframe = raw_dataframe.dropna(axis=0, subset=['timestamp','layer.ip.ip.dst_host', 'layer.ip.ip.src_host', 'layer.eth.eth.src', 'layer.eth.eth.dst']).reset_index(drop = True)
    sanitised_dataframe = sanitised_dataframe.fillna(np.nan)
    for i in required_columns:
        if i in sanitised_dataframe.columns:
            available_columns.append(i)
    required_features = sanitised_dataframe.loc[:,available_columns]
    srcport_cols = [col for col in required_features.columns if 'srcport' in col]
    required_features['src_port'] = required_features[srcport_cols].apply(lambda row: row[row.first_valid_index()] if row.first_valid_index() else 0, axis=1)
    required_features['src_port'].fillna(0, inplace=True)
    # Extracting destination port details
    dstport_cols = [col for col in required_features.columns if 'dstport' in col]
    required_features['dstport'] = required_features[dstport_cols].apply(lambda row: row[row.first_valid_index()] if row.first_valid_index() else 0, axis=1)
    required_features['dstport'].fillna(0, inplace=True)
    # Deleted list
    processed_data=required_features.drop(srcport_cols+dstport_cols, axis = 1)
    #print(required_features.head()) # for debugging
    
    processed_data['src_host_type']= required_features['layer.ip.ip.src_host'].apply([lambda x: 'internal' if ip_address(x).is_private else 'external'])
    processed_data['dst_host_type']= required_features['layer.ip.ip.dst_host'].apply([lambda x: 'internal' if ip_address(x).is_private else 'external'])
    #Required Columns:
    #==================
    new_columns = ['service_name','attacker_ip','attacker_mac','attack_timestamp','target_ip','target_mac','type_of_threat','packet_id','malware_type','attacker_domain', 'intel_source_feed_name','attacker_port', 'target_port', 'visited_domain', 'host_id']
    # New column creator loop.
    for i in range(len(new_columns)):
        last_column = len(processed_data.columns)
        processed_data.insert(loc=last_column, column=new_columns[i],value=None)
    del last_column
    gc.collect()

    processed_data = processed_data.reset_index(drop=True)
    for i in range(len(processed_data.src_host_type)):
        if (processed_data['src_host_type'][i] == 'external') and (processed_data['dst_host_type'][i] == 'internal'):
            # If the source is external and destination is internal then we will assume the machine is being attacked.
            processed_data['attacker_ip'][i] = processed_data['layer.ip.ip.src_host'][i]
            processed_data['attacker_mac'][i] = processed_data['layer.eth.eth.src'][i]
            processed_data['target_ip'][i] = processed_data['layer.ip.ip.dst_host'][i]
            processed_data['target_mac'][i] = processed_data['layer.eth.eth.dst'][i]
            processed_data['type_of_threat'][i] = 'External Attack'
            processed_data['packet_id'][i] = processed_data['id'][i]
            processed_data['attack_timestamp'][i] = processed_data['timestamp'][i]
            processed_data['service_name'][i] = processed_data['app_linkage'][i]
            processed_data['target_port'][i] = processed_data['dstport'][i]
            processed_data['attacker_port'][i] = processed_data['src_port'][i]
            #search_json(global_threat_dict_path,  processed_data['attacker_ip'][i], processed_data, 'attacker_ip')
     
        elif (processed_data['src_host_type'][i] == 'internal') and (processed_data['dst_host_type'][i] == 'external'):
            # If the source is internal and connection is being made externally then we will assume the machine is talking to a CNC server as internal people cannot do anything bad.
            processed_data['attacker_ip'][i] = processed_data['layer.ip.ip.dst_host'][i]
            processed_data['attacker_mac'][i] = processed_data['layer.eth.eth.dst'][i]
            processed_data['target_ip'][i] = processed_data['layer.ip.ip.src_host'][i]
            processed_data['target_mac'][i] = processed_data['layer.eth.eth.src'][i]
            processed_data['type_of_threat'][i] = 'Internal Compromised Machine'
            processed_data['packet_id'][i] = processed_data['id'][i]
            processed_data['attack_timestamp'][i] = processed_data['timestamp'][i]
            processed_data['service_name'][i] = processed_data['app_linkage'][i]
            processed_data['attacker_port'][i] = processed_data['dstport'][i]
            processed_data['target_port'][i] = processed_data['src_port'][i]
            #search_json(global_threat_dict_path,  processed_data['target_ip'][i], processed_data, 'target_ip')
     
        elif (processed_data['src_host_type'][i] == 'internal') and (processed_data['dst_host_type'][i] == 'internal'):
            # If the source is internal and connection is being made internally then it is either the case of internal communication or a possible insider attack.
            processed_data['attacker_ip'][i] = processed_data['layer.ip.ip.src_host'][i]
            processed_data['attacker_mac'][i] = processed_data['layer.eth.eth.src'][i]
            processed_data['target_ip'][i] = processed_data['layer.ip.ip.dst_host'][i]
            processed_data['target_mac'][i] = processed_data['layer.eth.eth.dst'][i]
            processed_data['type_of_threat'][i] = 'Lateral Movement'
            processed_data['packet_id'][i] = processed_data['id'][i]
            processed_data['attack_timestamp'][i] = processed_data['timestamp'][i]
            processed_data['service_name'][i] = processed_data['app_linkage'][i]
            processed_data['target_port'][i] = processed_data['dstport'][i]
            processed_data['attacker_port'][i] = processed_data['src_port'][i]
            #search_json(global_threat_dict_path, processed_data['target_ip'][i], processed_data, 'target_ip')
     
        else:
            # If the source is external and connection is being made to an external server then it is a case of attack on External Server by an externaly location server on perimeter.
            processed_data['attacker_ip'][i] = processed_data['layer.ip.ip.src_host'][i]
            processed_data['attacker_mac'][i] = processed_data['layer.eth.eth.src'][i]
            processed_data['target_ip'][i] = processed_data['layer.ip.ip.dst_host'][i]
            processed_data['target_mac'][i] = processed_data['layer.eth.eth.dst'][i]
            processed_data['type_of_threat'][i] = 'Attack on External Server'
            processed_data['packet_id'][i] = processed_data['id'][i]
            processed_data['attack_timestamp'][i] = processed_data['timestamp'][i]
            processed_data['service_name'][i] = processed_data['app_linkage'][i]         
            processed_data['target_port'][i] = processed_data['dstport'][i]
            processed_data['attacker_port'][i] = processed_data['src_port'][i]
            #search_json(global_threat_dict_path,  processed_data['attacker_ip'][i], processed_data, 'attacker_ip')
    
    # Dropping used fields.
    #=============================================
    processed_data = processed_data.drop(['dstport','src_port','id','src_host_type','dst_host_type','layer.ip.ip.src_host', 'layer.ip.ip.dst_host', 'layer.eth.eth.src','layer.eth.eth.dst', 'app_linkage'], axis=1)
    
    # Fixing timestamps
    #============================
    offset = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
    calculated_offset = offset / 60 / 60 * -1
    processed_data['timezone'] = "UTC"+ f"{calculated_offset}"
    print(processed_data.shape)
    
    # Flow data anlaysis for finding the internal target hosts external communication.
    #=============================
    # Initializing variables.
     
    df = pd.DataFrame(processed_data)

    # Group the DataFrame by 'target_ip' and aggregate the 'attacker_ip' and 'service_name' columns
    grouped_data = df.groupby('target_ip').agg({'attacker_ip': 'unique', 'service_name': 'first'})

    final_data_list = []  # Create an empty list to store dictionaries

    for target_ip, row in grouped_data.iterrows():
        attacker_ips = row['attacker_ip']
        service_name = row['service_name']
        for attacker_ip in attacker_ips:
            df_final_data = {'target_ip': target_ip, 'service_name': service_name}
            dns_lookup(attacker_ip, df_final_data)
            search_json(global_threat_dict_path, attacker_ip, df_final_data)
            final_data_list.append(df_final_data)

    data_to_temp = pd.DataFrame(final_data_list)
    data_to_temp.to_json('/var/log/data/processed_data/asset/asset.json', orient='records', lines=True)
    
def main():
    packet_to_process_file_location = sys.argv[1]
    global_threat_dict_path = '/app/it_globalFeed.ndjson'

    print("[i] Starting Data Processing.")
    asset_profiler(packet_to_process_file_location, global_threat_dict_path) 

if __name__ == "__main__":
    main()

    
