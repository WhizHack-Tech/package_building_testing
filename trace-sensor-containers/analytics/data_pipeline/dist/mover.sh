#!/bin/bash

cat /app/trace_alert.json >> /var/log/zerohack/processed_data/trace_alert.json
cat /app/trace_incident.json >> /var/log/zerohack/processed_data/trace_incident.json
cat /app/trace_event.json >> /var/log/zerohack/processed_data/trace_event.json
cat /app/trace_dpi.json >> /var/log/zerohack/processed_data/trace_dpi.json
