# Filename : Global Threat Feed Generator
# Purpose/Description : The code in this file fetches and consolidates threat information from the pre-defined sources and feeds processes them and sends them to opensearch datastore.
# Author : Amisha Prashar
# Copyright (c) : Whizhack Technologies (P) Ltd.
# Revisions/Modifications : Mahesh Banerjee ,Lakshy Sharma, Nikhil Garg, Nikhilesh Kumar
import requests, os, ndjson
import numpy as np
import json
import time
import logging
import pandas as pd

SLEEP_TIME = 21600
timestamp = time.strftime('%Y-%m-%d %H:%M:%S')


def download_blacklisted_hosts(threatFeed):
    # Ransomware hosts
    url = "https://blocklistproject.github.io/Lists/ransomware.txt"
    request = requests.get(url)
    with open("hosts.txt", "wb") as file:
        file.write(request.content)
    os.system('''sed -i '/^#/d' hosts.txt && sed -i -e 's/0.0.0.0 //' hosts.txt && sed -i -e '/^\s*$/d' hosts.txt; ''')
    with open("hosts.txt", "r") as file:
        for line in file:
            threat_data = {}
            domain = line.strip()
            threat_data["timestamp"] = timestamp
            threat_data["threat_signature"] = domain
            threat_data["threat_nature"] = "Domain"
            threat_data["attacker_domain"] = "Blacklisted Ransomware Domain"
            threat_data["malware_type"] = "Ransomware"
            threat_data["intel_source_feed_name"] = "Blocklist Project"
            threat_data["current_status"] = "online"
            threat_data["associated_domain"] = domain
            threat_data["threat_severity"] = 1
            threatFeed.append(threat_data)
    # Fraud hosts
    url = "https://blocklistproject.github.io/Lists/fraud.txt"
    request = requests.get(url)
    with open("hosts.txt", "wb") as file:
        file.write(request.content)
    os.system('''sed -i '/^#/d' hosts.txt && sed -i -e 's/0.0.0.0 //' hosts.txt && sed -i -e '/^\s*$/d' hosts.txt; ''')
    with open("hosts.txt", "r") as file:
        for line in file:
            threat_data = {}
            domain = line.strip()
            threat_data["timestamp"] = timestamp
            threat_data["threat_signature"] = domain
            threat_data["threat_nature"] = "Domain"
            threat_data["attacker_domain"] = "Blacklisted Fraud Domain"
            threat_data["malware_type"] = "Potential Fraud"
            threat_data["intel_source_feed_name"] = "Blocklist Project"
            threat_data["current_status"] = "online"
            threat_data["associated_domain"] = domain
            threat_data["threat_severity"] = 2
            threatFeed.append(threat_data)

    # Gambling
    url = "https://blocklistproject.github.io/Lists/gambling.txt"
    request = requests.get(url)
    with open("hosts.txt", "wb") as file:
        file.write(request.content)
    os.system('''sed -i '/^#/d' hosts.txt && sed -i -e 's/0.0.0.0 //' hosts.txt && sed -i -e '/^\s*$/d' hosts.txt; ''')
    with open("hosts.txt", "r") as file:
        for line in file:
            threat_data = {}
            domain = line.strip()
            threat_data["timestamp"] = timestamp
            threat_data["threat_signature"] = domain
            threat_data["threat_nature"] = "Domain"
            threat_data["attacker_domain"] = "Blacklisted Gambling Domain"
            threat_data["malware_type"] = "Potential Gambling"
            threat_data["intel_source_feed_name"] = "Blocklist Project"
            threat_data["current_status"] = "online"
            threat_data["associated_domain"] = domain
            threat_data["threat_severity"] = 3
            threatFeed.append(threat_data)

    # Malware 
    url = "https://blocklistproject.github.io/Lists/malware.txt"
    request = requests.get(url)
    with open("hosts.txt", "wb") as file:
        file.write(request.content)
    os.system('''sed -i '/^#/d' hosts.txt && sed -i -e 's/0.0.0.0 //' hosts.txt && sed -i -e '/^\s*$/d' hosts.txt; ''')
    with open("hosts.txt", "r") as file:
        for line in file:
            threat_data = {}
            domain = line.strip()
            threat_data["timestamp"] = timestamp
            threat_data["threat_signature"] = domain
            threat_data["threat_nature"] = "Domain"
            threat_data["attacker_domain"] = "Blacklisted Malicious Domain"
            threat_data["malware_type"] = "Malicious Domain"
            threat_data["intel_source_feed_name"] = "Blocklist Project"
            threat_data["current_status"] = "online"
            threat_data["associated_domain"] = domain
            threat_data["threat_severity"] = 2
            threatFeed.append(threat_data)

    # Phishing
    url = "https://blocklistproject.github.io/Lists/phishing.txt"
    request = requests.get(url)
    with open("hosts.txt", "wb") as file:
        file.write(request.content)
    os.system('''sed -i '/^#/d' hosts.txt && sed -i -e 's/0.0.0.0 //' hosts.txt && sed -i -e '/^\s*$/d' hosts.txt; ''')
    with open("hosts.txt", "r") as file:
        for line in file:
            threat_data = {}
            domain = line.strip()
            threat_data["timestamp"] = timestamp
            threat_data["threat_signature"] = domain
            threat_data["threat_nature"] = "Domain"
            threat_data["attacker_domain"] = "Blacklisted Phishing Domain"
            threat_data["malware_type"] = "Phishing"
            threat_data["intel_source_feed_name"] = "Blocklist Project"
            threat_data["current_status"] = "online"
            threat_data["associated_domain"] = domain
            threat_data["threat_severity"] = 1
            threatFeed.append(threat_data)

    # Drugs 
    url = "https://blocklistproject.github.io/Lists/drugs.txt"
    request = requests.get(url)
    with open("hosts.txt", "wb") as file:
        file.write(request.content)
    os.system('''sed -i '/^#/d' hosts.txt && sed -i -e 's/0.0.0.0 //' hosts.txt && sed -i -e '/^\s*$/d' hosts.txt; ''')
    with open("hosts.txt", "r") as file:
        for line in file:
            threat_data = {}
            domain = line.strip()
            threat_data["timestamp"] = timestamp
            threat_data["threat_signature"] = domain
            threat_data["threat_nature"] = "Domain"
            threat_data["attacker_domain"] = "Blacklisted Drugs Domain"
            threat_data["malware_type"] = "Potentially Drug Dealing Domain"
            threat_data["intel_source_feed_name"] = "Blocklist Project"
            threat_data["current_status"] = "online"
            threat_data["associated_domain"] = domain
            threat_data["threat_severity"] = 1
            threatFeed.append(threat_data)

    # Crypto jackers
    url = "https://blocklistproject.github.io/Lists/crypto.txt"
    request = requests.get(url)
    with open("hosts.txt", "wb") as file:
        file.write(request.content)
    os.system('''sed -i '/^#/d' hosts.txt && sed -i -e 's/0.0.0.0 //' hosts.txt && sed -i -e '/^\s*$/d' hosts.txt; ''')
    with open("hosts.txt", "r") as file:
        for line in file:
            threat_data = {}
            domain = line.strip()
            threat_data["timestamp"] = timestamp
            threat_data["threat_signature"] = domain
            threat_data["threat_nature"] = "Domain"
            threat_data["attacker_domain"] = "Blacklisted Crypto Domain"
            threat_data["malware_type"] = "Cryptojacking and Scams"
            threat_data["intel_source_feed_name"] = "Blocklist Project"
            threat_data["current_status"] = "online"
            threat_data["associated_domain"] = domain
            threat_data["threat_severity"] = 4
            threatFeed.append(threat_data)

    # Piracy 
    url = "https://blocklistproject.github.io/Lists/piracy.txt"
    request = requests.get(url)
    with open("hosts.txt", "wb") as file:
        file.write(request.content)
    os.system('''sed -i '/^#/d' hosts.txt && sed -i -e 's/0.0.0.0 //' hosts.txt && sed -i -e '/^\s*$/d' hosts.txt; ''')
    with open("hosts.txt", "r") as file:
        for line in file:
            threat_data = {}
            domain = line.strip()
            threat_data["timestamp"] = timestamp
            threat_data["threat_signature"] = domain
            threat_data["threat_nature"] = "Domain"
            threat_data["attacker_domain"] = "Blacklisted Piracy Domain"
            threat_data["malware_type"] = "Piracy"
            threat_data["intel_source_feed_name"] = "Blocklist Project"
            threat_data["current_status"] = "online"
            threat_data["associated_domain"] = domain
            threat_data["threat_severity"] = 3
            threatFeed.append(threat_data)

    # Redirecters
    url = "https://blocklistproject.github.io/Lists/redirect.txt"
    request = requests.get(url)
    with open("hosts.txt", "wb") as file:
        file.write(request.content)
    os.system('''sed -i '/^#/d' hosts.txt && sed -i -e 's/0.0.0.0 //' hosts.txt && sed -i -e '/^\s*$/d' hosts.txt; ''')
    with open("hosts.txt", "r") as file:
        for line in file:
            threat_data = {}
            domain = line.strip()
            threat_data["timestamp"] = timestamp
            threat_data["threat_signature"] = domain
            threat_data["threat_nature"] = "Domain"
            threat_data["attacker_domain"] = "Blacklisted Redirection Domain"
            threat_data["malware_type"] = "Potentially Malicious Redirection"
            threat_data["intel_source_feed_name"] = "Blocklist Project"
            threat_data["current_status"] = "online"
            threat_data["associated_domain"] = domain
            threat_data["threat_severity"] = 3
            threatFeed.append(threat_data)

    # Scammers
    url = "https://blocklistproject.github.io/Lists/scam.txt"
    request = requests.get(url)
    with open("hosts.txt", "wb") as file:
        file.write(request.content)
    os.system('''sed -i '/^#/d' hosts.txt && sed -i -e 's/0.0.0.0 //' hosts.txt && sed -i -e '/^\s*$/d' hosts.txt; ''')
    with open("hosts.txt", "r") as file:
        for line in file:
            threat_data = {}
            domain = line.strip()
            threat_data["timestamp"] = timestamp
            threat_data["threat_signature"] = domain
            threat_data["threat_nature"] = "Domain"
            threat_data["attacker_domain"] = "Blacklisted Scam Domain"
            threat_data["malware_type"] = "Scam Domain"
            threat_data["intel_source_feed_name"] = "Blocklist Project"
            threat_data["current_status"] = "online"
            threat_data["associated_domain"] = domain
            threat_data["threat_severity"] = 3
            threatFeed.append(threat_data)

    # Torrents
    url = "https://blocklistproject.github.io/Lists/torrent.txt"
    request = requests.get(url)
    with open("hosts.txt", "wb") as file:
        file.write(request.content)
    os.system('''sed -i '/^#/d' hosts.txt && sed -i -e 's/0.0.0.0 //' hosts.txt && sed -i -e '/^\s*$/d' hosts.txt; ''')
    with open("hosts.txt", "r") as file:
        for line in file:
            threat_data = {}
            domain = line.strip()
            threat_data["timestamp"] = timestamp
            threat_data["threat_signature"] = domain
            threat_data["threat_nature"] = "Domain"
            threat_data["attacker_domain"] = "Blacklisted Torrent Domain"
            threat_data["malware_type"] = "Torrent Domain"
            threat_data["intel_source_feed_name"] = "Blocklist Project"
            threat_data["current_status"] = "online"
            threat_data["associated_domain"] = domain
            threat_data["threat_severity"] = 4
            threatFeed.append(threat_data)

    os.remove("hosts.txt")
    return threatFeed

