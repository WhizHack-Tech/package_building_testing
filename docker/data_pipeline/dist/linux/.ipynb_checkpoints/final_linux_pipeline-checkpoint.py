# Importing Required Libraries
# ============================
import pandas as pd
import numpy as np
import sys,warnings
import boto3,codecs,json, gzip, gc, pickle
from io import StringIO, BytesIO 
from linux_helper import *
warnings.filterwarnings('ignore')
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',None)

# Getting Data from S3
print('[*] Connection with s3')
s3 = boto3.resource(service_name='s3',
                    region_name='us-east-1')
def getFiles(bucket_name,str_prefix):
    my_bucket = s3.Bucket(bucket_name)
    evefiles = my_bucket.objects.filter(Prefix=str_prefix)
    eve_sorted = [[obj.key,obj.last_modified.strftime('%Y-%m-%d %H:%M:%S')] for obj in sorted(evefiles, key=lambda x: x.last_modified,reverse=False)]
    print('[*] Total No Of files in s3:',len(eve_sorted))
    return eve_sorted 

# This function converts list to string
def list2Str(lst):
    try:
        if isinstance(lst, list):
            return",".join(lst)
        else:
            return lst
    except:
        pass
    
# For Extracting Data From Bucket
# -------------------------------
def getDatafromS3(from_bucket,files):
    # Input the Bucket name and windows agent names according to requirement:
    # ---------------------------------------------------------------------
    agent_names = ['L-036', 'L-007','L-016','L-019','L-021','L-025','L-028','L-029','L-030','L-037']
    lst=[]
    for key in files:
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
                else:
                    # print('[*] Data Not coming: ')
                    pass
        except:
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

df=feature_manipulation(df)

dfcc = pd.read_json('data.json', lines = True)
df['User_Name'] = df['agent.name'].map(dfcc.set_index('Asset_Id')['User_Name']) 
df['Os_Info'] = df['agent.name'].map(dfcc.set_index('Asset_Id')['OS_Info'])

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
del df, event, alert, incident, dfcc
gc.collect()
