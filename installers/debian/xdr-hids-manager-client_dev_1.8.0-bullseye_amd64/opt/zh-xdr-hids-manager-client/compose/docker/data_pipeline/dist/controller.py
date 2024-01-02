# Filename : IDS Filter
# Purpose/Description : The code in this file takes processed data from IDS and sends it to the database for presentation.
# Author : Hrushikesh Pradhan
# Copyright (c) : Whizhack Technologies (P) Ltd.
# Revisions/Modifications : Mahesh Banerjee ,Lakshy Sharma , Nihalkumar Parsania

import os, re, gc, subprocess, configparser

def config_reader():
    ''' This function will read all the configurations from the config.ini file and pass them to the scripts. '''
    config_object = configparser.ConfigParser()
    config_object.read("config.ini")
    locations = config_object["LOCATIONS"]
    return locations

def file_lookup(wazuh_path, wazuh_processed_file_location):
    ''' This function simply looks if the files exists or not.'''
    # Setting the regex expression.
    regex_exp = re.compile(r'part-\d{4}-\d{2}-\d{2}-\d{2}-\d{2}\.json$')
    while True:
        # Searching wazuh files.
        try:
            # Creating a list of files in the wazuhs folder.
            wazuh_files_list = list(filter(regex_exp.search,os.listdir(wazuh_path)))
            wazuh_files_list.remove(max(wazuh_files_list))
            wazuh_to_process_file = max(wazuh_files_list)
            wazuh_to_process_file_location = wazuh_path + wazuh_to_process_file
            del wazuh_files_list
            gc.collect()
        except ValueError:
            continue
        # Searching event files.
    
        # Searching asset files.
        #try:
        #    asset_files_list = list(filter(regex_exp.search,os.listdir(asset_path)))
        #    asset_files_list.remove(max(asset_files_list))
        #    asset_to_process_file = max(asset_files_list)
        #    asset_to_process_file_location = asset_path + asset_to_process_file
        #except ValueError:
        #    continue

        # Check if the wazuh, event and asset files have the same timestamp.

        if (wazuh_to_process_file_location != wazuh_processed_file_location): # and (asset_to_process_file_location != asset_processed_file_location):
            # Files are new, berak and return to main loop.
            break
        # If the previous file is same as the latest file then go back to loop.
        else:
            # Try removing latest asset fi
            continue
    # Cleanup and exit function.
    del regex_exp
   # del asset_files_list
    gc.collect()
    return wazuh_to_process_file_location# asset_to_process_file_location

def file_expunger(wazuh_processed_file_location): #, asset_processed_file_location):
    ''' This function deletes processed files to save disk space. '''
    os.remove(wazuh_processed_file_location)
   # os.remove(asset_processed_file_location)
    return None

def main():
    ''' This is the main function for orchestration. '''
    locations = config_reader()
    wazuh_path = locations["wazuh_path"]
    #asset_path = locations["asset_path"]
    wazuh_processed_file_location = 0
    #asset_processed_file_location = 0
    print("[i] Entering the processing loop.")
    while True:
        wazuh_to_process_file_location = file_lookup(wazuh_path, wazuh_processed_file_location)
        subprocess.run(["python3", "/app/processor.py", f"{wazuh_to_process_file_location}"])#, f"{asset_to_process_file_location}"]) 
        wazuh_processed_file_location = wazuh_to_process_file_location
       # asset_processed_file_location = asset_to_process_file_location
        file_expunger(wazuh_processed_file_location)#, asset_processed_file_location)

if __name__ == "__main__":
    main()
