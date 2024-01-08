#!/usr/bin/env python3
# Copyright   : Whizhack Technologies Pvt Ltd
# Author      : Nikhil Garg, Pratima Tiwari
# Description : This is an automation script for building xdr-website. 
# Usage       : This script will automatically update the variables (written in config.ini) in their respective location.
# Version     : 1.0.0

import os

def client_frontend():
    # Read the client URL from the config file
    with open('config.ini', 'r') as config_file:
        for line in config_file:
            if line.startswith('client_domain_url='):
                client_url = line.strip().split('=')[1]
                break

    #Read client frontend directory location from config file
    with open('config.ini', 'r') as config_file:
        for line in config_file:
            if line.startswith('client_frontend_dir_loc='):
                c_frontend_dir_loc = line.strip().split('=')[1]
                break

    #Joining the exact location with dist
    client_frontend_axios = os.path.join(c_frontend_dir_loc, 'src/axios.js')

    # Read the file with the data
    with open(client_frontend_axios , 'r') as data_file:
        data = data_file.read()

    # Replace '<<CLIENT-DOMAIN-URL>>' with the client URL
    updated_data = data.replace('<<CLIENT-DOMAIN-URL>>', client_url)

    # Write the updated data back to the file
    with open(client_frontend_axios , 'w') as data_file:
        data_file.write(updated_data)
        
def main():
    #Running functions
    #master_frontend()
    #master_backend()
    client_frontend()
    #client_backend()

main()
    
                