def download_coresec_list(threatFeed):
    ssh_url = "https://blacklist.3coresec.net/lists/ssh.txt"
    http_url = "https://blacklist.3coresec.net/lists/http.txt"
    mass_scan_url = "https://blacklist.3coresec.net/lists/misc.txt"

    request = requests.get(ssh_url)
    with open("corsecsshdata.json", "wb") as file:
        file.write(request.content)
    request = requests.get(http_url)
    with open("corsechttpdata.json", "wb") as file:
        file.write(request.content)
    request = requests.get(mass_scan_url)
    with open("corsecmassdata.json", "wb") as file:
        file.write(request.content)

    with open("corsecsshdata.json", "r") as file:
        for line in file:
            threat_data = {}
            ip = line.strip()
            threat_data["timestamp"] = timestamp
            threat_data["threat_signature"] = ip
            threat_data["threat_nature"] = "IP"
            threat_data["attacker_domain"] = "SSH Bruteforcing IP Found"
            threat_data["malware_type"] = "Reconnaisance Attempt"
            threat_data["intel_source_feed_name"] = "3 Coresec Blacklisted IP"
            threat_data["current_status"] = "online"
            threat_data["associated_domain"] = "N/A"
            threat_data["threat_severity"] = 1
            threatFeed.append(threat_data)
    with open("corsechttpdata.json", "r") as file:
        for line in file:
            threat_data = {}
            ip = line.strip()
            threat_data["timestamp"] = timestamp
            threat_data["threat_signature"] = ip
            threat_data["threat_nature"] = "IP"
            threat_data["attacker_domain"] = "HTTP Bruteforcing/Enumeration IP Found"
            threat_data["malware_type"] = "Reconnaisance Attempt"
            threat_data["intel_source_feed_name"] = "3 Coresec Blacklisted IP"
            threat_data["current_status"] = "online"
            threat_data["associated_domain"] = "N/A"
            threat_data["threat_severity"] = 1
            threatFeed.append(threat_data)
    with open("corsecmassdata.json", "r") as file:
        for line in file:
            ip = line.strip()
            threat_data = {}
            threat_data["timestamp"] = timestamp
            threat_data["threat_signature"] = ip
            threat_data["threat_nature"] = "IP"
            threat_data["attacker_domain"] = "Mass Scanner IP Found"
            threat_data["malware_type"] = "Reconnaisance Attempt"
            threat_data["intel_source_feed_name"] = "3 Coresec Blacklisted IP"
            threat_data["current_status"] = "online"
            threat_data["associated_domain"] = "N/A"
            threat_data["threat_severity"] = 2
            threatFeed.append(threat_data)

    os.remove("corsecsshdata.json")
    os.remove("corsechttpdata.json")
    os.remove("corsecmassdata.json")
    return threatFeed

