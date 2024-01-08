#  ==================================================================================================
#  File Name: postgresql_script.py
#  Description: Script to tables in pgadmin database.
#  ---------------------------------------------------------------------------------------------------
#  Item Name: Whizhack Master Dashboard
#  Author URL: https://whizhack.in

#  ====================================================================================================


from unicodedata import name
import psycopg2
from psycopg2 import extensions
import configparser

class Database_Init():

    def __init__(self, login_details = None, Name=None, Password=None):
        # Pass a dictionary containing the details listed in the config.ini
        # dict ={'admin_username': 'postgres' , 'admin_password':'rewash@upheld8@devoutly@only', 'host':'af99d30b47dd042a9a4761348d95dd18-6f5760c7ff3f84cf.elb.us-east-2.amazonaws.com', 'port':'3141', 'username': 'zh_client_jaydeep', 'user_password':'buffed@headway@reason@proving5'}
        dict ={'admin_username': 'postgres' , 'admin_password':'rewash@upheld8@devoutly@only', 'host':'af99d30b47dd042a9a4761348d95dd18-6f5760c7ff3f84cf.elb.us-east-2.amazonaws.com', 'port':'3141', 'username': Name, 'user_password':Password}
        print("Name is:", Name)
        print("password is:", Password)
        login_details=dict
        self.login_details = login_details
        #config_object = configparser.ConfigParser()
        #config_object.read("config.ini")
        #self.login_details = config_object["CONNECTION-OPTIONS"]

    def __connection_handler(self, user_login = False):
        ''' Establishes a connection to database and sends back a connection and cursor object. '''

        # If no argument provided then connect as the admin user.
        if user_login == False:
            psql_creds = {
                'user': '{}'.format(self.login_details["admin_username"]),
                'password': '{}'.format(self.login_details["admin_password"]),
                'port' : '{}'.format(self.login_details["port"]),
                'host': '{}'.format(self.login_details["host"]),
                'sslmode': 'allow',}
            dbconnection = psycopg2.connect(**psql_creds)
            autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
            dbconnection.set_isolation_level( autocommit )
            dbcursor = dbconnection.cursor()
            return dbcursor
    # If an arguement is provided then establish a connection based on provided databasename.
        else:
            psql_creds = {
                'dbname': '{}'.format(self.login_details["username"]), # Database name is always same as username for each user.
                'user': '{}'.format(self.login_details["username"]),
                'password': '{}'.format(self.login_details["user_password"]),
                'port' : '{}'.format(self.login_details["port"]),
                'host': '{}'.format(self.login_details["host"]),
                'sslmode': 'allow',}
            dbconnection = psycopg2.connect(**psql_creds)
            dbcursor = dbconnection.cursor()
            autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
            dbconnection.set_isolation_level( autocommit )
            return dbcursor

    def __user_creation(self, dbcursor):

        # Creating a new user and database for the new user.
        dbcursor.execute(f"CREATE USER {self.login_details['username']} WITH PASSWORD '{self.login_details['user_password']}';")    
        dbcursor.execute(f"CREATE DATABASE {self.login_details['username']};")
        return None

    def __user_setup(self, dbcursor):

        # Defining the attack events tables.
        aws_attack_event = '''
            CREATE table aws_attack_event(
                id uuid,
                packet_id text,
                attacker_ip text,
                attacker_mac text,
                target_id text,
                target_ip text,
                target_mac_address text,
                attack_timestamp timestamp,
                attacker_timezone text,
                data_input_timestamp timestamp,
                type_of_threat text,
                attack_threat_class text,
                attack_threat_type text,
                attack_threat_severity varchar,
                attack_os varchar,
                attacker_asn text,
                attacker_isp text,
                attacker_city text,
                attacker_country text,
                attacker_country_code text,
                attacker_lat text,
                attacker_lon text,
                attacker_region_name text,
                attacker_zip text,
                target_os text,
                target_status text,
                target_type text,
                target_city text,
                target_country text,
                target_region text,
                tcp_port text,
                udp_port text,
                icmp_port text,
                detection_mechanism_id text,
                detection_mechanism text,
                PRIMARY KEY (id));'''
        dbcursor.execute(aws_attack_event)

        azure_attack_event = '''
            CREATE table azure_attack_event(
                id uuid,
                packet_id text,
                attacker_ip text,
                attacker_mac text,
                target_id text,
                target_ip text,
                target_mac_address text,
                attack_timestamp timestamp,
                attacker_timezone text,
                data_input_timestamp timestamp,
                type_of_threat text,
                attack_threat_class text,
                attack_threat_type text,
                attack_threat_severity varchar,
                attack_os varchar,
                attacker_asn text,
                attacker_isp text,
                attacker_city text,
                attacker_country text,
                attacker_country_code text,
                attacker_lat text,
                attacker_lon text,
                attacker_region_name text,
                attacker_zip text,
                target_os text,
                target_status text,
                target_type text,
                target_city text,
                target_country text,
                target_region text,
                tcp_port text,
                udp_port text,
                icmp_port text,
                detection_mechanism_id text,
                detection_mechanism text,
                PRIMARY KEY (id));'''
        dbcursor.execute(azure_attack_event)

        onprim_attack_event = '''
            CREATE table onprim_attack_event(
                id uuid,
                packet_id text,
                attacker_ip text,
                attacker_mac text,
                target_id text,
                target_ip text,
                target_mac_address text,
                attack_timestamp timestamp,
                attacker_timezone text,
                data_input_timestamp timestamp,
                type_of_threat text,
                attack_threat_class text,
                attack_threat_type text,
                attack_threat_severity varchar,
                attack_os varchar,
                attacker_asn text,
                attacker_isp text,
                attacker_city text,
                attacker_country text,
                attacker_country_code text,
                attacker_lat text,
                attacker_lon text,
                attacker_region_name text,
                attacker_zip text,
                target_os text,
                target_status text,
                target_type text,
                target_city text,
                target_country text,
                target_region text,
                tcp_port text,
                udp_port text,
                icmp_port text,
                detection_mechanism_id text,
                detection_mechanism text,
                PRIMARY KEY (id));'''
        dbcursor.execute(onprim_attack_event)
        print("[...] Created attack event tables.")

        # Defining the organization data.
        org_data = '''
            CREATE TABLE org_data (
            org_id uuid,
            config_ip varchar,
            config_port varchar,
            date_format_xi varchar,
            default_currency varchar,
            default_currency_symbol varchar,
            default_language varchar,
            invoice_terms_condition varchar,
            notification_bar varchar,
            notification_close_btn varchar,
            notification_position varchar,
            org_address varchar,
            org_api_id varchar,
            org_api_key varchar,
            org_api_password varchar,
            org_cin_no varchar,
            org_city varchar,
            org_country varchar,
            org_email varchar,
            org_gst_image bytea,
            org_gst_no varchar,
            org_name varchar,
            org_pan_image bytea,
            org_pancard_no varchar,
            org_phone_no varchar,
            org_post_code varchar,
            org_setting_id int,
            org_tan_no varchar,
            publishable_key varchar,
            secret_key varchar,
            sensor_city varchar,
            sensor_code varchar,
            sensor_location varchar,
            sensor_no int,
            sensor_state varchar,
            system_timezone varchar,
            updated_at varchar,
            PRIMARY KEY (org_id));'''
        dbcursor.execute(org_data)
        print("[...] Created organization data table.")

        # Defining roles data within the organization.
        roles_data = '''
            CREATE TABLE org_roles (
            role_uuid uuid,
            role_id int,
            company_id int,
            created_at varchar,
            role_access varchar,
            role_name varchar,
            role_resources varchar,
            PRIMARY KEY (role_id)); '''
        dbcursor.execute(roles_data)
        print("[...] Created organization roles data table.")

        # Defining the settings of the organization.
        org_settings = '''
            CREATE TABLE org_setting (
            setting_id uuid,
            date_format_xi varchar,
            default_currency varchar,
            default_currency_symbol varchar,
            default_language varchar,
            invoice_terms_condition varchar,
            notification_bar varchar,
            notification_close_btn varchar,
            notification_position varchar,
            org_id int,
            publishable_key varchar,
            secret_key varchar,
            system_timezone varchar,
            updated_at varchar,
            PRIMARY KEY (setting_id)); '''
        dbcursor.execute(org_settings)
        print("[...] Created organization settings table.")

        # Defining the details of each user.
        user_details_data = '''
            CREATE TABLE user_data (
            user_id uuid,
            org_id varchar,
            address_1 varchar,
            address_2 varchar,
            asset_alert_mail_alert varchar,
            attack_alert_mail varchar,
            city varchar,
            contact_number varchar,
            country varchar,
            created_date varchar,
            is_active int,
            is_logged_in int,
            last_login_timestamp varchar,
            last_logout_timestamp varchar,
            login_alert_mail varchar,
            login_mail_alert varchar,
            password varchar,
            postcode varchar,
            state varchar,
            threat_attackevent_mail_alart varchar,
            updates_newslatter_mail varchar,
            user_email varchar,
            user_fullname varchar,
            user_roles text [],
            user_type varchar,
            username varchar,
            PRIMARY KEY (user_id)); '''
        dbcursor.execute(user_details_data)
        print("[...] Created user details table.")

        # creating a table which logs each users actions.
        user_log_table = '''
            CREATE TABLE user_log (
            id uuid,
            org_id varchar,
            user_id varchar,
            label_log_id varchar,
            label_value text,
            created_date varchar,
            log_metadata varchar,
            PRIMARY KEY (id));'''
        dbcursor.execute(user_log_table)
        print("[...] Created user log table.")

        network_map_table = '''
            CREATE TABLE organisation_network_map (
                id uuid,
                created_at timestamp,
                aws_map JSONB,
                azure_map JSONB,
                gcp_map JSONB,
                onprim_map JSONB,
                PRIMARY KEY (id));'''
        dbcursor.execute(network_map_table)
        print("[...] Created network map table.")
        return None

    def initialize_user(self):#import the class and call this function
        # Connect as admin and start user initialize process.
        dbcursor = self.__connection_handler()
        self.__user_creation(dbcursor)
        dbcursor.close()
        # Stopping connection and logging in as a user for further setup.
        dbcursor = self.__connection_handler(user_login = True)
        self.__user_setup(dbcursor)
        dbcursor.close()

        return None

# Starting the script.
if __name__ == "__main__":
    database_starter = Database_Init()
    database_starter.initialize_user()