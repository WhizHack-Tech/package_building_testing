import pandas as pd
import numpy as np
import boto3,codecs,json, gzip, gc, warnings
from io import StringIO, BytesIO
from win_helper import *
# from termcolor import colored
warnings.filterwarnings('ignore')
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',None)
# -------------------------------------------------------------------------
s3= boto3.resource(
    service_name='s3',
    region_name='us-east-1')
print('[*] Sort files in S3')
def getFiles(bucket_name,str_prefix):
    my_bucket = s3.Bucket(bucket_name)
    evefiles = my_bucket.objects.filter(Prefix=str_prefix)
    eve_sorted = [[obj.key,obj.last_modified.strftime('%Y-%m-%d %H:%M:%S')] for obj in sorted(evefiles, key=lambda x: x.last_modified,reverse=False)]
    print('[*] Total No Of files in s3:',len(eve_sorted))
    return eve_sorted

# For Extracting Data From Bucket
# -------------------------------
def getDatafromS3(from_bucket,files):
    # Input the Bucket name and windows agent names according to requirement:
    # ---------------------------------------------------------------------
    agent_names = ["L-001","L-008","L-009","L-011","L-012","L-013","L-015","L-018","L-020","L-026","L-031",
                   "L-032","L-033","L-034","L-035","L-038","L-022"]
    lst=[]
    for key in files:
        # key = ['wazuh/202309130834_0.gz', '2023-09-13 08:45:06']
        key=key[0]
        try:
            obj = s3.Object(from_bucket, key)
            with gzip.GzipFile(fileobj=obj.get()["Body"]) as gzipfile:
                data = pd.json_normalize([json.loads(i)for i in gzipfile.readlines()])
                data = data[data['agent.name'].isin(agent_names)]
                if data.shape[0] > 1:
                    # Drop rows with 100% NaN values
                    data = data.dropna(axis=1, how='all')
                lst.append(data)
        except Exception as e:
            print("error found:", key, e)
            pass
    data3 = pd.concat(lst, ignore_index=True)
    del lst,obj
    return data3

def get_data(from_bucket, key):
    files = getFiles(from_bucket, key)
    print('[*] Taking no of records according to us:')
    data = getDatafromS3(from_bucket, files[-1:])
    # Apply filter based on agent names (windows agents)
    return data

df = get_data('s3-hids', 'wazuh/')

df = feature_manupulation(df)
owner = {
        "L-001": "Jyoti",
        "L-008": "Devansh",
        "L-009": "Malvika",
        "L-011": "Divya",
        "L-012": "Piyush",
        "L-013": "Meghna",
        "L-015": "Harihar",
        "L-018": "Sarvesh",
        "L-020": "Rajat",
        "L-026": "Vidhushi",
        "L-031": "Sai",
        "L-032": "Danish",
        "L-033": "Baby",
        "L-034": "Priya",
        "L-035": "Jaydeep",
        "L-038": "Divyansh",
        "L-022": "Hemang"
    }
# Map owner names to the 'owner' column based on 'agent.name'
df['User_Name'] = df['agent.name'].map(owner)
df['Os_Info'] = "Windows"
# Release memory by deleting the 'owner' dictionary and running garbage collection
del owner
gc.collect()
# Define a function to replace 'old_word' with 'new_word' in a string
def replace_word(text):
    if isinstance(text, str):
        return text.replace('wazuh', 'HIDS')
    else:
        return text
    
# Apply the replace_word function to each cell in the DataFrame using .applymap()
df = df.applymap(replace_word)
# Resetting index and dropping null values in source host and destination host.
df = df.reset_index(drop=True)
# Filter rows where 'rule.level' values are between 3 and 7
event = df[(df['rule.level'] >= 3) & (df['rule.level'] <= 7)]
# Filter rows where 'rule.level' values are greater than 7 and less than 12
alert = df[(df['rule.level'] > 7) & (df['rule.level'] < 12)]
# Filter rows where 'rule.level' values are greater than 12
incident = df[df['rule.level'] > 12]
print(event.shape, alert.shape, incident.shape)
event.to_json('event.json', orient = 'records', lines = True)
alert.to_json('alert.json', orient = 'records', lines = True)
incident.to_json('incident.json', orient = 'records', lines = True)
del df, event, alert, incident
gc.collect()