def download_feodo_list(threatFeed):
    url = "https://feodotracker.abuse.ch/downloads/ipblocklist_recommended.json"
    request = requests.get(url)
    with open("feododata.json", "wb") as file:
        file.write(request.content)
    with open("feododata.json", "r") as file:
        raw_feodolist = json.loads(file.read())
        for each_item in raw_feodolist:
            threat_data = {}
            threat_data["timestamp"] = timestamp
            threat_data["threat_signature"] = each_item["ip_address"]
            threat_data["threat_nature"] = "IP"
            threat_data["attacker_domain"] = "Banking Trojan"
            threat_data["malware_type"] = each_item["malware"]
            threat_data["intel_source_feed_name"] = "Feodo Blacklisted C&C Servers"
            threat_data["current_status"] = each_item["status"]
            threat_data["associated_domain"] = each_item["hostname"]
            threat_data["threat_severity"] = 1
            threatFeed.append(threat_data)
    os.remove("feododata.json")
    return threatFeed

def download_threatfox_list(threatFeed):
    url = "https://threatfox.abuse.ch/export/json/recent/"
    request = requests.get(url)
    with open("threatfoxdata.json", "wb") as file:
        file.write(request.content)
    with open("threatfoxdata.json", "r") as file:
        threatfox_json = json.loads(file.read())
        for ioc_id in threatfox_json:
            for ioc in threatfox_json[ioc_id]:
                if ioc["ioc_type"] == "ip:port":
                    threat_data = {}
                    threat_data["timestamp"] = timestamp
                    threat_data["threat_signature"] = ioc["ioc_value"].split(':')[0]
                    threat_data["threat_nature"] = "IP"
                    threat_data["attacker_domain"] = ioc["threat_type"].capitalize().replace("_", " ")
                    threat_data["malware_type"] = ioc["malware"]
                    threat_data["intel_source_feed_name"] = "Threatfox"
                    if ioc["last_seen_utc"] != None:
                        threat_data["current_status"] = "online"
                    else:
                        threat_data["current_status"] = "offline"
                    threat_data["associated_domain"] = "N/A"
                    threat_data["threat_severity"] = 1
                    threatFeed.append(threat_data)
                elif ioc["ioc_type"] == "url":
                    threat_data = {}
                    threat_data["timestamp"] = timestamp
                    threat_data["threat_signature"] = ioc["ioc_value"]
                    threat_data["threat_nature"] = "URL"
                    threat_data["attacker_domain"] = ioc["threat_type"].capitalize().replace("_", " ")
                    threat_data["malware_type"] = ioc["malware"]
                    threat_data["intel_source_feed_name"] = "Threatfox"
                    if ioc["last_seen_utc"] != None:
                        threat_data["current_status"] = "online"
                    else:
                        threat_data["current_status"] = "offline"
                    threat_data["threat_severity"] = 1
                    threat_data["associated_domain"] = "N/A"
                    threatFeed.append(threat_data)
                elif ioc["ioc_type"] == "domain":
                    threat_data = {}
                    threat_data["timestamp"] = timestamp
                    threat_data["threat_signature"] = ioc["ioc_value"].split(':')[0]
                    threat_data["threat_nature"] = "Domain"
                    threat_data["attacker_domain"] = ioc["threat_type"].capitalize().replace("_", " ")
                    threat_data["malware_type"] = ioc["malware"]
                    threat_data["intel_source_feed_name"] = "Threatfox"
                    if ioc["last_seen_utc"] != None:
                        threat_data["current_status"] = "online"
                    else:
                        threat_data["current_status"] = "offline"
                    threat_data["threat_severity"] = 1
                    threat_data["associated_domain"] = ioc["ioc_value"].split(':')[0]
                    threatFeed.append(threat_data)
    os.remove("threatfoxdata.json")
    return threatFeed

