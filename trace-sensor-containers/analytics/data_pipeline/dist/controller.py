# Filename : Trace Data Pipeline Controller
# Purpose/Description : The code in this file takes processed data from from TRACE Components such as honeypots, P0f, FATT, IDS and DPI Engines and sends it to the Processor Component.
# Author : Nikhilesh Kumar, Nikhil Garg
# Copyright (c) : Whizhack Technologies (P) Ltd.
# Revisions/Modifications : Mahesh Banerjee

import os, re, gc, subprocess, configparser

def config_reader():
    ''' This function will read all the configurations from the config.ini file and pass them to the scripts. '''
    config_object = configparser.ConfigParser()
    config_object.read("config.ini")
    locations = config_object["LOCATIONS"]
    return locations

def file_lookup(dpi_path, honeynet_path, dpi_processed_file_location, honeynet_processed_file_location):
    ''' This function simply looks if the files exists or not.'''
    # Setting the regex expression.
    regex_exp = re.compile(r'part-\d{4}-\d{2}-\d{2}-\d{2}-\d{2}\.json$')
    while True:
        # Searching dpi files.
        try:
            # Creating a list of files in the dpis folder.
            dpi_files_list = list(filter(regex_exp.search,os.listdir(dpi_path)))
            dpi_files_list.remove(max(dpi_files_list))
            dpi_to_process_file = max(dpi_files_list)
            dpi_to_process_file_location = dpi_path + dpi_to_process_file
            del dpi_files_list
            gc.collect()
        except ValueError:
            continue
        # Searching honeynet files.
        try:
            honeynet_files_list = list(filter(regex_exp.search,os.listdir(honeynet_path)))
            honeynet_files_list.remove(max(honeynet_files_list))
            honeynet_to_process_file = max(honeynet_files_list)
            honeynet_to_process_file_location = honeynet_path + honeynet_to_process_file
            del honeynet_files_list
            gc.collect()
        except ValueError:
            continue
        # Searching asset files.

        # Check if the dpi, honeynet and asset files have the same timestamp.
        if (dpi_to_process_file == honeynet_to_process_file): #and (dpi_to_process_file == asset_to_process_file):
            # Check if the files have been processed earlier or not.
            if (dpi_to_process_file_location != dpi_processed_file_location) and (honeynet_to_process_file_location != honeynet_processed_file_location): # and (asset_to_process_file_location != asset_processed_file_location):
                # Files are new, berak and return to main loop.
                break
        # If the previous file is same as the latest file then go back to loop.
        else:
            # Try removing latest asset file.
            # Check if the dpi, honeynet and asset files have the same timestamp.
            if (dpi_to_process_file == honeynet_to_process_file): #and (dpi_to_process_file == asset_to_process_file):
                # Check if the files have been processed earlier or not.
                if (dpi_to_process_file_location != dpi_processed_file_location) and (honeynet_to_process_file_location != honeynet_processed_file_location): #and (asset_to_process_file_location != asset_processed_file_location):
                    # Files are new, berak and return to main loop.
                    break
            else:
                continue
    # Cleanup and exit function.
    del regex_exp
   # del asset_files_list
    gc.collect()
    return dpi_to_process_file_location, honeynet_to_process_file_location # asset_to_process_file_location

def file_expunger(dpi_processed_file_location, honeynet_processed_file_location): #, asset_processed_file_location):
    ''' This function deletes processed files to save disk space. '''
    os.remove(dpi_processed_file_location)
    os.remove(honeynet_processed_file_location)
    return None

def main():
    ''' This is the main function for orchestration. '''
    locations = config_reader()
    honeynet_path = locations["honeynet_path"]
    dpi_path = locations["dpi_path"]
    dpi_processed_file_location = 0
    honeynet_processed_file_location = 0
    print("[i] Entering the processing loop.")
    while True:
        dpi_to_process_file_location, honeynet_to_process_file_location = file_lookup(dpi_path, honeynet_path, dpi_processed_file_location, honeynet_processed_file_location)
        subprocess.run(["python3", "/app/processor.py", f"{dpi_to_process_file_location}", f"{honeynet_to_process_file_location}"])#, f"{asset_to_process_file_location}"]) 
        dpi_processed_file_location = dpi_to_process_file_location
        honeynet_processed_file_location = honeynet_to_process_file_location
        print("[*] Deleting used files.")
        file_expunger(dpi_processed_file_location, honeynet_processed_file_location)#, asset_processed_file_location)

if __name__ == "__main__":
    main()
