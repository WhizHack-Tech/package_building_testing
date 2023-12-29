''' Filename : controller.py (merger)
    Purpose/Description : This program is a controller script written for managing the merger script.
    Author : Lakshy Sharma (Cyber Security Engineer)
    Revised By : Mahesh Banerjee (Cyber Security Engineer)
    Copyright (c) : Whizhack Technologies (P) Ltd.'''

# Complete default libraries.
import time, os, re, gc, subprocess
# Complete config processing libraries.
from configparser import ConfigParser

def config_reader():
    ''' This function will read all the configurations from the config.ini file and pass them to the scripts. '''
    # Creating a configuration object.
    config_object = ConfigParser()
    # Reading the config file using the object.
    config_object.read("/app/config.ini")
    # Collecting configurations.
    variables = config_object["MERGER-VARIABLES"]
    locations = config_object["MERGER-LOCATIONS"]
    del config_object
    gc.collect()
    # Returning all values to main function for transport elsewhere.
    return variables, locations

def file_lookup(packet_path, event_path, packet_processed_file_location, event_processed_file_location):
    ''' This function simply looks if the files exists or not.'''
    # Setting the regex expression.
    regex_exp = re.compile(r'part-\d{4}-\d{2}-\d{2}-\d{2}-\d{2}\.json$')
    while True:
        # Searching for valid packet files.
        try:
            # Creating a list of files in the packets folder.
            packet_files_list = list(filter(regex_exp.search,os.listdir(packet_path)))
            # Finding the latest file and removing it from the list to avoid the file that logstash is still using.
            packet_files_list.remove(max(packet_files_list))
            # Finding the new latest file to process.
            packet_to_process_file = max(packet_files_list)
            # Creating the latest file location.
            packet_to_process_file_location = packet_path + packet_to_process_file
            del packet_files_list
            gc.collect()
        except ValueError:
            time.sleep(10)
            continue
        # Searching for valid event files.
        try:
            event_files_list = list(filter(regex_exp.search,os.listdir(event_path)))
            event_files_list.remove(max(event_files_list))
            event_to_process_file = max(event_files_list)
            event_to_process_file_location = event_path + event_to_process_file
            del event_files_list
            gc.collect()
        except ValueError:
            time.sleep(10)
            continue
        # Checking if the packet and event files have the same timestamp or not.
        if packet_to_process_file == event_to_process_file:
            # If the timestamp is same then check if the files have been processed earlier or not.
            if (packet_to_process_file_location != packet_processed_file_location) and (event_to_process_file_location != event_processed_file_location):
                # If the files are new then return to main function.
                break
        # If the previous file is same as the latest file then go back to loop.
        else:
            time.sleep(10)
            continue
    # Cleanup and exit function.
    del regex_exp
    gc.collect()
    return packet_to_process_file_location, event_to_process_file_location

def file_expunger(packet_processed_file_location, event_processed_file_location):
    ''' This function deletes processed files to save disk space. '''
    os.remove(packet_processed_file_location)
    os.remove(event_processed_file_location)
    return None

def main():
    ''' This is the main function for orchestration. '''
    # Capturing the configurations.
    variables, locations = config_reader()
    # Setting the target files
    event_path = locations["suricata_path"]
    packet_path = locations["packet_path"]
    merged_path = locations["merged_path"]
    # Setting the timestamp we need to look for.
    packet_processed_file_location = int(variables["initial_file"])
    event_processed_file_location = int(variables["initial_file"])
    # Starting an infinite loop.
    while True:
        print("[*] Starting file lookup loop.")
        # Catching the files which needs to be processed and passing it to the merger.
        packet_to_process_file_location, event_to_process_file_location = file_lookup(packet_path, event_path, packet_processed_file_location, event_processed_file_location)
        # Calling the merge function on latest files.
        # Everyone has to do things that they are not proud of...
        # May God have mercy on me when the judgement day arrives.
        print("[*] Calling merger.")
        subprocess.run(["python3", "/app/second_entry.py", "{}".format(packet_to_process_file_location), "{}".format(event_to_process_file_location), "{}".format(merged_path)])
        print("[*] Completed merge call.")
        # Updating the processed file variables.
        packet_processed_file_location = packet_to_process_file_location
        event_processed_file_location = event_to_process_file_location
        # Expunging function which deletes the files once they have been processed to save disk space.
        file_expunger(packet_processed_file_location, event_processed_file_location)
        print("[*] Cleaned used files.")
# Starting the function.
if __name__ == '__main__':
    # Calling main function to start merging the files.
    main()