def download_tor_ips(threatFeed):
    # Capture the TOR Relays
    relay_nodes_url = "https://raw.githubusercontent.com/SecOps-Institute/Tor-IP-Addresses/master/tor-nodes.lst"
    relay_request = requests.get(relay_nodes_url)
    with open("torips.txt", "wb") as file:
        file.write(relay_request.content)
    with open("torips.txt", "r") as file:
        for line in file:
            ip = line.strip()
            threat_data = {}
            threat_data["timestamp"] = timestamp
            threat_data["threat_signature"] = ip
            threat_data["threat_nature"] = "IP"
            threat_data["attacker_domain"] = "Tor Relay Node"
            threat_data["malware_type"] = "N/A"
            threat_data["intel_source_feed_name"] = "Tor Statistics"
            threat_data["current_status"] = "online"
            threat_data["associated_domain"] = "N/A"
            threat_data["threat_severity"] = 4
            threatFeed.append(threat_data)

    # Capture the TOR Exit Nodes.
    exit_nodes_url = "https://raw.githubusercontent.com/SecOps-Institute/Tor-IP-Addresses/master/tor-exit-nodes.lst"
    exit_nodes_request = requests.get(exit_nodes_url)
    with open("torips.txt", "wb") as file:
        file.write(exit_nodes_request.content)
    with open("torips.txt", "r") as file:
        for line in file:
            ip = line.strip()
            threat_data = {}
            threat_data["timestamp"] = timestamp
            threat_data["threat_signature"] = ip
            threat_data["threat_nature"] = "IP"
            threat_data["attacker_domain"] = "Tor Exit Node"
            threat_data["malware_type"] = "N/A"
            threat_data["intel_source_feed_name"] = "Tor Statistics"
            threat_data["current_status"] = "online"
            threat_data["associated_domain"] = "N/A"
            threat_data["threat_severity"] = 3
            threatFeed.append(threat_data)
    os.remove("torips.txt")
    return threatFeed

