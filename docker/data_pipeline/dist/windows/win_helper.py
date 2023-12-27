import pandas as pd
import numpy as np
import gc, re, pickle
# Call the 'feature_manipulation' function with the DataFrame 'df'
def feature_manupulation(dataframe):
    dataframe  = dataframe.copy()
    df= dataframe.copy()
    dd = pd.read_excel('windows_sheet.xls')
    for i in dd['Total columns AT FIRST (36)'][1:]:
        if i not in df.columns:
            df[i] = np.nan
    # Define columns to simplify by joining list elements or filling missing values with "Undefined"    
    columns_to_simplify = ['syscheck.attrs_after', 'syscheck.win_perm_after', 'syscheck.changed_attributes', 'rule.groups']
    def simplify_column(column_name):
        df[column_name] = df[column_name].apply(lambda x: ' '.join(map(str, x)) if isinstance(x, list) else "Undefined" if pd.isna(x) else str(x))
    for column in columns_to_simplify:
        simplify_column(column)
    del columns_to_simplify
    gc.collect()
    
    # Convert specified columns to integers and fill missing values with 0
    def convert(df):
        columns_to_convert = ['syscheck.size_after','syscheck.size_before','data.win.system.task','data.win.system.opcode',
                              'data.win.system.level','data.win.eventdata.logonType','data.win.eventdata.reportStatus']
        for column in columns_to_convert:
            df[column] = df[column].fillna(0).astype(int)
        del columns_to_convert
        gc.collect()
    convert(df)
    # Define default values for specified columns and fill missing values with defaults
    def fill(df):
        default_values = {
            'syscheck.event': "Indeterminate",
            'syscheck.value_type': "REG_NONE",
            'syscheck.mode': "Unidentified Status",
            'data.win.system.channel': "No Bridge",
            'data.win.system.severityValue': "Undefined",
            'data.win.system.providerName': "Not found",
            'data.win.system.eventSourceName': "Unknown",
            'data.sca.type': "sca",
            'data.win.eventdata.processName': "No path found",
            'data.win.eventdata.providerName': "No service",
            'syscheck.arch': "[x0]",
            'data.sca.check.reason': "Reason Not Specified",
            'data.sca.check.references': "No Reference Link",
            'data.sca.check.result': "No Result Given",
            'data.win.eventdata.logonProcessName': "Not Specified",
            'data.win.eventdata.appName': "No apps running"
        }
        for column, default_value in default_values.items():
                df[column].fillna(default_value, inplace=True)
        del default_values
        gc.collect()
    fill(df)
    # Determine 'syscheck_size' based on specific conditions
    df["syscheck_size"] = df.apply(lambda row: 
                                            "Created" if row["syscheck.size_before"] == 0 and row["syscheck.size_after"] > 0 and row["syscheck.event"] == "deleted" else
                                            "Upgrade" if row["syscheck.size_before"] == 0 and row["syscheck.size_after"] > 0 and row["syscheck.event"] == "added" else
                                            "Modified" if row["syscheck.size_before"] != row["syscheck.size_after"] and row["syscheck.event"] == "modified" else
                                            "No change", axis=1)
    # Function to classify 'syscheck.audit.process.name' based on keywords in 'path'
    def classify_path(path):
        try:
            if pd.isna(path):
                return 'No Audit Process Running'
            if re.search(r'EdgeWebView|firefox|chrome|msedge', path):
                return 'Web Browser'
            elif re.search(r'Python310|sublime_text|EXCEL|Teams|WINWORD|WinRAR|Microsoft\\Teams|OneDrive', path):
                return 'Productivity App'
            elif re.search(r'steam|pg_dump|svchost|PickerHost|explorer', path):
                return 'System process'
            elif re.search(r'VMware|VirtualBox', path):
                return 'Virtual Machine'
            else:
                return 'New Process'
        except:
            return 'Error'

    df['syscheck.audit.process.name'] = df['syscheck.audit.process.name'].apply(classify_path)
    
    # Function to get a non-null value from two columns or use "MISSING" if both are null
    def get_value(param1, p1):
        try:
            return param1 if pd.notna(param1) else p1 if pd.notna(p1) else "MISSING"
        except Exception as e:
            return 'MISSING'
    df["data.win.eventdata.params"] = df.apply(lambda row: get_value(row["data.win.eventdata.param1"], row["data.win.eventdata.p1"]), axis=1)
    
    # Function to classify 'data.win.eventdata.params' based on specific keywords
    def classify_path_full(path):
        system_keywords = [
            r'(Update;ScanForUpdates|Sysmain|Update;ScanForUpdatesForUser|Update;|windows\.immersivecontrolpanel|Microsoft\.Windows\.ShellExperienceHost|osqueryd\.exe|MoUsoCoreWorker\.exe|qemu-system-x86_64\.exe|studio64\.exe|audiodg\.exe|LiveCaptions\.exe|invcol\.exe|SecurityHealthService\.exe|Microsoft\.MSPaint|Microsoft\.ScreenSketch|OneDrive\.exe|TiWorker\.exe|AdvancedMicroDevicesInc|MicrosoftWindows\.Client\.WebExperience|DisplaySwitch\.exe|mc-fw-host\.exe|Background Intelligent Transfer Service|Windows Modules Installer|DBUtilDrv2 Service|MicrosoftWindows\.Client\.CBS|CortanaUI|Microsoft\.AAD\.BrokerPlugin|windows\.immersivecontrolpanel|microsoft\.windowscommunicationsapps|Windows Image Acquisition|Device Setup Manager|Windows Camera Frame Server Monitor|Windows Security Service|CDPUserSvc|intel_cst_helper_service\.exe)',
            r"windows\.immersivecontrolpanel_10\.0\.6\.1000_neutral_neutral_cw5n1h2txyewy!microsoft\.windows\.immersi[^\s]*",
            r"microsoft\.windowscommunicationsapps_16005\.14326\.21538\.0_x64__8wekyb3d8bbwe!microsoft\.windowslive\.calendar\.AppXwkn9j84yh1kvnt49k5r8h6y1ecsv09hs\.mca",
            r'\\\\Device\\\\HarddiskVolume3\\\\Windows\\\\System32\\\\fcon.dll|\\\\Device\\\\HarddiskVolume3\\\\Windows\\\\System32\\\\drivers\\\\aswVmm.sys',
            r'\\"C:\\\\Windows\\\\system32\\\\backgroundTaskHost.exe\\" -ServerName:App.AppXnme9zjyebb2xnyygh6q9ev6p5d234br2.mca',
            r'\\"C:\\\\Windows\\\\system32\\\\backgroundTaskHost.exe\\" -ServerName:App.AppXskrs33yvbnt65vwp5545yw4r7nkv3h5t.mca'
        ]
        software_keywords = [
            r'Microsoft\.YourPhone_1\.23052\.122\.0_x64__8wekyb3d8bbwe', 'msedgewebview2setup\.exe', 
            r'msedge\.exe', r'WINWORD\.EXE', r'McSync\.exe', r'javaw\.exe', r'Blue Radar\.exe', r'GlobalPresenter\.exe',
            r'RealtekSemiconductorCorp\.RealtekAudioControl_1\.35\.271\.0_x64__dt26b99r8h8gj', r'TextInputHost\.exe',
            r'MicrosoftTeams_23182\.305\.2227\.4931_x64__8wekyb3d8bbwe', r'chrome\.exe', r'firefox\.exe', r'Teams\.exe',
            r'Postman\.exe', r'MicrosoftEdgeUpdate\.exe', r'DAX3API\.exe', r'utweb\.exe', r'node\.exe', r'draw\.io\.exe',
            r'OneDriveUpdaterService\.exe', r'Zoom\.exe', r'java\.exe',
        ]
        third_party_keywords = [
            r'(\{[0-9A-Fa-f-]+\}|Group Policy Client|Npcap Packet Driver|Dell Client Management Service|DellInc\.DellSupportAssistforPCs|Brave Update Service \(brave\)|Dolby DAX API Service|P9RdrService)',
        ]
        security_keywords = [
            r'System Guard Runtime Monitor Broker', r'Microsoft Defender Antivirus Mini-Filter Driver',
            r'Microsoft Defender Antivirus Service', r'McAfee Module Core Service',
            r'Microsoft Defender Antivirus Boot Driver', r'McAfee Framework Host', r'Device Association Service',
        ]
        if path == 'MISSING':
            return 'Unknown Event'
        elif any(re.search(pattern, path) for pattern in system_keywords):
            return 'System'
        elif any(re.search(pattern, path) for pattern in software_keywords):
            return 'Software'
        elif any(re.search(pattern, path) for pattern in third_party_keywords):
            return 'Third Party Services'
        elif any(re.search(pattern, path) for pattern in security_keywords):
            return 'Security'
        else:
            return path
    
    df['data.win.eventdata.params'] = df['data.win.eventdata.params'].apply(classify_path_full)  
    
    # Function to classify 'data.win.eventdata.serviceName' based on specific keywords
    def classify_service(service_name):
        try:
            if pd.isna(service_name):
                return "No Service"
            keywords = {
                "Dell": "Dell services",
                "DBUtil": "Dell services",
                "VirtualBox": "Virtual Machines",
                "VMware": "Virtual Machines",
                "Sysmon": "Security services",
                "Software Monitor": "Security services",
                "osqueryd": "Network services",
                "Npcap": "Network services",
                "BioNTDrv": "Network services",
                "MpKs": "Anti-virus services",
                "McAfee": "Anti-virus services",
            }
            for keyword, category in keywords.items():
                if keyword in service_name:
                    return category
            return "Service Not Known"
        except Exception as e:
            pass
    df['data.win.eventdata.serviceName'] = df['data.win.eventdata.serviceName'].apply(classify_service)
    
    # Function to classify 'data.win.eventdata.eventName' based on specific event categories
    def classify_event(event_name):
        event_categories = {
            'Application Error': [
                'MoAppHang', 'APPCRASH', 'MoAppHangXProc', 'MoAppCrash',
                'CameraStartupFailureEvent', 'AppHangB1'
            ],
            'Update Error': [
                'StoreAgentDownloadFailure1', 'StoreAgentInstallFailure1',
                'SkyDriveClientError', 'StoreAgentScanForUpdatesFailure0',
                'StoreAgentSearchUpdatePackagesFailure1', 'crashpad_log'
            ],
            'System Error': [
                'AppxDeploymentFailureBlue', 'RADAR_PRE_LEAK_64',
                'LiveKernelEvent', 'ContainerCrashDump', 'BlueScreen',
                'CLR20r3', 'MoBEX', 'BEX64'
            ],
        }
        for category, event_list in event_categories.items():
            if event_name in event_list:
                return category

        if pd.isna(event_name):
            return 'Error Unspecified'
        else:
            return 'New Error'
    df['data.win.eventdata.eventName'] = df['data.win.eventdata.eventName'].apply(classify_event)

    # Function to classify 'data.win.eventdata.keyName' based on keywords
    def classify_key(key):
        if pd.isna(key):
            return "Unknown"
        if any(keyword in key for keyword in ['AAD.', 'TB_0_aadrm.com', 'TB_2_aadrm.com', 'TB_1_aadrm.com']):
            return "Azure Active Directory"
        elif any(keyword in key for keyword in ['TB_0_api.', 'TB_2_api.', 'TB_1_api.']):
            return "API"
        elif any(keyword in key for keyword in ['TB_0_', 'TB_1_', 'TB_2_', 'Microsoft Connected Devices Platform device certificate']):
            return "Microsoft domain"
        else:
            return "New Key Name"

    # Apply the 'classify_key' function to 'data.win.eventdata.keyName' column
    df['data.win.eventdata.keyName'] = df['data.win.eventdata.keyName'].apply(classify_key)

    # Combine 'param2' and 'param3' columns and classify 'data.win.eventdata.paramtype'
    df['data.win.eventdata.paramtype'] = df['data.win.eventdata.param2'].fillna("Missing").astype(str) + ' ' + df['data.win.eventdata.param3'].fillna("Missing").astype(str)
    # Function to classify 'data.win.eventdata.paramtype' based on keywords
    def classify_param(param):
        if param == 'Missing Missing':
            return "Anonymous event"
        benign_keywords = ['demand start auto start', 'disabled demand start', 'disabled auto start', 'disabled system start']
        warning_keywords = ['auto start demand start', 'demand start disabled', 'demand start boot start', 'auto start disabled', 'system start disabled']
        if any(keyword in param for keyword in benign_keywords):
            return "Benign Event"
        elif any(keyword in param for keyword in warning_keywords):
            return "Warning Event"
        else:
            return "New Event"
    df['data.win.eventdata.paramtype'] = df['data.win.eventdata.paramtype'].apply(classify_param)

    # Function to classify 'rule.groups' based on specific keywords
    def classify_rule(rule):
        if 'windows_security' in rule:
            return 'Windows Security Events'
        elif 'windows_system' in rule or 'windows_application' in rule:
            return 'Windows System Events'
        elif any(keyword in rule for keyword in ['ossec', 'wazuh', 'sca']):
            return 'Host Security'
        else:
            return 'Not Specified'
    df['rule.groups'] = df['rule.groups'].apply(classify_rule)
    with open('windows.pkl', 'rb') as file:
        pipeline = pickle.load(file)
    dd = dd['Total Columns FINAL (32)'][1:33].to_list()
    dataframe['anomaly_label'] = pipeline.predict(df[dd])
    df=df.add_suffix('_')
    append_str = '_'
    dd= [sub + append_str for sub in dd]
    dataframe =  pd.concat([dataframe, df[dd]], axis = 1)
    dataframe = dataframe.drop_duplicates(subset=dd)
    dataframe.drop(columns=dd, inplace=True)
    del df
    gc.collect()
    return dataframe
