#!/usr/bin/env python3
# Copyright   : Whizhack Technologies Pvt Ltd
# Author      : Nikhil Garg, Pratima Tiwari
# Description : This is an automation script for building xdr-website. 
# Usage       : This script will automatically update the variables (written in config.ini) in their respective location.
# Version     : 1.0.0

import os

def master_frontend():

    # Read the master URL from the config file
    with open('config.ini', 'r') as config_file:
        for line in config_file:
            if line.startswith('master_domain_url='):
                master_url = line.strip().split('=')[1]
                break

    #Read master frontend directory location from config file
    with open('config.ini', 'r') as config_file:
        for line in config_file:
            if line.startswith('master_frontend_dir_loc='):
                m_frontend_dir_loc = line.strip().split('=')[1]
                break
    
    #Joining the exact location with dist
    master_frontend_axios= os.path.join(m_frontend_dir_loc, 'src/axios.js')

    # Read the file with the data
    with open(master_frontend_axios , 'r') as data_file:
        data = data_file.read()

    # Replace '<<MASTER-DOMAIN-URL>>' with the master URL
    updated_data = data.replace('<<MASTER-DOMAIN-URL>>', master_url)

    # Write the updated data back to the file
    with open(master_frontend_axios, 'w') as data_file:
        data_file.write(updated_data)
        
   
            
def main():
    #Running functions
    master_frontend()
    #master_backend()
    #client_frontend()
    #client_backend()

main()
    
                