def download_urlhaus_database(threatFeed):
    url = "https://urlhaus.abuse.ch/downloads/csv_recent/"
    request = requests.get(url)
    with open("urlhausdata.csv", "wb") as file:
        file.write(request.content)
    os.system('''sed -i '1,8d' urlhausdata.csv && sed -i -e 's/# //' urlhausdata.csv;''')
    urlhaus_data = pd.read_csv("urlhausdata.csv")
    for index, row_data in urlhaus_data.iterrows():
        threat_url = row_data["url"]
        threat_data = {}
        threat_data["threat_signature"] = threat_url
        threat_data["threat_nature"] = "URL"
        threat_data["attacker_domain"] = str(row_data["threat"]).replace("_", " ").capitalize()
        #threat_data["attacker_domain"] = row_data["threat"].replace("_", " ").capitalize()
        threat_data["malware_type"] = str(row_data["tags"]).replace(","," ")
        threat_data["intel_source_feed_name"] = "URLHaus"
        threat_data["current_status"] = "online"
        threat_data["associated_domain"] = "N/A"
        threat_data["threat_severity"] = 1
        threatFeed.append(threat_data)

    os.remove("urlhausdata.csv")
    return threatFeed

def download_openphish_database(threatFeed):
    url = "https://openphish.com/feed.txt"
    request = requests.get(url)
    with open("openphishdata.txt", "wb") as file:
        file.write(request.content)
    with open("openphishdata.txt", "r") as file:
        for line in file:
            threat_url = line.strip()
            threat_data = {}
            threat_data["timestamp"] = timestamp
            threat_data["threat_signature"] = threat_url
            threat_data["threat_nature"] = "URL"
            threat_data["attacker_domain"] = "Phishing"
            threat_data["malware_type"] = "Phishing or Spam"
            threat_data["intel_source_feed_name"] = "Openphish"
            threat_data["current_status"] = "online"
            threat_data["threat_severity"] = 1
            threat_data["associated_domain"] = "N/A"
            threatFeed.append(threat_data)
    os.remove("openphishdata.txt")
    return threatFeed
        
