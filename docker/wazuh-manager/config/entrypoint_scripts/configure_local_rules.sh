#!/bin/bash

cat >/var/ossec/etc/rules/local_rules.xml <<EOL
<group name="windows, sysmon,">

  <rule id="100013" level="15">
    <if_sid>61603</if_sid>
    <field name="win.eventdata.commandLine" type="pcre2">(?i)-k LocalServiceNetworkRestricted -pass</field>
    <description>Lockbit 3.0 Ransomware Launched.</description>
    <mitre>
      <id>T1134</id>
    </mitre>
  </rule>
 
  <rule id="100015" level="12" timeframe="100" frequency="2">
    <if_sid>61613</if_sid>
    <field name="win.eventdata.targetFilename" type="pcre2">(?i)\\\\users</field>
    <field name="win.eventdata.targetFilename" type="pcre2">(?i)\.+readme\.txt</field>
    <description>The file $(win.eventdata.targetFilename) has been created in multiple directories. Possible ransomware activity.</description>
  </rule>

  <rule id="100029" level="10">
    <if_sid>61614</if_sid>
    <field name="win.eventdata.targetObject" type="pcre2" >HKLM\\\\System\\\\CurrentControlSet\\\\Services\\\\vmicvss</field>
    <field name="win.eventdata.eventType" type="pcre2" >^DeleteKey$</field>
    <field name="win.eventdata.user" type="pcre2" >NT AUTHORITY\\\\SYSTEM</field>
    <description>Hyper-V volume shadow copy requestor service $(win.eventdata.user) has been deleted on $(win.system.computer). Possible ransomware activity.</description>   
    <mitre>
      <id>T1490</id>
     </mitre>
  </rule>
  
  <rule id="100030" level="10">
    <if_sid>61614</if_sid>
    <field name="win.eventdata.targetObject" type="pcre2" >HKLM\\\\System\\\\CurrentControlSet\\\\Services\\\\VSS</field>
    <field name="win.eventdata.eventType" type="pcre2" >^DeleteKey$</field>
    <field name="win.eventdata.user" type="pcre2" >NT AUTHORITY\\\\SYSTEM</field>
    <description>Volume shadow copy service $(win.eventdata.user) has been deleted on $(win.system.computer). Possible ransomware activity.</description>
    <mitre>
      <id>T1490</id>
    </mitre>
  </rule>

  <rule id="100031" level="10">
    <if_sid>61614</if_sid>
    <field name="win.eventdata.targetObject" type="pcre2" >HKLM\\\\System\\\\CurrentControlSet\\\\Services\\\\WinDefend</field>
    <field name="win.eventdata.eventType" type="pcre2" >^DeleteKey$</field>
    <field name="win.eventdata.user" type="pcre2" >NT AUTHORITY\\\\SYSTEM</field>
    <description>Windows defender service $(win.eventdata.user) has been deleted on $(win.system.computer). Possible Ransomware Activity.</description>
    <mitre>
      <id>T1562.001</id>
    </mitre>
  </rule>
  
  <rule id="100032" level="10" ignore="10">
    <if_sid>61614</if_sid>
    <field name="win.eventdata.targetObject" type="pcre2" >HKLM\\\\SOFTWARE\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\WINEVT\\\\Channels</field>
    <field name="win.eventdata.eventType" type="pcre2" >^CreateKey$</field>
    <description>Multiple Registry Keys created in Event Viewer on $(win.system.computer). Possible Ransomware Activity.</description>
    <mitre>
      <id>T1070.001</id>
    </mitre>
  </rule>
  
</group>
EOL

chown wazuh:wazuh /var/ossec/etc/rules/local_rules.xml
chmods 660 /var/ossec/etc/rules/local_rules.xml