# Filename : IDS, Ml, Dl Pipeline
# Purpose/Description : The code in this file takes processed data from IDS, ml & dl sends it to the database for presentation.
# Author : Hrushikesh Pradhan
# Copyright (c) : Whizhack Technologies (P) Ltd.
# Revisions/Modifications : Mahesh Banerjee ,Lakshy Sharma , Nihalkumar Parsania

import json, os, gc, warnings, subprocess, sys,time, ndjson
import pandas as pd
from dateutil.tz import tzutc, UTC
import datetime as dt
import time
from linux_helper import *
from win_helper import *


added_count = 6
deleted_count = 12
modified_count = 1
# Setting initial variables for pandas.
pd.options.mode.chained_assignment = None
warnings.filterwarnings('ignore')


def ransomware_detection(raw_dataframe):
    # Ransomware Detection
    raw_dataframe['attack_epoch_time'] = raw_dataframe['timestamp']

    raw_dataframe['timestamp'] = pd.to_datetime(raw_dataframe.timestamp).dt.tz_localize(None)
    raw_dataframe['timestamp'] = raw_dataframe['timestamp'].astype('datetime64[s]')
    raw_dataframe['timestamp'] = raw_dataframe['timestamp'].astype(str)

    for i in raw_dataframe:
        raw_dataframe = raw_dataframe.rename(columns={str(i):str(i).replace('.','_')})

    raw_dataframe['potential_ransomware_event'] = False

    unique_agent_names = raw_dataframe['agent_name'].unique()

    # Columns for Ransomware Detection

    ransomware_detection_cols = ['attack_epoch_time', 'agent_id', 'agent_name','agent_ip','syscheck_path', 'rule_description','syscheck_event','decoder_name']
    temp_selected_columns = raw_dataframe
    for i in ransomware_detection_cols:
        if i not in temp_selected_columns.columns:
            temp_selected_columns[i] = np.nan
    temp_selected_columns = temp_selected_columns[ransomware_detection_cols]
    selected_columns = temp_selected_columns.loc[:, ['attack_epoch_time', 'agent_id', 'agent_name','agent_ip','syscheck_path', 'rule_description','syscheck_event','decoder_name']]
    del temp_selected_columns

    for agent_name in unique_agent_names:
        unique_agent_df = selected_columns[selected_columns['agent_name'] == agent_name]
        unique_agent_df = unique_agent_df.dropna(subset=['syscheck_path'])
        result_df = unique_agent_df.groupby('agent_name').filter(
        lambda x: (x['syscheck_event'] == 'added').sum() >= added_count and
                (x['syscheck_event'] == 'deleted').sum() >= deleted_count and
                (x['syscheck_event'] == 'modified').sum() >= modified_count
        )    
        if result_df.empty:
            pass
        else:
            raw_dataframe.loc[raw_dataframe['agent_name']== agent_name , 'potential_ransomware_event'] = True
        
    return raw_dataframe


def linux_ai_analyser(raw_dataframe):

    raw_dataframe=feature_manipulation(raw_dataframe)

    raw_dataframecc = pd.read_json('linux/data.json', lines = True)
    raw_dataframe['User_Name'] = raw_dataframe['agent.name'].map(raw_dataframecc.set_index('Asset_Id')['User_Name']) 
    raw_dataframe['Os_Info'] = raw_dataframe['agent.name'].map(raw_dataframecc.set_index('Asset_Id')['OS_Info'])

    # Define a function to replace 'old_word' with 'new_word' in a string
    def replace_word(text):
        if isinstance(text, str):
            return text.replace('wazuh', 'HIDS')
        else:
            return text
    # Apply the replace_word function to each cell in the DataFrame using .applymap()
    raw_dataframe = raw_dataframe.applymap(replace_word)
    # Resetting index and dropping null values in source host and destination host.
    linux_ai_dataframe = raw_dataframe.reset_index(drop=True)

    return linux_ai_dataframe


def windows_ai_analyser(raw_dataframe):

    raw_dataframe = feature_manupulation(raw_dataframe)
    owner = {
            "L-001": "Jyoti",
            "L-008": "Devansh",
            "L-009": "Malvika",
            "L-011": "Divya",
            "L-012": "Piyush",
            "L-013": "Meghna",
            "L-015": "Harihar",
            "L-018": "Sarvesh",
            "L-020": "Rajat",
            "L-026": "Vidhushi",
            "L-031": "Sai",
            "L-032": "Danish",
            "L-033": "Baby",
            "L-034": "Priya",
            "L-035": "Jaydeep",
            "L-038": "Divyansh",
            "L-022": "Hemang"
        }
    # Map owner names to the 'owner' column based on 'agent.name'
    raw_dataframe['User_Name'] = raw_dataframe['agent.name'].map(owner)
    raw_dataframe['Os_Info'] = "Windows"
    # Release memory by deleting the 'owner' dictionary and running garbage collection
    del owner
    gc.collect()
    # Define a function to replace 'old_word' with 'new_word' in a string
    def replace_word(text):
        if isinstance(text, str):
            return text.replace('wazuh', 'HIDS')
        else:
            return text
        
    # Apply the replace_word function to each cell in the DataFrame using .applymap()
    raw_dataframe = raw_dataframe.applymap(replace_word)
    # Resetting index and dropping null values in source host and destination host.
    windows_ai_dataframe = raw_dataframe.reset_index(drop=True)

    return windows_ai_dataframe

def linux_and_windows_data_appender(linux_ai_dataframe, windows_ai_dataframe):

    ai_analyse_dataframe = pd.concat([linux_ai_dataframe, windows_ai_dataframe], axis=0, ignore_index=True)

    return ai_analyse_dataframe


def core_pipeline(wazuh_path):
    ''' This function reads data from the required files, merges them and pushes them into the database after some processing. '''
    # Creating work copies of the data.
    #===================================

    raw_dataframe = pd.read_json(wazuh_path, lines=True)
    raw_dataframe['attack_epoch_time'] = raw_dataframe['timestamp']

    linux_df = linux_ai_analyser(raw_dataframe)
    windows_df = windows_ai_analyser(raw_dataframe)
    
    combine_df = linux_and_windows_data_appender(linux_df, windows_df)

    df_with_ransom = ransomware_detection(combine_df)
    
    ####

    wazuh_incident_df = df_with_ransom[~df_with_ransom["rule_level"].isin([0,1,2,3,4,5,6,7,8,9,10])]

    wazuh_alert_df = df_with_ransom[~df_with_ransom["rule_level"].isin([0,1,2,3,4,5,6,7,11,12,13,14,15])]

    wazuh_event_df = df_with_ransom[~df_with_ransom["rule_level"].isin([8,9,10,11,12,13,14,15])]

    wazuh_incident_df.to_json('/app/wazuh_incident.json', orient = 'records', lines = True)
    wazuh_alert_df.to_json('/app/wazuh_alert.json', orient = 'records', lines = True)
    wazuh_event_df.to_json('/app/wazuh_event.json', orient = 'records', lines = True)

    #final_output.to_json('/app/temp.json', orient = 'records', lines = True)
    subprocess.run(["bash","/app/mover.sh"])

    return None

def main():
    wazuh_to_process_file_location = sys.argv[1]
    #asset_to_process_file_location = sys.argv[3]

    print("[i] Starting Data Processing.")
    core_pipeline(wazuh_to_process_file_location) #, asset_to_process_file_location)

if __name__ == "__main__":
    main()


