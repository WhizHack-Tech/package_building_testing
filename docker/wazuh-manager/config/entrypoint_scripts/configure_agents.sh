#!/bin/bash

cat >/var/ossec/etc/shared/default/agent.conf <<EOL
<agent_config>
  <syscheck>
    <disabled>no</disabled>

    <!-- Frequency that syscheck is executed default every 12 hours -->
    <frequency>21600</frequency>

    <scan_on_start>yes</scan_on_start>

    <!-- Generate alert when new file detected -->
    <alert_new_files>yes</alert_new_files>

    <!-- Don't ignore files that change more than 3 times -->
    <auto_ignore>no</auto_ignore>
    
    <!-- Directories to check  (perform all possible verifications) -->
    <directories>/bin,/sbin,/boot</directories>
    <directories whodata="yes" check_all="yes" report_changes="yes" realtime="yes">/home,/etc,/usr/bin,/usr/sbin</directories>
    <directories whodata="yes" check_all="yes" realtime="yes" report_changes="yes">/home/*/Desktop</directories>
    <directories whodata="yes" check_all="yes" realtime="yes" recursion_level="3" report_changes="yes">C:\Users\*\OneDrive\Desktop</directories>    
    <directories whodata="yes" check_all="yes" realtime="yes" recursion_level="3" report_changes="yes">C:\Users\*\Desktop</directories>
    <directories whodata="yes" check_all="yes" realtime="yes" recursion_level="3" report_changes="yes">C:\Users\*\Downloads</directories>
    <directories whodata="yes" check_all="yes" realtime="yes" recursion_level="3" report_changes="yes">C:\Users\*\Documents</directories>

    <!-- Files/directories to ignore -->
    <ignore>/etc/mtab</ignore>
    <ignore>/etc/hosts.deny</ignore>
    <ignore>/etc/mail/statistics</ignore>
    <ignore>/etc/random-seed</ignore>
    <ignore>/etc/random.seed</ignore>
    <ignore>/etc/adjtime</ignore>
    <ignore>/etc/httpd/logs</ignore>
    <ignore>/etc/utmpx</ignore>
    <ignore>/etc/wtmpx</ignore>
    <ignore>/etc/cups/certs</ignore>
    <ignore>/etc/dumpdates</ignore>
    <ignore>/etc/svc/volatile</ignore>
    <ignore>/sys/kernel/security</ignore>
    <ignore>/sys/kernel/debug</ignore>
    <ignore>/home/*/.mozilla</ignore>
    <ignore>/home/*/.cache</ignore>

    <!-- File types to ignore -->
    <ignore type="sregex">.log$|.swp$</ignore>

    <!-- Check the file, but never compute the diff -->
    <nodiff>/etc/ssl/private.key</nodiff>

    <skip_nfs>yes</skip_nfs>
    <skip_dev>yes</skip_dev>
    <skip_proc>yes</skip_proc>
    <skip_sys>yes</skip_sys>

    <!-- Frequency for ACL checking (seconds) -->
    <windows_audit_interval>60</windows_audit_interval>

    <!-- Nice value for Syscheck module -->
    <process_priority>10</process_priority>

    <!-- Maximum output throughput -->
    <max_eps>1000</max_eps>

    <!-- Database synchronization settings -->
    <synchronization>
      <enabled>yes</enabled>
      <interval>5m</interval>
      <max_eps>10</max_eps>
    </synchronization>
  </syscheck>
</agent_config>

EOL

chown wazuh:wazuh /var/ossec/etc/shared/default/agent.conf
chmod 660 /var/ossec/etc/shared/default/agent.conf

