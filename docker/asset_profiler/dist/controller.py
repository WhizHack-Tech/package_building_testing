# Filename : IDS Filter
# Purpose/Description : The code in this file takes processed data from IDS and sends it to the database for presentation.
# Author : Hrushikesh Pradhan
# Copyright (c) : Whizhack Technologies (P) Ltd.
# Revisions/Modifications : Mahesh Banerjee ,Lakshy Sharma , Nihalkumar Parsania, Amisha Prashar

import os, re, gc, subprocess, configparser

def config_reader():
    ''' This function will read all the configurations from the config.ini file and pass them to the scripts. '''
    config_object = configparser.ConfigParser()
    config_object.read("config.ini")
    locations = config_object["LOCATIONS"]
    return locations

def file_lookup(packet_path, packet_processed_file_location):
    ''' This function simply looks if the files exists or not.'''
    # Setting the regex expression.
    regex_exp = re.compile(r'part-\d{4}-\d{2}-\d{2}-\d{2}-\d{2}\.json$')
    while True:
        # Searching packet files.
        try:
            # Creating a list of files in the packets folder.
            packet_files_list = list(filter(regex_exp.search,os.listdir(packet_path)))
            packet_files_list.remove(max(packet_files_list))
            packet_to_process_file = max(packet_files_list)
            packet_to_process_file_location = packet_path + packet_to_process_file
            #print(packet_to_process_file_location)
            del packet_files_list
            gc.collect()
        except ValueError:
            continue
        if (packet_to_process_file_location != packet_processed_file_location):  
            # Files are new, berak and return to main loop.
            break
        else:
            continue
    del regex_exp
    gc.collect()
    return packet_to_process_file_location    
    
def file_expunger(packet_processed_file_location): 
    ''' This function deletes processed files to save disk space. '''
    os.remove(packet_processed_file_location)
    return None

def main():
    ''' This is the main function for orchestration. '''
    locations = config_reader()
    packet_path = locations["packet_path"]
    packet_processed_file_location = 0
    print("[i] Entering the processing loop.")
    while True:
        #packet_path = /var/log/zerohack/normalized_data/listener/
        packet_to_process_file_location = file_lookup(packet_path, packet_processed_file_location)
        subprocess.run(["python3", "/app/process.py", f"{packet_to_process_file_location}"])
        print('File Processed')
        packet_processed_file_location = packet_to_process_file_location
        print("[*] Deleting used files.")
        file_expunger(packet_processed_file_location)
        
         
if __name__ == "__main__":
    main()
