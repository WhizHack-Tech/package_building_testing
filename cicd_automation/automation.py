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
      
def master_backend():
    # Read the postgres URL from the config file
    with open('config.ini', 'r') as config_file:
        for line in config_file:
            if line.startswith('postgres_ip='):
                postgres_ip = line.strip().split('=')[1]
                break
    #Read master frontend directory location from config file
    with open('config.ini', 'r') as config_file:
        for line in config_file:
            if line.startswith('master_backend_dir_loc='):
                m_backend_dir_loc = line.strip().split('=')[1]
                break
    #Joining the exact location with dist
    master_backend_settings = os.path.join(m_backend_dir_loc, 'backend/settings.py')
    # Read the file with the data
    with open(master_backend_settings , 'r') as data_file:
        data = data_file.read()
    # Replace '<<DATABASE-HOST>>' with the database-host ip.
    updated_data = data.replace('<<DATABASE-HOST>>', postgres_ip)
    # Write the updated data back to the file
    with open(master_backend_settings , 'w') as data_file:
        data_file.write(updated_data)
      
  ######################################################################################     
       
    # Read the postgres URL from the config file
    # with open('config.ini', 'r') as config_file:
    #     for line in config_file:
    #         if line.startswith('database='):
    #             database = line.strip().split('=')[1]
    #             break

    # # Read the file with the data
    # with open(master_backend_settings , 'r') as data_file:
    #     data = data_file.read()

    # # Replace 'testing_live_db2' with the testing_live_db11.
    # updated_data = data.replace('testing_live_db2', database)

    # # Write the updated data back to the file
    # with open(master_backend_settings , 'w') as data_file:
    #     data_file.write(updated_data)
            
    # ######################################################################################   
     
    # # Read the client URL from the config file
    # with open('config.ini', 'r') as config_file:
    #     for line in config_file:
    #         if line.startswith('client_full_url='):
    #             client_url = line.strip().split('=')[1]
    #             break

    # #Joining the exact location with dist
    # master_backend_new_user = os.path.join(m_backend_dir_loc, 'backend_app/url_for_new_user.py')

    # # Read the file with the data
    # with open(master_backend_new_user , 'r') as data_file:
    #     data = data_file.read()

    # # Replace 'https://dev-xdr.zerohack.in/generate-new-password/' with the client URL
    # updated_data = data.replace('https://dev-xdr.zerohack.in/generate-new-password/', client_url)

    # # Write the updated data back to the file
    # with open(master_backend_new_user , 'w') as data_file:
    #     data_file.write(updated_data)    
        
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
        
def client_backend():
    # Read the postgres URL from the config file
    with open('config.ini', 'r') as config_file:
        for line in config_file:
            if line.startswith('postgres_ip='):
                postgres_ip = line.strip().split('=')[1]
                break
    #Read client backend directory location from config file
    with open('config.ini', 'r') as config_file:
        for line in config_file:
            if line.startswith('client_backend_dir_loc='):
                c_backend_dir_loc = line.strip().split('=')[1]
                break
    #Joining the exact location with dist
    client_backend_settings = os.path.join(c_backend_dir_loc, 'backend/settings.py')
    # Read the file with the data
    with open(client_backend_settings , 'r') as data_file:
        data = data_file.read()
    # Replace '<<DATABASE-HOST>>' with the database-host ip.
    updated_data = data.replace('<<DATABASE_HOST>>', postgres_ip)
    # Write the updated data back to the file
    with open(client_backend_settings , 'w') as data_file:
        data_file.write(updated_data) 
      
    ####################################################################################     
  
    # Read the postgres URL from the config file
    with open('config.ini', 'r') as config_file:
        for line in config_file:
            if line.startswith('database='):
                database = line.strip().split('=')[1]
                break
    # Read the file with the data
    with open(client_backend_settings , 'r') as data_file:
        data = data_file.read()
    # Replace 'testing_live_db2' with the testing_live_db11.
    updated_data = data.replace('<<SQL_DATABASE_NAME>>', database)
    # Write the updated data back to the file
    with open(client_backend_settings , 'w') as data_file:
        data_file.write(updated_data)
          
    ####################################################################################
  
    # Read the client URL from the config file
    with open('config.ini', 'r') as config_file:
        for line in config_file:
            if line.startswith('client_full_url='):
                client_url = line.strip().split('=')[1]
                break
    #Joining the exact location with dist
    client_backend_new_user = os.path.join(c_backend_dir_loc, 'frontend/url_for_new_user.py')
    # Read the file with the data
    with open(client_backend_new_user , 'r') as data_file:
        data = data_file.read()
    # Replace 'https://dev-xdr.zerohack.in' with the client URL
    updated_data = data.replace('<<CLIENT_DOMAIN_URL>>', client_url)
    # Write the updated data back to the file
    with open(client_backend_new_user , 'w') as data_file:
        data_file.write(updated_data)                 
            
def main():
    #Running functions
    #master_frontend()
    #master_backend()
    #client_frontend()
    client_backend()

main()
    
                