def it_exportDatabase(threatFeed):        
    # logging.info(f"Captured {len(threatFeed)} Threats.")
    # with open("/var/log/feed_generator/it_globalFeed.json", "w") as file:
    #     json.dump(threatFeed, file, indent=4)  
      
    logging.info("Exported Feed to Dispatch File.")

def search_json(file_path, search_value):
    with open(file_path, 'r') as json_file:
        data = ndjson.load(json_file)
        for item in data:
            for i in search_value:
                if i in item.values():
                    items = list(item.values())
                    data = {'layer.ip.ip.src_host': items[1], 'attacker_domain': items[3], 'malware_type': items[4], 'intel_source_feed_name': items[5]} 
                    df = pd.DataFrame(data, index=[0])
                    df1 = pd.read_json('/home/aprashar/s3-data/pipeline_df.json', lines=True)
                    df1['attacker_domain'] = None
                    df1['malware_type'] = None
                    df1['intel_source_feed_name'] = None
                    
                    print(df.head())
                    print(df1.head())
                    
                    df2 = pd.merge(df1, df, on='layer.ip.ip.src_host', how='left')
                    print(df2)        
        return None

def main():
    while True:
        logging.info("Initiating IT Feed Collection.")
        threatFeed = []
        threatFeed = download_blacklisted_hosts(threatFeed)
        threatFeed = download_coresec_list(threatFeed)
        threatFeed = download_feodo_list(threatFeed)
        threatFeed = download_threatfox_list(threatFeed)
        threatFeed = download_tor_ips(threatFeed)
        threatFeed = download_urlhaus_database(threatFeed)
        threatFeed = download_openphish_database(threatFeed)
        df = pd.DataFrame(threatFeed)
        df=df[df['threat_nature']=='IP']
        df.drop_duplicates(subset=['threat_signature', 'attacker_domain','malware_type', 'intel_source_feed_name', 'current_status',], inplace= True)
        
        df.to_json('/app/it_globalFeed.ndjson', orient="records", lines=True)
        
        #To facilitate debuging saving the ouput
        #file_path = '/var/log/feed_generator/it_globalFeed.ndjson'
        
        # To facilitate debuging search the generated list
        #search_value = ['101.32.74.175']
        #search_json(file_path, search_value)
        
        break
        #time.sleep(SLEEP_TIME)
main()


  
