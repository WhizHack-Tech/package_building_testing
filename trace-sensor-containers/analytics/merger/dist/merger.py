''' Filename : merger.py (merger)
    Purpose/Description : This program is a merger script which merges packet and event data together.
    Author : Hrushikesh Pradhan, Rajat Sharma.
    Revised By : Mahesh Banerjee, Lakshy Sharma.
    Copyright (c) : Whizhack Technologies (P) Ltd.'''

# Complete datetime format.
from datetime import datetime
# Complete default libraries.
import json, gc, subprocess,sys
# Complete data processing libraries.
import pandas as pd
# Setting initial variables for pandas.
pd.options.mode.chained_assignment = None

def merge_function(packet_path, suricata_path, merged_path):
    ''' This is function merges the packet and event files together and stores the output. '''

    # Reading packet and event files and preparing them for processing.
    with open(packet_path) as packet_file:
        pkt_dataframe = pd.read_json(packet_file, lines=True)
        del packet_file
        gc.collect()
    with open(suricata_path) as event_file:
        eve_dataframe = pd.read_json(event_file, lines=True)
        del event_file
        gc.collect()

    # Try to load the required fields from our events files.
    try:
        eve_dataframe = eve_dataframe[['timestamp', 'src_ip', 'dest_ip', 'event_type', 'alert.signature', 'alert.category', 'alert.severity']]
    # If there are no alerts then insert the None values in alert related fields.
    except:
        # Capture existing fields.
        eve_dataframe = eve_dataframe[['timestamp', 'src_ip', 'dest_ip', 'event_type']]
        # Calculate the last column.
        last_column = len(eve_dataframe.columns)
        # Insert the alert.signature column.
        eve_dataframe.insert(loc=last_column, column='alert.signature',value=None)
        # Update the last column.
        last_column = last_column + 1
        # Insert the alert.category column.
        eve_dataframe.insert(loc=last_column, column='alert.category',value=None)
        # Update the last column.
        last_column = last_column + 1
        # Insert the alert.severity column.
        eve_dataframe.insert(loc=last_column, column='alert.severity',value=0)
        # Cleanup used variables.
        del last_column
        gc.collect()

    # Iterate over each existing timestamp and fix the format for eve dataframe.
    eve_dataframe['timestamp']  =  eve_dataframe['timestamp'] = pd.to_datetime(eve_dataframe.timestamp).dt.tz_localize(None) 
    # Dropping any duplicates and resetting our indexes.
    eve_dataframe = eve_dataframe.dropna(axis=0, subset=['timestamp']).reset_index(drop = True)
    # Performing the merge operation with timestamp matching.
    merged_dataframe = pd.merge_asof(pkt_dataframe.sort_values('timestamp'), eve_dataframe.sort_values('timestamp'), on='timestamp', direction='forward')

    # Intermediate cleaning.
    del eve_dataframe
    gc.collect()
    del pkt_dataframe
    gc.collect()

    # Dropping any null values in the IP fields and fixing the broken indexes.
    merged_dataframe = merged_dataframe.dropna(axis=0, subset=['layer.ip.ip.dst_host', 'layer.ip.ip.src_host', 'src_ip', 'dest_ip']).reset_index(drop = True)
    # Define conditions for swapping the values of 'layer.ip.ip.src_host' and 'layer.ip.ip.dst_host'
    cond1 = (merged_dataframe['layer.ip.ip.src_host'] == merged_dataframe['src_ip']) & (merged_dataframe['layer.ip.ip.dst_host'] == merged_dataframe['dest_ip'])
    cond2 = (merged_dataframe['layer.ip.ip.src_host'] == merged_dataframe['dest_ip']) & (merged_dataframe['layer.ip.ip.dst_host'] == merged_dataframe['src_ip'])
    # Create a new dataframe with the rows that match condition 2
    swaping_dataframe = merged_dataframe.loc[cond2].reset_index(drop=True)
    # Swap the values of 'layer.ip.ip.dst_host' and 'layer.ip.ip.src_host' in the new dataframe
    swaping_dataframe['layer.ip.ip.dst_host'], swaping_dataframe['layer.ip.ip.src_host'] = swaping_dataframe['dest_ip'], swaping_dataframe['src_ip']
    # Select the rows that match condition 1 in the original dataframe
    merged_dataframe = merged_dataframe.loc[cond1].reset_index(drop=True)
    # Concatenate the original dataframe and the new dataframe, and reset the index
    merged_dataframe = pd.concat([merged_dataframe, swaping_dataframe], axis = 0, ignore_index = True)
    # ******************************************************************************************************************
    # Dropping the unused columns and resetting our indexes.
    merged_dataframe = merged_dataframe.drop(['src_ip', 'dest_ip'], axis =1).reset_index(drop = True)
    # Exporting merged data to a temporary json file.
    merged_dataframe.to_json('/app/temp.json', orient='records', lines=True)
    # Final cleaning.
    del merged_dataframe,cond1, cond2,swaping_dataframe
    gc.collect()
    # Moving our merged file to its place.
    subprocess.run(["bash","/app/mover.sh"])
    #return print("[*] Successfully merged files. ")
    return None

def main(packet_to_process_file_location, event_to_process_file_location, merged_path):
    ''' This is the main function for orchestration. '''
    #packet_to_process_file_location = sys.argv[1]
    #event_to_process_file_location = sys.argv[2]
    #merged_path = sys.argv[3]
    # Creating a dedicated object and merging files.
    merge_function(packet_to_process_file_location, event_to_process_file_location, merged_path)
    sys.exit(0)

# Starting the function.
if __name__ == '__main__':
    # Calling main function to start merging the files.
    main()
