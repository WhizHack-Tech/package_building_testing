#!/bin/bash

cat /app/wazuh_alert.json >> /var/log/data/processed_data/wazuh_alert.json
cat /app/wazuh_incident.json >> /var/log/data/processed_data/wazuh_incident.json
cat /app/wazuh_event.json >> /var/log/data/processed_data/wazuh_event.json
#cat /app/temp.json >> /var/log/data/processed_data/alert.json
