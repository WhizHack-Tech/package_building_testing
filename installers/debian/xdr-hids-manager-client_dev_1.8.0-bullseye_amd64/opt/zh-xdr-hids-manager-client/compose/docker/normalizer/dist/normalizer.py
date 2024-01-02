# Complete datetime format.
from datetime import datetime
# Complete default libraries.
import time, json, os, re, gc
# Complete config processing libraries.
from configparser import ConfigParser
# Complete data processing libraries.
import pandas as pd


def config_reader():
    ''' This function will read all the configurations from the config.ini file and pass them to the scripts. '''
    # Creating a configuration object.
    config_object = ConfigParser()
    # Reading the config file using the object.
    config_object.read("config.ini")
    # Collecting configurations.
    locations = config_object["LOCATIONS"]
    # Returning all values to main function for transport elsewhere.
    return locations

def file_lookup(wazuh_path, wazuh_processed_file_location):
    ''' This function simply looks if the files exists or not.'''
    # Setting the regex expression.
    regex_exp = re.compile(r'part-\d{4}-\d{2}-\d{2}-\d{2}-\d{2}\.json$')
    while True:
        # Searching for valid wazuh files.
        try:
            # Creating a list of files in the wazuhs folder.
            wazuh_files_list = list(filter(regex_exp.search,os.listdir(wazuh_path)))
            
            # Finding the latest file and removing it from the list to avoid the file that logstash is still using.
            wazuh_files_list.remove(max(wazuh_files_list))
            
            # Finding the new latest file to process.
            wazuh_to_process_file = max(wazuh_files_list)
            
            # Creating the latest file location.
            wazuh_to_process_file_location = wazuh_path + wazuh_to_process_file
            
            del wazuh_files_list
            gc.collect()
            
        except ValueError:
            continue
        
        # Check if the packet, event and asset files have the same timestamp.
        if (wazuh_to_process_file_location != wazuh_processed_file_location):
            # Files are new, berak and return to main loop.
            break
        # If the previous file is same as the latest file then go back to loop.
        else:
            continue
        
    # Cleanup and exit function.
    del regex_exp
    gc.collect()
        
    return wazuh_to_process_file_location, wazuh_to_process_file

def normalize(wazuh_path, wazuh_filename, destination_path ):
    # Reading wazuh file and normalizing the data.
    with open(wazuh_path, 'r', encoding='latin-1') as file:
       
        wazuh_data=[json.loads(line.rstrip("\n")) for line in file]
        
        pkt_dataframe = pd.json_normalize(wazuh_data)
        
        print(pkt_dataframe.columns)
        
        pkt_dataframe.to_json(destination_path + 'wazuh/'+wazuh_filename, orient='records', lines=True)
        del pkt_dataframe
        gc.collect()
    return None

def file_expunger(wazuh_processed_file_location):
    ''' This function deletes processed files to save disk space. '''
    os.remove(wazuh_processed_file_location)
    return None

def main():
    ''' This is the main function for orchestration. '''
    # Capturing the configurations.
    locations = config_reader()
    # Setting the target files
    wazuh_path = locations["wazuh_path"]
    destination_path = locations["destination_path"]
    # Setting the timestamp we need to look for.
    wazuh_processed_file_location = 0
    # Starting an infinite loop.
    
    while True:
        print("[*] Starting the normalization loop.")
        # Catching the files which needs to be processed and passing it to the merger.
        wazuh_to_process_file_location, wazuh_to_process_file = file_lookup(wazuh_path, wazuh_processed_file_location)
        print("[*] Found valid files. Starting normalization.")
        
        # Calling the normalizer function.
        normalize(wazuh_to_process_file_location, wazuh_to_process_file, destination_path)
        
        # Updating the processed file variables.
        wazuh_processed_file_location = wazuh_to_process_file_location
        
        # Expunging function which deletes the files once they have been processed to save disk space.
        print("[*] Deleting used files.")
        file_expunger(wazuh_processed_file_location)

# Starting the function.
if __name__ == '__main__':
    # Calling main function to start merging the files.
    main()

